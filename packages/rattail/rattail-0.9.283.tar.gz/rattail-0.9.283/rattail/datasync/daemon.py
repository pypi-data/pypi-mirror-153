# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
DataSync for Linux
"""

from __future__ import unicode_literals, absolute_import

import sys
import time
import logging
from traceback import format_exception

from rattail.db import api
from rattail.daemon import Daemon
from rattail.threads import Thread
from rattail.datasync.config import load_profiles
from rattail.datasync.util import get_lastrun, get_lastrun_setting, get_lastrun_timefmt, next_batch_id


log = logging.getLogger(__name__)


class DataSyncDaemon(Daemon):
    """
    Linux daemon implementation of DataSync.

    This is normally started via command line, e.g.:

    .. code-block:: sh

       cd /srv/envs/poser
       bin/rattail -c app/datasync.conf datasync start

    .. note::
       Even though the naming implies a "proper" daemon, it will not
       actually daemonize itself.  For true daemon behavior, you
       should run this using a wrapper such as `supervisor`_.

       .. _supervisor: http://supervisord.org
    """

    def run(self):
        """
        Starts watcher and consumer threads according to configuration.

        A separate thread is started for each watcher defined in
        config.  :func:`watch_for_changes()` is the target callable
        for each of these threads.

        Additionally, a separate thread is started for each consumer
        defined for the watcher.  :func:`consume_changes_perpetual()`
        is the target callable for each of these threads.

        Once all threads are started, this (main) thread loops forever
        (so as to stay alive, and hence keep child threads alive) but
        takes no further actions.
        """
        for key, profile in load_profiles(self.config).items():

            # Create watcher thread for the profile.
            name = '{}-watcher'.format(key)
            log.debug("starting thread '{}' with watcher: {}".format(name, profile.watcher_spec))
            thread = Thread(target=watch_for_changes, name=name, args=(self.config, profile.watcher))
            thread.daemon = True
            thread.start()

            # Create consumer threads, unless watcher consumes itself.
            if not profile.watcher.consumes_self:

                # Create a thread for each "isolated" consumer.
                # for consumer in profile.isolated_consumers:
                for consumer in profile.consumers:
                    name = '{}-consumer-{}'.format(key, consumer.key)
                    log.debug("starting thread '%s' with consumer: %s", name, consumer.spec)
                    thread = Thread(target=consume_changes_perpetual, name=name, args=(self.config, consumer))
                    thread.daemon = True
                    thread.start()

        # Loop indefinitely.  Since this is the main thread, the app will
        # terminate when this method ends; all other threads are "subservient"
        # to this one.
        while True:
            time.sleep(.01)


def watch_for_changes(config, watcher):
    """
    Target for datasync watcher threads.

    This function will loop forever (barring an error) and
    periodically invoke the ``watcher`` object to check for any new
    changes, then pause before doing it again, etc.  It also tries to
    detect errors and handle them gracefully.

    The watcher itself is of course responsible for the mechanics of
    checking for new changes.  It also determines how frequently the
    checks should happen, etc.

    Each time the watcher finds/returns changes, this function will
    invoke :func:`record_or_process_changes()` with the result.

    :param config: Config object for the app.

    :param watcher: Reference to datasync watcher object.
    """
    app = config.get_app()

    # let watcher do any setup it needs
    watcher.setup()

    # the 'last run' value is maintained as zone-aware UTC
    lastrun = get_lastrun(config, watcher.key)
    lastrun_setting = get_lastrun_setting(config, watcher.key)
    timefmt = get_lastrun_timefmt(config)

    # outer loop - this should never terminate unless an unhandled
    # exception happens, or the daemon is stopped
    while True:

        # reset for inner loop
        thisrun = app.make_utc(tzinfo=True)
        attempts = 0
        last_error_type = None

        # inner loop - this is for sake of retry
        while True:
            attempts += 1

            try:
                changes = watcher.get_changes(lastrun)

            except Exception as error:

                exc_type, exc, traceback = sys.exc_info()

                # If we've reached our final attempt, stop retrying.
                if attempts >= watcher.retry_attempts:
                    log.warning("attempt #%s of %s failed calling `watcher.get_changes()`, "
                                "this thread will now *terminate* until datasync restart",
                                attempts, watcher.retry_attempts, exc_info=True)
                    app.send_email('datasync_error_watcher_get_changes', {
                        'watcher': watcher,
                        'error': exc,
                        'attempts': attempts,
                        'traceback': ''.join(format_exception(exc_type, exc, traceback)).strip(),
                        'datasync_url': config.datasync_url(),
                    })
                    raise

                # If this exception is not the first, and is of a different type
                # than seen previously, do *not* continue to retry.
                if last_error_type is not None and not isinstance(error, last_error_type):
                    log.exception("new exception differs from previous one(s), "
                                  "giving up on watcher.get_changes()")
                    raise

                # remember which type of error this was; pause for next retry
                last_error_type = type(error)
                log.warning("attempt #%s of %s for watcher.get_changes() failed",
                            attempts, watcher.retry_attempts, exc_info=True)
                log.debug("pausing for %s seconds before making next attempt",
                          watcher.retry_delay)
                if watcher.retry_delay:
                    time.sleep(watcher.retry_delay)

            else: # watcher got changes okay (possibly empty set)

                # record new lastrun time
                lastrun = thisrun
                try:
                    api.save_setting(None, lastrun_setting,
                                     lastrun.strftime(timefmt))
                except:
                    log.exception("failed to save lastrun time")
                    raise

                if changes:
                    log.debug("got %s changes from watcher", len(changes))

                    # record or process changes (depends on watcher)
                    try:
                        record_or_process_changes(config, watcher, changes)
                    except:
                        log.exception("failed to record/process changes")
                        raise

                    # prune changes if applicable (depends on watcher)
                    try:
                        prune_changes(config, watcher, changes)
                    except:
                        log.exception("failed to prune changes")
                        raise

                # break out of inner loop to reset the attempt count
                # for next grab
                break

        # pause between successful change grabs
        time.sleep(watcher.delay)


def record_or_process_changes(config, watcher, changes):
    """
    This function is responsible for the "initial" handling of changes
    obtained from a watcher.  What this means will depend on the
    watcher, as follows:

    Most watchers are just that - their only job is to report new
    changes to datasync.  In this case this function will merely
    "record" the changes, by inserting them into the
    ``datasync_change`` queue table for further processing by the
    consumer(s).

    But some watchers "consume self" - meaning any changes they find,
    they also are responsible for processing.  In this case this
    function will "process" (consume) the changes directly, by
    invoking the watcher to do so.  These changes will *not* be added
    to the queue table for any other consumer(s) to process.

    :param config: Config object for the app.

    :param watcher: Reference to datasync watcher, from whence changes
       came.

    :param changes: List of changes obtained from the watcher.

    :returns: ``True`` if all goes well, ``False`` if error.

       TODO: Actually current logic will raise an error instead of
       returning ``False``.  That may be preferable, in which case
       docs should be updated.  But technically it does still return
       ``True`` if no error.
    """
    app = config.get_app()
    model = config.get_model()

    # if watcher consumes itself, then it will process its own
    # changes.  note that there are no assumptions made about the
    # format or structure of these change objects.
    if watcher.consumes_self:
        try:
            session = app.make_session()
        except:
            log.exception("failed to make session")
            raise
        try:
            watcher.process_changes(session, changes)
        except:
            log.exception("watcher failed to process its changes")
            session.rollback()
            raise
        else:
            session.commit()
            log.debug("watcher has consumed its own changes")
            return True
        finally:
            session.close()

    # will record changes to consumer queue...

    # give all change stubs the same timestamp, to help identify them
    # as a "batch" of sorts, so consumers can process them as such.
    # (note, this is less important for identifiying a batch now that
    # we have batch_id, but is probably still helpful anyway)
    now = app.make_utc()

    # save change stub records to rattail database, for consumer
    # thread to find and process
    saved = 0
    try:
        session = app.make_session()
    except:
        log.exception("failed to make session for recording changes")
        raise
    try:
        # assign new/unique batch_id so that consumers can keep things
        # straight
        batch_id = next_batch_id(session)
        batch_seq = 0
        for key, change in changes:
            batch_seq += 1
            for consumer in watcher.consumer_stub_keys:
                session.add(model.DataSyncChange(
                    source=watcher.key,
                    batch_id=batch_id,
                    batch_sequence=batch_seq,
                    payload_type=change.payload_type,
                    payload_key=change.payload_key,
                    deletion=change.deletion,
                    obtained=now,
                    consumer=consumer))
                saved += 1
            session.flush()
    except:
        log.exception("failed to record changes")
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()

    log.debug("saved %s '%s' changes to datasync queue", saved, watcher.key)
    return True


def prune_changes(config, watcher, changes):
    """
    Tell the watcher to prune the original change records from its source
    database, if relevant.
    """
    if not watcher.prunes_changes:
        return

    try:
        # note that we only give it the keys for this
        pruned = watcher.prune_changes([c[0] for c in changes])
    except:
        log.exception("failed to prune changes")
        raise
    if pruned is not None:
        log.debug("watcher pruned %s changes", pruned)


def consume_changes_perpetual(config, consumer):
    """
    Target for datasync consumer threads.

    This function will loop forever (barring an error) and
    periodically invoke the ``consumer`` object to process any changes
    in the queue, then pause before doing it again, etc.  It also
    tries to detect errors and handle them gracefully.

    This function is mostly just the loop itself; it calls
    :func:`consume_current_changes()` during each iteration.

    :param config: Config object for the app.

    :param consumer: Reference to datasync consumer object.
    """
    # tell consumer to do initial setup
    consumer.setup()

    # begin thread perma-loop
    while True:

        # try to consume all current changes
        try:
            result = consume_current_changes(config, consumer)
        except:
            log.exception("failed to consume current changes")
            raise

        if not result:
            # consumption failed, so exit the perma-loop (this thread
            # is now dead)
            break

        # wait 1 sec by default, then look for more changes
        time.sleep(consumer.delay)


def consume_current_changes(config, consumer):
    """
    Consume all changes currently available for the given consumer.

    The datasync queue table will be checked, and if it contains any
    changes applicable to the given consumer, then the consumer will
    be invoked to process the changes.

    If there are no applicable changes in the queue, this function
    will return without taking any real action.  But if there are
    changes, then it tries to be smart about processing them in the
    correct order, as follows:

    The changes are sorted by
    :attr:`~rattail.db.model.datasync.DataSyncChange.obtained` in
    order to determine the earliest timestamp.  Then it calls
    :func:`consume_changes_from()` with that timestamp.

    Once all changes with that timestamp have been processed
    (consumed), this function again looks for any applicable changes
    in the queue, sorting by timestamp and then calling
    :func:`consume_changes_from()` with earliest timestamp.

    This process repeats until there are no longer any changes in the
    queue which pertain to the given consumer.

    :param config: Config object for the app.

    :param consumer: Reference to datasync consumer object.

    :returns: ``True`` if all goes well, ``False`` if error.
    """
    app = config.get_app()
    model = config.get_model()

    try:
        session = app.make_session()
    except:
        log.exception("failed to make session for consuming changes")
        raise

    def get_first_change():
        change = session.query(model.DataSyncChange)\
                        .filter(model.DataSyncChange.source == consumer.watcher.key)\
                        .filter(model.DataSyncChange.consumer == consumer.key)\
                        .order_by(model.DataSyncChange.obtained)\
                        .first()
        return change

    # determine first 'obtained' timestamp
    try:
        first = get_first_change()
    except:
        log.exception("failed to get first change")
        session.close()
        return False

    error = False
    while first:

        # try to consume these changes
        try:
            if not consume_changes_from(config, session, consumer,
                                        first.obtained):
                error = True
        except:
            error = True
            log.exception("failed to consume changes obtained at: %s",
                          first.obtained)

        if error:
            break

        # fetch next 'obtained' timestamp
        try:
            first = get_first_change()
        except:
            log.exception("failed to get next-first change")
            break

    # no more changes! (or perhaps an error)
    session.close()
    return not error


def consume_changes_from(config, session, consumer, obtained):
    """
    Consume all changes which were "obtained" at the given timestamp.

    This fetches all changes from the datasync queue table, which
    correspond to the given consumer and which have an
    :attr:`~rattail.db.model.datasync.DataSyncChange.obtained` value
    matching the one specified.

    There are two possibilities here: either the matching changes are
    part of a "true" batch (i.e. they have a
    :attr:`~rattail.db.model.datasync.DataSyncChange.batch_id` value),
    or not.

    This function therefore first looks for changes which *do* have a
    ``batch_id``.  If found, it then sorts those changes by
    :attr:`~rattail.db.model.datasync.DataSyncChange.batch_sequence`
    to be sure they are processed in the correct order.

    If none of the changes have a ``batch_id`` then this function does
    not sort the changes in any way; they will be processed in
    (presumably) random order.

    In any case, regardless of ``batch_id``, at this point the
    function has identified a set of changes to be processed as a
    "batch" by the consumer.  But the larger the batch, the longer it
    will take for the consumer to process it.  This brings a couple of
    issues:

    If the consumer is a Rattail DB, and data versioning is enabled,
    this may cause rather massive resource usage if too many data
    writes happen.

    Additionally, there is no true "progress indicator" for datasync
    at this time.  A semi-practical way to determine its progress is
    simply to view the queue table and see what if anything it
    contains (when empty, processing is complete).  The set of changes
    being processed here, will be removed from the queue only after
    being processed.  Hence, the larger the batch, the "less granular"
    the "progress indicator" will be.

    To address these issues then, this function may "prune" the set of
    changes such that only so many are processed at a time.

    And finally, we have a (possibly smaller) set of changes to be
    processed.  This function will then ask the consumer to begin a
    new transaction, then process the changes, and ultimately commit
    the transaction.

    Once processing is complete (i.e. assuming no error) then those
    changes are removed from the queue.

    :param config: Config object for the app.

    :param session: Current session for Rattail DB.

    :param consumer: Reference to datasync consumer object.

    :param obtained: UTC "obtained" timestamp for the first change in
       the queue.  This is used to filter existing changes, i.e. we
       only want to process changes with this same timestamp, as they
       are treated as a single "batch".

    :returns: ``True`` if all goes well, ``False`` if error.
    """
    app = config.get_app()
    model = config.get_model()

    # we only want changes "obtained" at the given time.  however, at least
    # until all code has been refactored, we must take two possibilities into
    # account here: some changes may have been given a batch ID, but some may
    # not.  we will prefer those with batch ID, or fall back to those without.
    changes = session.query(model.DataSyncChange)\
                     .filter(model.DataSyncChange.source == consumer.watcher.key)\
                     .filter(model.DataSyncChange.consumer == consumer.key)\
                     .filter(model.DataSyncChange.obtained == obtained)\
                     .filter(model.DataSyncChange.batch_id != None)\
                     .order_by(model.DataSyncChange.batch_id,
                               model.DataSyncChange.batch_sequence)\
                     .all()
    if changes:
        # okay, we got some with a batch ID, now we must prune that list down
        # so that we're only dealing with a single batch
        batch_id = changes[0].batch_id
        changes = [c for c in changes if c.batch_id == batch_id]
    else:
        # no changes with batch ID, so let's get all without ID instead
        changes = session.query(model.DataSyncChange)\
                         .filter(model.DataSyncChange.source == consumer.watcher.key)\
                         .filter(model.DataSyncChange.consumer == consumer.key)\
                         .filter(model.DataSyncChange.obtained == obtained)\
                         .filter(model.DataSyncChange.batch_id == None)\
                         .all()

    # maybe limit size of batch to process.  this can be useful e.g. when large
    # amounts of changes land in the queue with same timestamp, and versioning
    # is also enabled.
    batch_size = config.getint('rattail.datasync', 'batch_size_limit')
    if batch_size and len(changes) > batch_size:
        changes = changes[:batch_size]

    log.debug("will process %s changes from %s", len(changes),
              app.localtime(obtained, from_utc=True))
    consumer.begin_transaction()

    attempts = 0
    errtype = None
    while True:

        attempts += 1

        try:
            consumer.process_changes(session, changes)

        except Exception as errobj: # processing failed!
            exc_type, exc, traceback = sys.exc_info()

            try:
                consumer.rollback_transaction()
            except:
                log.exception("consumer failed to rollback transaction")
                return False

            # if we've reached our final attempt, stop retrying
            if attempts >= consumer.retry_attempts:
                log.warning("attempt #%s failed calling `consumer.process_changes()`; "
                            "this thread will now *terminate* until datasync restart",
                            attempts, exc_info=True)
                app.send_email('datasync_error_consumer_process_changes', {
                    'watcher': consumer.watcher,
                    'consumer': consumer,
                    'error': exc,
                    'attempts': attempts,
                    'traceback': ''.join(format_exception(exc_type, exc, traceback)).strip(),
                    'datasync_url': config.datasync_url(),
                })
                return False

            # if this exception is not the first, and is of a different type
            # than seen previously, do *not* continue to retry
            if errtype is not None and not isinstance(errobj, errtype):
                log.exception("new exception differs from previous one(s), "
                              "giving up on consumer.process_changes()")
                return False

            # record the type of exception seen; maybe pause before next retry
            errtype = type(errobj)
            log.warning("attempt #%s failed for '%s' -> '%s' consumer.process_changes()",
                        attempts, consumer.watcher.key, consumer.key)
            log.debug("pausing for %s seconds before making attempt #%s of %s",
                      consumer.retry_delay, attempts + 1, consumer.retry_attempts)
            if consumer.retry_delay:
                time.sleep(consumer.retry_delay)

        else: # consumer processed changes okay

            # commit consumer transaction
            try:
                consumer.commit_transaction()
            except:
                log.exception("consumer failed to commit transaction")
                return False

            # delete these changes from datasync queue
            try:
                for i, change in enumerate(changes):
                    session.delete(change)
                    if i % 200 == 0:
                        session.flush()
                session.commit()
            except:
                log.exception("failed to delete changes from queue")
                return False

            # can stop the attempt/retry loop now
            log.debug("processed %s changes", len(changes))
            break

    return True
