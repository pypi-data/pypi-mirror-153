## -*- mode: conf; -*-

<%text>############################################################</%text>
#
# ${app_title} core config
#
<%text>############################################################</%text>


<%text>##############################</%text>
# rattail
<%text>##############################</%text>

[rattail]
app_package = ${app_package}
timezone.default = ${timezone}
appdir = ${appdir}
datadir = ${os.path.join(appdir, 'data')}
batch.files = ${os.path.join(appdir, 'data', 'batch')}
workdir = ${os.path.join(appdir, 'work')}
export.files = ${os.path.join(appdir, 'data', 'exports')}

[rattail.config]
# require = /etc/rattail/rattail.conf
configure_logging = true
usedb = true
preferdb = true

[rattail.db]
default.url = ${db_url}
versioning.enabled = true

[rattail.mail]

# this is the global email shutoff switch
#send_emails = false

# recommended setup is to always talk to postfix on localhost and then
# it can handle any need complexities, e.g. sending to relay
smtp.server = localhost

# by default only email templates from rattail proper are used
templates = rattail:templates/mail

# this is the "default" email profile, from which all others initially
# inherit, but most/all profiles will override these values
default.prefix = [${app_title}]
default.from = rattail@localhost
default.to = root@localhost
# nb. in test environment it can be useful to disable by default, and
# then selectively enable certain (e.g. feedback, upgrade) emails
#default.enabled = false


<%text>##############################</%text>
# alembic
<%text>##############################</%text>

[alembic]
script_location = rattail.db:alembic
version_locations = rattail.db:alembic/versions


<%text>##############################</%text>
# logging
<%text>##############################</%text>

[loggers]
keys = root, exc_logger, beaker, txn, sqlalchemy, django_db, flufl_bounce, requests

[handlers]
keys = file, console, email

[formatters]
keys = generic, console

[logger_root]
handlers = file, console
level = DEBUG

[logger_exc_logger]
qualname = exc_logger
handlers = email
level = ERROR

[logger_beaker]
qualname = beaker
handlers =
level = INFO

[logger_txn]
qualname = txn
handlers =
level = INFO

[logger_sqlalchemy]
qualname = sqlalchemy.engine
handlers =
# handlers = file
# level = INFO

[logger_django_db]
qualname = django.db.backends
handlers =
level = INFO
# level = DEBUG

[logger_flufl_bounce]
qualname = flufl.bounce
handlers =
level = WARNING

[logger_requests]
qualname = requests
handlers =
# level = WARNING

[handler_file]
class = handlers.RotatingFileHandler
args = (${repr(os.path.join(appdir, 'log', 'rattail.log'))}, 'a', 1000000, 100, 'utf_8')
formatter = generic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
formatter = console
# formatter = generic
# level = INFO
# level = WARNING

[handler_email]
class = handlers.SMTPHandler
args = ('localhost', 'rattail@localhost', ['root@localhost'], "[Rattail] Logging")
formatter = generic
level = ERROR

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(funcName)s: %(message)s
datefmt = %Y-%m-%d %H:%M:%S

[formatter_console]
format = %(levelname)-5.5s [%(name)s][%(threadName)s] %(funcName)s: %(message)s
