
CHANGELOG
=========

0.9.284 (2022-06-02)
--------------------

* Bump version to avoid last upload (?).


0.9.283 (2022-06-02)
--------------------

* Allow suppression of warnings when removing duplicate key values.

* Stop using deprecated kwargs for product lookup.


0.9.282 (2022-05-15)
--------------------

* Add ``render_vendor()`` method for VendorHandler.


0.9.281 (2022-05-14)
--------------------

* Tweaks for rattail -> rattail datasync.


0.9.280 (2022-05-03)
--------------------

* Tweak some string encoding for python2.


0.9.279 (2022-04-13)
--------------------

* Tweak some things for customer importer esp. for ``group_ids`` field.

* Tweak how output is decoded, for ``run-n-mail`` command.


0.9.278 (2022-04-06)
--------------------

* Add ``rattail mysql-chars`` command to view/fix charset, collation.

* Add more error handling to datasync; more docs.


0.9.277 (2022-04-04)
--------------------

* Let cases and/or units be (dis)allowed for new custorder.

* Tweak logging when datasync watcher fails.

* Add transaction logic for rattail->rattail datasync.


0.9.276 (2022-03-29)
--------------------

* Allow errors to raise when fetching poser reports.


0.9.275 (2022-03-26)
--------------------

* Try harder to cleanup when datasync error happens.


0.9.274 (2022-03-24)
--------------------

* Refactor session usage for datasync consumers.


0.9.273 (2022-03-22)
--------------------

* Define some "pre-process" logic for datasync consumers.


0.9.272 (2022-03-21)
--------------------

* Define email settings for ``run_n_mail``.


0.9.271 (2022-03-17)
--------------------

* Add custorder xref markers for trainwreck; import logic.


0.9.270 (2022-03-10)
--------------------

* Add basic UNFI catalog parser for tab-separated format.

* Render empty string if no price given.

* Assign report output id explicitly, via counter value.


0.9.269 (2022-03-09)
--------------------

* Fallback to showing employee name field when person missing/empty.

* Record execution kwargs as special params, when executing batch.

* Can't return poser reports if can't import ``poser.reports`` module.


0.9.268 (2022-03-08)
--------------------

* Allow "default" batch handlers to be registered in config.


0.9.267 (2022-03-07)
--------------------

* Add upload "temp dir" setting for pyramid in "complete" ``web.conf``.


0.9.266 (2022-03-05)
--------------------

* Add commands, ``setting-get`` and ``setting-put``.

* Assume remote borg command is just ``borg`` by default.

* Enable email by default in "complete" rattail config template.

* Record app package name in complete config file template.

* Add initial/stub support for managing poser views.

* Add ``AppHandler.render_mako_template()`` convenience method.


0.9.265 (2022-03-02)
--------------------

* Add basic Poser support for custom reports.


0.9.264 (2022-03-01)
--------------------

* Define appdir in complete config template.

* Add very basic / beginnings of Poser Handler.

* Add "vendor not shipped" status for receiving batch.


0.9.263 (2022-02-26)
--------------------

* Some tweaks for importing data from Excel (xlsx) files.

* Add ``config.parse_list()`` method.

* Auto filter by date, for ``trainwreck import-self``.

* Add problem report for "mailmon misses".


0.9.262 (2022-02-25)
--------------------

* Add ``make_appdir()`` and ``make_config_file()`` to AppHandler.

* Add "complete" mako templates for rattail, web config.

* Fetch discounts along with line items for ``trainwreck import-self``.

* Add "discount type" for Trainwreck line item discounts.


0.9.261 (2022-02-20)
--------------------

* Add patronage to trainwreck schema; skeleton for ``import-self`` cmd.

* Add per-item discounts to trainwreck; importing support.

* Add ``AppHandler.render_percent()`` convenience method.


0.9.260 (2022-02-15)
--------------------

* Add AppHandler methods to get/save/delete settings.

* Add "fuzzy fields" support for int/float/decimal.

* Render empty string if currency value is ``None``.


0.9.259 (2022-02-13)
--------------------

* Add "fuzzy fields" concept for importers.

* Make ``locate_product_for_vendor_code()`` prefer unit items.

* Compare received vs. shipped to check row status.

* Add ``AppHandler.render_duration()`` convenience method.

* Stop using legacy syntax to define entry points.


0.9.258 (2022-02-10)
--------------------

* Always pass along associated products when printing label batch.

* Add generic ``get_next_counter_value()`` method for importers.


0.9.257 (2022-02-09)
--------------------

* Show email address for new custorder person autocomplete.


0.9.256 (2022-02-08)
--------------------

* Add common normalize logic to ``ProductsHandler``.


0.9.255 (2022-02-07)
--------------------

* Show pseudo-progress when saving Excel report.

* Lower log level when disconnecting IMAP for mailmon.


0.9.254 (2022-02-06)
--------------------

* Add ``match_on_time_field`` for Trainwreck importers.


0.9.253 (2022-02-05)
--------------------

* Add "all" product locate methods to products handler.

* Commit (or rollback) local transaction before host, when importing.


0.9.252 (2022-02-04)
--------------------

* Tweak vendor catalog batch input params; fix tests.

* Make sure default phone number is first, when importing.

* Add ``group_ids`` field for Customer model importer.


0.9.251 (2022-02-01)
--------------------

* Misc. flexibility improvements for vendor catalog batch.


0.9.250 (2022-02-01)
--------------------

* Allow rattail watcher to get deleted before new/dirty changes.


0.9.249 (2022-01-31)
--------------------

* Rename permission for generating new report.

* Add ``CSVReport`` base class.


0.9.248 (2022-01-31)
--------------------

* Stash docstring for ReportParam in its ``helptext`` attr.

* Add ``safe_filename()`` method for reports.


0.9.247 (2022-01-31)
--------------------

* Always establish start/end date+time range for all importers.

* Fix typo for printing batch of labels.

* Add project generators for rattail-integration, tailbone-integration.

* Add ``--list-all-models`` flag for all import/export commands.

* Avoid cache query when fetching single local object for importer.

* Only delete object if importer allows it, from datasync.

* Change default initial delay for luigi OvernightTask datasync wait.


0.9.246 (2022-01-26)
--------------------

* Fix label printing for 2-up style formatter.

* Allow report output fields to vary based on params.


0.9.245 (2022-01-18)
--------------------

* Be a little smarter about IMAP server disconnect.


0.9.244 (2022-01-15)
--------------------

* Add label handler; refactor label formatting logic.

* Refactor mailmon daemon to ensure only 1 thread per IMAP account.


0.9.243 (2022-01-13)
--------------------

* Add ``AppHandler.make_object()`` convenience method.


0.9.242 (2022-01-10)
--------------------

* Add problem report for stale inventory batches.

* Batch handlers declare versioning is okay for delete action.

* Add explicit Sale, TPR, Current price columns for label batch.

* Add some more logging for mailmon daemon.


0.9.241 (2022-01-08)
--------------------

* Misc. changes for vendor catalog batch and related features.

* Add vendor handler, to better organize catalog parser logic.

* Add ``AppHandler.next_counter_value()`` magic.

* Add nominal support for mysql db backend.

* Refactor some usage of ``cache_model()``.


0.9.240 (2022-01-06)
--------------------

* Remove deprecated use of ``rattail.batch.handlers.get_batch_handler()``.


0.9.239 (2022-01-03)
--------------------

* Fix a couple of dynamic class names, for python2.

* Let datasync consumers declare handler key instead of spec.

* Deprecate the name ``NewDataSyncConsumer`` and update docs.

* Remove usage of ``app.get_designated_import_handler()``.

* Add basic Trainwreck handler.


0.9.238 (2021-12-29)
--------------------

* Remove unused module ``rattail.db.diffs``.

* Move main product lookup logic to products handler.

* Add basic "resolve" support for person, product from new custorder.


0.9.237 (2021-12-23)
--------------------

* Add ``load_object()`` convenience method for AppHandler.

* Make ``config.getint()`` smarter about using default value.

* Add basic "pending product" support for new custorder batch.

* Store copy of msg file just for bouncer, when using.

* Refactor mailmon daemon structure to minimize IMAP connections.

* Add error delay for mailmon, continuum comment for bounce handling.

* Remove support for "daemonize" option in filemon, datasync etc..

* Remove deprecated "dbsync" logic.


0.9.236 (2021-12-20)
--------------------

* Add way to handle an email bounce via filemon.


0.9.235 (2021-12-20)
--------------------

* Set ``app`` attribute for problem report handler, pass to email context.


0.9.234 (2021-12-20)
--------------------

* Make ``app.get_all_import_handlers()`` a bit smarter.


0.9.233 (2021-12-17)
--------------------

* Assign enum and app attrs in datasync consumer constructor.

* Add setting for tailbone grid "sticky headers".

* Expose settings for tailbone vue.js and buefy versions.

* Add basic time-related methods to AppHandler.


0.9.232 (2021-12-14)
--------------------

* Let config know if/when versioning has been enabled.

* Add "missing" tallies for receiving, plus allow un-declare credit.

* Default to false for all config flags in purchase batch handler.

* Stop "requiring" config files by default, it was too problematic.


0.9.231 (2021-12-11)
--------------------

* Fix calculation of seconds since last run for datasync watcher.

* Allow running a problem report just to get results, but avoid email.

* Let progress be passed in late, when running problem report.


0.9.230 (2021-12-09)
--------------------

* Add some purchase order abstractions to purchase batch handler.

* Add default logic for purchase batch ``make_row_from_po_item()``.


0.9.229 (2021-12-08)
--------------------

* Add ``get_problem_report_handler()`` method to AppHandler.

* Use python's ``importlib`` instead of doing our own thing.

* Add ``pre_process_changes()`` and ``post_process_changes()`` for datasync.


0.9.228 (2021-12-07)
--------------------

* Set the ``model`` attr when making new ``AppHandler`` object.


0.9.227 (2021-12-07)
--------------------

* Add some methods/attrs to import handlers, for exposing in web app.

* Overhaul import handler config etc.:
  * add ``AppHandler.get_designated_import_handlers()`` and friends
  * exit w/ code 1 when command line makes no sense and must print help
  * register all core import/export handlers via setup.py and config
  * use "handler key" lookup for all core import/export commands
  * stop displaying model list in help for import/export command
  * migrate datasync "change" permissions, per tailbone changes
  * log warning w/ traceback if loading entry point fails

* Mark only certain handlers as being safe for web app.

* Add ``get_active_stores()`` method for app handler.

* Make config object required, for Report constructor.


0.9.226 (2021-12-03)
--------------------

* Make stale timeout configurable, change default for datasync/collectd.

* Use common logic for basic product refresh in label batch.


0.9.225 (2021-11-29)
--------------------

* Allow loading "disabled" datasync profiles, if caller specifies.

* Add ``rattail datasync remove-settings`` command.

* Always "require" config files when making config object.


0.9.224 (2021-11-28)
--------------------

* Add setting for receiving from PO w/ invoice.

* Add some sale pricing logic for custorder batch.

* Include current time in datasync/collectd output.


0.9.223 (2021-11-27)
--------------------

* Only specify interval if we receive one from collectd.

* Add basic stale queue detection for datasync/collectd.


0.9.222 (2021-11-27)
--------------------

* Add workarounds if collectd does not pass env variables (?).


0.9.221 (2021-11-27)
--------------------

* Postpone import in case no sqlalchemy.

* Move datasync command logic to its own module.

* Add ``rattail datasync collectd`` sub-sub-command.


0.9.220 (2021-11-26)
--------------------

* Add way to "require" included config files.

* Only coerce logging timestamps if we have a timezone set.

* Set ``Subcommand.app`` within constructor, for convenience.


0.9.219 (2021-11-25)
--------------------

* Add basic support for receiving from PO with invoice.


0.9.218 (2021-11-14)
--------------------

* Add ``Role.sync_users`` flag and make importer logic honor it.


0.9.217 (2021-11-11)
--------------------

* Add no-op ``parse_date()`` method for ``ExcelReaderXLSX`` class.


0.9.216 (2021-11-11)
--------------------

* Add basic model, status enum for PendingProduct.


0.9.215 (2021-11-08)
--------------------

* Only show POD image if so configured; use "image not found" fallback.

* Add some "case price" logic for custorder batch.

* Add ``get_past_products()`` method for custorder batch handler.

* Add support for finding past items, for new custorder.

* Add basic support for ``invoice2data`` for InvoiceParser.

* Let purchase batch handler declare supported invoice parsers.

* Add simple ``ExcelInvoicParser`` class.


0.9.214 (2021-11-05)
--------------------

* Add ``progress_loop()`` method for app and generic handlers.

* Add "generic" vendor catalog parser.


0.9.213 (2021-11-04)
--------------------

* Add some product info fetchers to custorder batch handler.

* Add setting for "product price may be questionable" for custorders.


0.9.212 (2021-11-02)
--------------------

* Add "did not receive" status for purchase batch rows.

* Add "cannot calculate price" row status for new product batch.


0.9.211 (2021-10-22)
--------------------

* Assign ``app`` and ``model`` attributes when ProblemReport instantiates.


0.9.210 (2021-10-21)
--------------------

* Record 'lastrun' time when mailmon watcher succeeds.


0.9.209 (2021-10-20)
--------------------

* Improve default autocomplete for products.

* Add ``why_not_add_product()`` for custorder batch handler.

* Limit autocomplete results for customer/phone lookup in new custorder.

* Consolidate "new custorder" autocomplete logic for people, customers.

* Restore "pending" customer when unassigning batch contact.

* Add ``add_product()`` method for custorder batch handler.

* Calculate invoice totals when overlaying onto PO for purchase batch.

* Allow for alternate encoding in CSV importers.

* Add basic "price needs confirmation" support for custorder.

* Make ``product`` the first kwarg to ``get_image_url()``.

* Add new 'products.neworder' autocompleter; refactor a bit.


0.9.208 (2021-10-14)
--------------------

* Fix merge logic when employee needs to be transferred to new person.


0.9.207 (2021-10-14)
--------------------

* Invoke auth handler when deleting a user via importer.


0.9.206 (2021-10-14)
--------------------

* Add support for syncing roles, with users and permissions for each.


0.9.205 (2021-10-13)
--------------------

* Try to guess unit or case cost from invoice, if only one is specified.

* Add basic auth handler concept.


0.9.204 (2021-10-11)
--------------------

* Increase precision for cost fields in purchase, batch.


0.9.203 (2021-10-07)
--------------------

* Add ``PendingCustomer`` model, for sake of new custorder workflow.

* Add ``contact_name`` for custorder and batch.

* Add ``update_pending_customer()`` for custorder batch handler.

* Let ``InventoryBatchRow.case_cost`` equal zero.


0.9.202 (2021-10-06)
--------------------

* Add costing batch logic to overlay invoice onto PO data.

* Always add new/dirty first, deleted last, for RattailWatcher.

* Fix bug in products autocomplete.

* Add custorder batch settings to control contact info choice/editing.

* Add "contact update request" workflow for new custorders.


0.9.201 (2021-10-05)
--------------------

* Add ``get_contact_notes()`` method for custorder batch handler.

* Add ``get_contact_phones()`` method for custorder batch handler.

* Add PeopleHandler methods for add/update of phone, email.

* Improve ``get_context_employee()`` for EmploymentHandler.


0.9.200 (2021-10-03)
--------------------

* Remove some assertions which aren't always true...

* Tweak how we call the change recorder.


0.9.199 (2021-10-03)
--------------------

* Add initial version of the "mailmon" daemon.


0.9.198 (2021-10-01)
--------------------

* Add support for Autocomplete Handlers.

* Add config object to ``ChangeRecorder`` class.

* Add simple error logging when bouncer fails to login to server.


0.9.197 (2021-09-30)
--------------------

* Add basic workflow support for invoice costing (purchase) batches.

* Try to parse invoice number from invoice file.


0.9.196 (2021-09-28)
--------------------

* Add ``format_phone_number()`` method to app handler.

* Make ``get_first_email()`` type methods skip invalid addresses.


0.9.195 (2021-09-27)
--------------------

* Add "all" enum values for custorder item status, event.

* Declare model for CustomerOrderItemNote.


0.9.194 (2021-09-27)
--------------------

* Fix bugs in new clientele methods.


0.9.193 (2021-09-27)
--------------------

* Make custorder batch handler responsible for (un)assigning contact.

* Add ``cache_model()`` method to app handler.


0.9.192 (2021-09-26)
--------------------

* Add ``render_quantity()`` method to app handler.

* Always assign ``app`` attribute when instantiating batch handler.

* Assign store, fix sequence when making a new custorder/batch.


0.9.191 (2021-09-25)
--------------------

* Add "custom" customer autocomplete for new custorder handler.

* Add ``render_price()`` method for products handler.


0.9.190 (2021-09-21)
--------------------

* Flush after deleting batch rows.

* Some tweaks for customer orders.


0.9.189 (2021-09-16)
--------------------

* Add "request merge" logic to people handler; send email alert.


0.9.188 (2021-09-15)
--------------------

* Version bump per botched PyPI upload.


0.9.187 (2021-09-15)
--------------------

* Add ``AppHandler.normalize_phone_number()`` method.

* Cache the configured model when making a datasync watcher.


0.9.186 (2021-09-12)
--------------------

* Add way to customize product autocomplete for new custorder.

* Let "has activity" win over "has inventory" for delproduct row status.


0.9.185 (2021-09-09)
--------------------

* Add basic membership handler structure; tweak people, clientele.

* Allow specifying alternate name for association proxy.

* Raise specific error if batch is already executed.

* Make model importer "extensions" more..extensible.


0.9.184 (2021-09-01)
--------------------

* Tweak some customization hooks for custorder batch handler.


0.9.183 (2021-08-26)
--------------------

* Add ``app.get_email_handler()`` method.

* Add more helpful error, if trainwreck import is missing transaction.

* Add merge-related methods to ``PeopleHandler``, plus some docs.

* Add model for ``MergePeopleRequest`` to track people in need of merge.


0.9.182 (2021-08-04)
--------------------

* Ignore ProductPriceAssociation changes for legacy Rattail datasync consumer.

* Fix datasync bug for Rattail -> Rattail "import".


0.9.181 (2021-08-01)
--------------------

* Refactor how we handle product "price xref" fields via datasync.


0.9.180 (2021-07-27)
--------------------

* Improve default subject logic for importer warning emails.

* Add email config for Rattail <-> Rattail data import/export.


0.9.179 (2021-07-22)
--------------------

* Fix ``super()`` parent bug.


0.9.178 (2021-07-21)
--------------------

* Add dict-specific logic for normalizing "local" object.


0.9.177 (2021-07-21)
--------------------

* Raise error if unknown product scanned for inventory.

* Add special datasync logic for product/price associations.


0.9.176 (2021-07-15)
--------------------

* Auto-expand delproduct batch to include unit + all packs.


0.9.175 (2021-06-18)
--------------------

* Fix template context for importer diff warning email preview.

* Exclude ``suggested_price_uuid`` for rattail->rattail Product import.


0.9.174 (2021-06-18)
--------------------

* Let config set flags for product importing.


0.9.173 (2021-06-18)
--------------------

* Avoid blank upc when caching products.

* Lower log level when product not found.


0.9.172 (2021-06-17)
--------------------

* Add ``--no-collect-changes`` arg for importer commands.


0.9.171 (2021-06-11)
--------------------

* Assume empty string means null, in datetime conversion for CSV import.

* Require ``config`` and ``key`` args for ``ConfigProfile`` constructor.

* Accept extra kwargs for ``util.capture_output()``.

* Fix how cost diffs are checked for vendor catalog batch.

* Fix bug when refreshing single label batch row.

* Tweak basic project template, per LOC SMS integration.

* Add ``PeopleHandler.ensure_address()`` method.


0.9.170 (2021-04-28)
--------------------

* Only make batch data dir if it doesn't exist.

* Add "has inventory" status for delete item batch (rows).

* Add ``batch_id_str()`` convenience function.


0.9.169 (2021-04-27)
--------------------

* Allow "batch importers" to avoid collecting changes for processing.


0.9.168 (2021-04-12)
--------------------

* Don't use ``log.warn()``.

* Add ``render_date()`` method for app handler.


0.9.167 (2021-03-30)
--------------------

* Add ``Store.archived`` flag to schema.

* Only cache departments which have a number.

* Freeze version of SQLAlchemy to 1.3.x.


0.9.166 (2021-03-11)
--------------------

* Fix preview for user_feedback emails.

* Add trainwreck alembic files to project manifest.

* Create the ``data/uploads`` folder when making app dir.

* Better handle cost diff when old value is null, for catalog batch.

* Fix how rsync excludes are used as fallback for borg backup.

* Add ``inactivity_months`` field for delete product batch.

* Add misc. more fields to base Trainwreck schema.


0.9.165 (2021-03-05)
--------------------

* Let include/exclude lists differ for rsync vs. borg, in backup command.

* Add ``date_created`` field for "delete product" batch row.


0.9.164 (2021-03-02)
--------------------

* Move some enum values to rattail-onager.

* Add "pending customer orders" status for delete product batch row.


0.9.163 (2021-02-19)
--------------------

* Add trainwreck enum entry for CORE-POS.

* Add "full" support for Trainwreck <-> Trainwreck import/export commands.


0.9.162 (2021-02-18)
--------------------

* Describe execution for some common batches.

* More improvements to "delete products" batch.

* Misc. tweaks for vendor catalog batch.

* Add proper "default" model for Trainwreck.


0.9.161 (2021-02-10)
--------------------

* Relax validation of phone numbers a bit.


0.9.160 (2021-02-10)
--------------------

* Rename tables for purchase batches.

* Add XLSX-flavored ExcelReader class.

* Fix execution description for purchase batches.

* Always use versioning workarounds for vendor catalog batches.


0.9.159 (2021-02-04)
--------------------

* Add ``make_temp_dir()`` and ``make_temp_path()`` for app handlers.

* Rename tables, models for various batches.
  
* Add ``BatchHandler.is_mutable()``.


0.9.158 (2021-02-01)
--------------------

* Add ``Purchase.id`` column to schema.

* Fix ``PurchaseItem.po_total`` when creating from ordering batch.

* Add ``BatchHandler.describe_execution()`` method.

* Add ``render_currency()`` and ``render_datetime()`` for app handler.

* Misc. reporting tweaks; add "Customer Mailing" sample report.

* Purge things for legacy (jquery) mobile apps.

* Let ``PurchaseBatchHandler`` define which receiving workflows are supported.

* Add ``ProductsHandler.get_image_url()`` etc.


0.9.157 (2021-01-28)
--------------------

* Add basic PeopleHandler, for consistently updating names.


0.9.156 (2021-01-27)
--------------------

* Let win32 share the 'auth' extra.


0.9.155 (2021-01-27)
--------------------

* Initial support for adding items to, executing customer order batch.

* Add simple ``rattail checkdb`` command.


0.9.154 (2021-01-25)
--------------------

* Add some default logic to ``FromFile`` importer base.

* Tweak borg requirement for 'backup' extra.

* Add ``AppHandler.get_report_handler()`` and improve related docs a bit.

* Add feature to generate new features...

* Add basic dev bootstrap for new projects.

* Add new batch type for deleting products.

* Show import vs. export direction in warnings/diff email.

* Set ``self.model`` when constructing new Importer.

* Avoid meaningless flushes within importer main loop.

* Don't use list for ``Product.shopfoo_product`` type relationships.

* Set ``self.model`` when constructing a DataSyncConsumer.

* Add generic ``FromRattailConsumer`` base class for datasync.

* Add "Units of Measure" table, and mapping logic in products handler.

* Add ``webapi.conf`` file for use with ``rattail make-config``.

* Fix some discrepancies in primary vs. version table schema.


0.9.153 (2020-12-15)
--------------------

* Add basic model, importer for IFPS PLU Codes.


0.9.152 (2020-12-04)
--------------------

* Add ``phone_number_is_invalid()`` method to app handler.

* Add basic structure for "Board Handler" feature.

* Add 'datadir' to sample config files.


0.9.151 (2020-12-01)
--------------------

* Add new "app handler" concept, w/ handlers for employment, clientele.


0.9.150 (2020-11-24)
--------------------

* Add vendor catalog parser for Equal Exchange.

* Refresh product record, when attaching new price via importer.


0.9.149 (2020-10-14)
--------------------

* Simplify how certain "list" data is cleared, when importing to Rattail.


0.9.148 (2020-10-13)
--------------------

* Log warning instead of assertion error, if runas_user doesn't exist.

* Stop trying to use win32 api to know "default config paths".

* Stop creating separate 'batch' folder for ``rattail make-appdir``.

* Allow datasync to export to rattail but *not* record changes.


0.9.147 (2020-10-02)
--------------------

* Fix how record associations are removed for rattail importing.

* Load "runas user" into current session, for X -> Rattail importers.

* Make sure model extension tables are eagerly joined for Rattail importing.


0.9.146 (2020-09-24)
--------------------

* Add methods to create new sheet, and toggle grid lines for ExcelWriter.

* Add "summary" sheet to Excel-based reports.


0.9.145 (2020-09-22)
--------------------

* Use static default timezone for new 'fabric' project.

* Add more flexible "extensions" mechanism for Rattail model importers.

* Turn on display of rattail deprecation warnings by default.


0.9.144 (2020-09-19)
--------------------

* Small tweaks for default config in 'fabric' projects.

* Allow overriding column header labels when writing Excel file.

* Add ``makedirs`` kwarg for ``Batch.absolute_filepath()`` method.

* Add batch handler methods for writing, updating from worksheet.

* Give importer diff emails an automatic default subject.

* Add ``--no-password`` flag for ``rattail make-user`` command.


0.9.143 (2020-09-16)
--------------------

* Always create 'data' dir when making app dir.

* Add support for generating a 'fabric' project.


0.9.142 (2020-09-14)
--------------------

* Add basic handler/template for generating new custom projects.


0.9.141 (2020-09-02)
--------------------

* Ignore bad UPC when reading products from file for label batch.

* Add ``Product.average_weight`` to schema.


0.9.140 (2020-08-21)
--------------------

* Add ``--skip-if-empty`` flag for ``rattail run-n-mail`` command.

* Add base classes for Rattail -> Rattail (local) imports.

* Always try to set ``runas_user`` etc. when making an importer.

* Allow override of header row for CSV exporters.

* Add base data model for "shopfoo" pattern.

* Add base pattern logic for Shopfoo data export.


0.9.139 (2020-08-17)
--------------------

* Add ``rattail version-check`` command, for consistency checks.


0.9.138 (2020-08-13)
--------------------

* Include alt code lookup for inventory "quick entry" logic.

* Fix how we obtain local system title for importers.


0.9.137 (2020-08-10)
--------------------

* Add ``PricingBatchRow.old_true_margin`` column to schema.

* Tweak how/when we set "manually priced" status for pricing batch rows.

* Add basic TXT template for user feedback emails.

* Grow column for permission name.


0.9.136 (2020-08-09)
--------------------

* Always import the data model module early, when running commands.

* Add new base classes for customer order/item models.

* Add data models for "customer order" batches.

* Add ``first_email()``, ``first_phone()`` etc. for ContactMixin.

* Fix some encoding bugs on python 2.

* Add association proxy for ``Employee.users``.


0.9.135 (2020-07-30)
--------------------

* Add base classes for "purging" subcommands.


0.9.134 (2020-07-29)
--------------------

* Add ``BatchHandler.delete_extra_data()`` method.

* Add ``BatchHandler.do_delete()`` method.


0.9.133 (2020-07-29)
--------------------

* Be smarter about deleting rows, when deleting batch.


0.9.132 (2020-07-28)
--------------------

* Tweak logic for purging batches to avoid warnings, duplicate progress.


0.9.131 (2020-07-26)
--------------------

* Grow ``Product.item_id`` to allow 50 chars.

* Don't create empty department, when importing subdepartment.

* Remove unused "fablib" line from manifest.

* Let config define arbitrary kwargs for datasync watcher.

* Add ``can_delete_object()`` method for importers.

* Add ``cache_model()`` convenience method for problem reports.

* Log info instead of debug, to show count of problems found.


0.9.130 (2020-06-18)
--------------------

* Remove 'fixture' use within tests; plus fix some tests.

* Add ``email_output()`` method for report handler, plus common template.


0.9.129 (2020-05-28)
--------------------

* Add ``require`` kwarg for ``Person.only_customer()`` method.

* Add some indexes, to optimize profile view.


0.9.128 (2020-05-20)
--------------------

* Add "shelved" flag for pricing batches.

* Add "safe" param logic for decimal report params.


0.9.127 (2020-04-17)
--------------------

* Add support for extra header rows, for Excel reader.

* Add generic ``FromFile`` importer base class.

* Change method call to allow for simpler signature.


0.9.126 (2020-04-06)
--------------------

* Fix how we assign ``Purchase.total`` when executing an ordering batch.

* Improve logic for making new Receiving batch from PO.

* Copy PO total from purchase object, when making new receiving batch.

* Add ``--borg-tag`` arg for ``rattail backup`` command.

* Add ``Product.get_default_pack_item()`` convenience method.

* Add ``Role.notes`` field to schema.

* Add way for report to provide available "choices" for any param.

* Add ``get_output_filename()`` method for ToFile exporters.

* Move most of inventory batch logic into the handler (from Tailbone).

* Add setting to disable old/legacy jQuery mobile app.


0.9.125 (2020-03-18)
--------------------

* Sever the "backref" tie for ``Person._customers``.

* Add setting for display of POD images in Tailbone.

* Add ``revoke_permission()`` convenience auth function.

* Fix the Subdepartment importer per real-time datasync use.

* Stash a reference to handler instance, when creating datasync consumer.

* Add "customer fields" for Person importer.

* Add ``ContactMixin`` for Rattail importers; use with Customer and Person.

* Declare the Member model to be a "contact" for related magic.

* Add version importers for member data.

* Add ``Member.number`` to schema.

* Add ``Customer.first_person()`` convenience method.


0.9.124 (2020-03-11)
--------------------

* Add logic for Order Form worksheet, in purchase batch handler.


0.9.123 (2020-03-05)
--------------------

* Add ``refresh_many()`` method for batch handlers.

* Raise explicit error in ``data_diffs()`` to tell which side is missing data.

* Add default implementation logic for ``Importer.cache_local_data()``.

* Fix some math/logic for calculating "pending" amounts in purchase batch.


0.9.122 (2020-03-02)
--------------------

* Grow ``item_entry`` field for batches, to accommodate product_uuid.


0.9.121 (2020-03-01)
--------------------

* Stop breaking on bad input, for purchase batch ``update_row_quantity()``.

* Delete each row in batch, one by one, when deleting batch.

* Add ``Employee.sorted_history()`` and improve ``get_current_history()``.

* Implement ``GPC.__lt__()`` rich comparison.


0.9.120 (2020-02-26)
--------------------

* Add ``update_row_quantity()``, ``order_row()`` methods for purchase batch handler.

* Update the *calculated* PO total when removing row from ordering batch.

* Add 60-second delay for "datasync wait" logic in Luigi overnight tasks.


0.9.119 (2020-02-21)
--------------------

* Tweak how output of ``rattail runsql`` command is handled.


0.9.118 (2020-02-19)
--------------------

* Let config define ``--keep-*`` args for ``borg prune`` command.

* Use progress when writing rows to Excel.


0.9.117 (2020-02-12)
--------------------

* Add new ``ProblemReportEmail`` base class, for simpler email previews.

* Add "current price" to schema for pricing batch; populate on refresh.

* Add support for newer file format, in KeHE invoice parser.


0.9.116 (2020-02-03)
--------------------

* Remove ``__future__`` imports from project scaffold template.

* Fix some password prompts, for python 3.

* Add some custom tables, model importers, web views for new project template.

* Don't consult the DB when fetching configured enum module.


0.9.115 (2020-01-28)
--------------------

* Allow populating a new pricing batch from products with "SRP breach".

* Remove versioning workarounds for core batch handlers.

* Add "invalid address" flags for primary contact types.

* Add "price breaches SRP" status for pricing batch rows.


0.9.114 (2020-01-20)
--------------------

* Add awareness of default "importer" batch handler.

* Explicitly avoid data versioning when executing import/export batch.

* Improve "batch" awareness for datasync queue logic.

* Add ``ProblemReportHandler.progress_loop()`` convenience method.


0.9.113 (2020-01-07)
--------------------

* Fix how "current" price is set for Product importer.


0.9.112 (2020-01-06)
--------------------

* Fix handling of tpr/sale prices for rattail Product datasync.


0.9.111 (2020-01-06)
--------------------

* Remove TPR, sale price refs from *simple* Product importer fields.


0.9.110 (2020-01-06)
--------------------

* Add ``Product.tpr_price`` and ``sale_price``, tweak model importer.


0.9.109 (2020-01-02)
--------------------

* Mark a Product as dirty, when ProductCost is deleted.

* Remove cascade settings for ``Person._customers`` relationship.


0.9.108 (2019-12-19)
--------------------

* Allow config to define datasync "batch" size limit.


0.9.107 (2019-12-02)
--------------------

* Add logic for updating row invoice cost/totals for receiving batch.

* Add catalog unit cost, confirmation flags for receiving batch rows.

* Add logic for updating catalog cost for receiving batch row.

* Add ``receiving_complete`` flag for PurchaseBatch.


0.9.106 (2019-11-15)
--------------------

* Add ``quick_entry()`` method signature for batch handlers.

* Try to set creator of new batch, if user is specified.

* Try to assign configured store when making new purchase batch.

* Add ``get_eligible_purchases()`` method for 'purchase' batch handler.

* Add proper "quick entry" logic for purchase batch.

* Fix some receiving row logic when null quantities present.


0.9.105 (2019-11-08)
--------------------

* Cascade delete for ProductStoreInfo.

* Add ``rattail make-batch`` command.

* Add ``finalize_session()`` convenience method for Subcommand.


0.9.104 (2019-10-30)
--------------------

* Fix issue with import diff email template, when extra fields present.

* Only retain "used importers" if instructed, in import handler.


0.9.103 (2019-10-25)
--------------------

* Add ``rattail purge-versions`` command.


0.9.102 (2019-10-23)
--------------------

* Add setting to "force unit item" for inventory batch.

* Add "generic" sequence for customer numbers.


0.9.101 (2019-10-15)
--------------------

* Add way for callers to assign "comment" for versioning transaction.

* Add ``-m`` flag option for ``rattail import-versions --comment``.


0.9.100 (2019-10-12)
--------------------

* Improve importer logic for "Global" objects, for sake of datasync.

* Add generic JSON ``params`` field to core batch schema.

* Make pricing batch population more robust for UPC/product.

* Add unit cost diff percentage for vendor catalog batch rows.

* Add "preferred vendor" flags for vendor catalog batch rows.

* Add unit cost diff, related status for vendor invoice batch rows.

* Add initial "problem report" framework.

* Use OrderedDict for configured db engines.


0.9.99 (2019-10-07)
-------------------

* Tweak Luigi summary filter logic for detecting "all good" message.

* Add ``local_only`` flag for Person, User, plus "Global" importers.


0.9.98 (2019-10-04)
-------------------

* Add ``remove_email()`` etc. for ContactMixin.

* Provide default/fallback node title for importers' sake.


0.9.97 (2019-10-02)
-------------------

* Declare 'sys' to be a built-in mysql db name, for ``rattail backup``.

* Add ``--groups`` arg to ``rattail make-user`` command.

* Add ``WarnSummaryIfProblems`` logging filter for Luigi.

* Provide default app title when generating mail.

* Convert command output to Unicode, for ``run-n-mail``.


0.9.96 (2019-09-24)
-------------------

* Add ``util.simple_error()`` for basic rendering of error message.

* Add ``default_importers_only`` flag for datasync consumers.

* Add progress support for some Excel writer methods.


0.9.95 (2019-09-18)
-------------------

* Strip whitespace from fieldnames by default, for ``ExcelReader``.

* Don't try to locate product if empty "entry" provided, for batch handlers.

* Add ``get_product_by_scancode()`` API function; leverage in batch handler.


0.9.94 (2019-09-17)
-------------------

* Add ``--dump-tables`` arg for ``rattail backup`` command.

* Add support for Borg backups, in ``rattail backup``.

* Add 'backup' requirements extra.

* Allow config to define where db dumps go for backup.

* Retain reference to "used" importer instances, when running via handler.

* Add ``ImportHandler.extra_importer_kwargs`` and associated logic.


0.9.93 (2019-09-10)
-------------------

* Add basis for a ``trainwreck prune`` command, to prune old data.


0.9.92 (2019-09-09)
-------------------

* Make sure new projects declare support for Python 3 (only).

* Remove some web templates from project scaffold.

* Make the Customer model use ContactMixin.

* Preserve "zeroes" when converting handheld batch to inventory batch.

* Check existence of ``psql`` command before using it, for backups.


0.9.91 (2019-08-04)
-------------------

* Add ``ContactMixin`` class to consolidate handling of phone/email/address.


0.9.90 (2019-07-30)
-------------------

* Add "from same to same" importer base class.

* Add basic support for Trainwreck <-> Trainwreck import/export.

* Add support for ``rattail export-csv`` command.

* Change progress message when caching local data for importer.

* Add basic support for ``rattail import-csv`` command.


0.9.89 (2019-07-13)
-------------------

* Add ``Employee.only_person()`` convenience method.


0.9.88 (2019-07-09)
-------------------

* Add ``RattailConfig.datadir()`` convenience method.

* Stop using deprecated RattailConfig methods.

* Fix main version query, to remove duplicate results.


0.9.87 (2019-06-16)
-------------------

* Allow session to define client IP address for data versioning.


0.9.86 (2019-06-13)
-------------------

* Copy item ID and UPC when refreshing row for pricing batch.

* Fix WinCE batch file parsing per python 3.

* Add ``po_total_calculated`` columns for purchasing batch, row.


0.9.85 (2019-05-09)
-------------------

* Add ``cache_model()`` convenience method for reports.


0.9.84 (2019-05-09)
-------------------

* Store report type key and params when generating new report.

* Add support for "totals" row to basic Excel report output.


0.9.83 (2019-05-07)
-------------------

* Add generic ``ExcelReport`` base class.


0.9.82 (2019-05-05)
-------------------

* Add basic support for custom number formats, in Excel writer.


0.9.81 (2019-04-30)
-------------------

* Add ``--kwargs`` argument for batch execution command line.


0.9.80 (2019-04-26)
-------------------

* Remove redundant setup when populating vendor catalog batch.

* Assign continuum versioning author when executing any batch.


0.9.79 (2019-04-25)
-------------------

* Comment out app_title in base_meta for new project template.

* Add 'newproduct' batch for importing new items from e.g. spreadsheet.

* Add "allowance" fields for Vendor Catalog batches.

* Add vendor item code, family code etc. for pricing batch.

* Add generic "products" batch type, can convert to labels or pricing batch.

* Fix data encoding when writing to progress socket for python3.


0.9.78 (2019-04-12)
-------------------

* Add ``Employee.get_current_history()`` convenience method.


0.9.77 (2019-04-04)
-------------------

* Let handler create importers for datasync consumer.


0.9.76 (2019-04-04)
-------------------

* Make sure importer knows "direction" when used within datasync.


0.9.75 (2019-04-03)
-------------------

* Remove deprecated web menu template in new project template.

* Set importer ``direction`` early, in case ``supported_fields`` needs it.


0.9.74 (2019-04-02)
-------------------

* Use "shipped" instead of "ordered" for truck dump child row "claims".

* Use shipped instead of ordered, for setting purchase batch row status.


0.9.73 (2019-03-29)
-------------------

* Some improvements to basic project template.

* Add new 'reporting' mini-framework.

* Allow "loose" product matching between truck dump parent and child.

* Add ``can_declare_credit()`` method for purchase batch handler.


0.9.72 (2019-03-21)
-------------------

* Add simple ``JSONTextDict`` data type for SQLAlchemy columns.


0.9.71 (2019-03-14)
-------------------

* Add ``BatchHandler.do_remove_row()`` caller method.

* Omit deprecated kwarg for ``session.is_modified()``.

* Add ``direction`` attribute for ImportHandler and Importer.

* Add debug logging when "stale changes" detected for datasync.

* Add ``declare_credit()`` method for purchase batch handler.


0.9.70 (2019-03-11)
-------------------

* Fix progress bar construction (for real).

* Add ``percentage`` kwarg to ``pricing.gross_margin()`` function.

* Add ``ProductVolatile`` model, for "volatile" product attributes.

* Tweak ``pretty_hours()`` to better handle negative values.


0.9.69 (2019-03-08)
-------------------

* Fix logic for calculating "credit total".

* Add "calculated" invoice total for receiving row, batch.

* Fix how some "receive row" logic worked, for aggregated product rows.

* Expand UPC-E to UPC-A when doing product receiving lookup.


0.9.68 (2019-03-07)
-------------------

* Fix progress bar error, as of ``progress==1.5`` package.


0.9.67 (2019-03-06)
-------------------

* Tweak how we create config parser object, for python 3 vs. 2.

* Refresh receiving batch after "auto-receiving" all items.

* Add ``mark_complete()`` and ``mark_incomplete()`` methods for batch handler.

* Add some basic docs for "product receiving" features.

* Add first implementation of ``receive_row()`` for purchase batch handler.

* Add "truck dump status" fields for purchase batch, row.

* Make "auto receive all" logic smarter, to handle split cases.

* Don't raise error if "removing" a batch row which was already "removed".

* Auto-create "missing" credits for product not accounted for, when receiving.


0.9.66 (2019-02-25)
-------------------

* Tweak CSV parsing for new handheld batch, per python3.


0.9.65 (2019-02-22)
-------------------

* Aggregate when adding truck dump child row already present in parent.

* Clean up Rattail <-> Rattail import/export handlers a bit.

* Add ``Customer.add_mailing_address()`` convenience method.

* Add ``CustomerNote`` and ``Customer.notes``.

* Add setting for whether 'vendor' fields should use autocomplete or dropdown.


0.9.64 (2019-02-14)
-------------------

* Refactor datasync consumer logic, for prettier email and retry support.

* Remove some old handler-less logic for emails.

* Add ``include_fields()`` and ``exclude_fields()`` importer methods.


0.9.63 (2019-02-12)
-------------------

* Fix help bug for ``export-rattail`` command.

* Add ``time.first_of_year()`` convenience function.

* Add ``--year`` arg for importer subcommands.

* Add convenience method ``Person.only_customer()``.


0.9.62 (2019-02-08)
-------------------

* Allow suppression of stderr from ``pip freeze`` when running upgrade.

* Introduce some new logic for "children first" truck dump receiving.

* Don't overwrite PO, invoice cost for purchase batch row upon refresh.


0.9.61 (2019-02-05)
-------------------

* Add "node title" app setting.

* Add support for importing member, member contact data.

* Add ``config.node_type()`` convenience method.

* Add app setting for background color.


0.9.60 (2019-01-31)
-------------------

* Improve logic for default ``repr(ModelBase)`` output.


0.9.59 (2019-01-28)
-------------------

* Tweak logic for fetching "runas user".


0.9.58 (2019-01-24)
-------------------

* Fix invoice parser for Albert's, per python3.


0.9.57 (2019-01-22)
-------------------

* Tweak contrib UNFI invoice parser, for python3 support.


0.9.56 (2019-01-21)
-------------------

* Accept hours as decimal instead of delta, for ``util.pretty_hours()``.

* Add python3 support for contrib KeHE vendor invoice parser.

* Tweak some label printing logic to support python 3.


0.9.55 (2019-01-17)
-------------------

* Add app settings for restart commands, for datasync/filemon daemons.

* Add generic ``rattail run-n-mail`` command.


0.9.54 (2019-01-10)
-------------------

* Add ``extra_data`` text column to all batch tables.

* Always refresh TD parent batch row, when transforming pack to unit.


0.9.53 (2019-01-08)
-------------------

* Grow markup field for pricing batch rows, ever so slightly.


0.9.52 (2019-01-05)
-------------------

* Always set "runas" user when making DB session for command.


0.9.51 (2019-01-01)
-------------------

* Tweak logging if duplicate keys found when making cache.

* Add basic Member table.


0.9.50 (2018-12-19)
-------------------

* Fix product version schema, for last migration.


0.9.49 (2018-12-19)
-------------------

* Grow ``Product.uom_abbreviation`` field to allow 10 chars.


0.9.48 (2018-12-19)
-------------------

* Add basic support for making new pricing batch from input file.

* Add subdepartment to core "product" batch row mixin schema.

* Add "label profile" field for label batches.

* Add way to declare label type for new label batch from data file.


0.9.47 (2018-12-12)
-------------------

* Refactor how we read some config values for datasync.


0.9.46 (2018-12-11)
-------------------

* Fix population logic when making batch from file via filemon.


0.9.45 (2018-12-05)
-------------------

* Add ``Object.setdefault()`` method.

* Add way to extend available types, for ``rattail make-config``.

* Add "sync me" flag to LabelProfile model, honor it within importers.

* Overhaul datasync consumer thread logic a bit.

* Add clue for checking perms, when pruning non-existing filemon folder.


0.9.44 (2018-12-02)
-------------------

* Add some default magic for importers reading from CSV file.

* Coerce generic import batch row keys to string, for description.

* Add ``rattail datasync check-watchers`` subcommand.

* Add basic "min % diff" logic for pricing batches.

* Grow some "margin" columns in pricing batch row table.

* Allow override of decimal places when converting hours.

* Tweak some label batch logic per python3.

* Add ``old_price_margin`` column for pricing batch rows.

* Update sample config and new project template.


0.9.43 (2018-11-19)
-------------------

* Tweak how we assign 'runas' user for commands.


0.9.42 (2018-11-19)
-------------------

* Add ``rattail purge-batches`` command.

* Add ``Customer.wholesale`` flag.

* Add ``suggested_price``, ``margin_diff``, ``price_diff_percent`` for pricing
  batch rows.


0.9.41 (2018-11-14)
-------------------

* Grow column for ``Role.name`` to 100 chars.

* Add "suggested price" hack for old-style rattail -> rattail datasync.


0.9.40 (2018-11-09)
-------------------

* Add index for trainwreck ``Transaction.receipt_number``.


0.9.39 (2018-11-09)
-------------------

* Add ``product_suggested_price`` field for ProductPrice model importer.


0.9.38 (2018-11-08)
-------------------

* Detect non-numeric entry when locating row for purchase batch.

* Add setup/teardown to handler, for batch populate.

* Add "suggested price" features for Product model, importer.


0.9.37 (2018-11-07)
-------------------

* Add "current discount" fields for ``ProductCost`` model.

* Add "true" unit cost, margin to pricing batch rows.

* Add client IP address to user feedback email.


0.9.36 (2018-10-25)
-------------------

* Add simple ``datasync check`` command.


0.9.35 (2018-10-24)
-------------------

* Add ``required`` flag for app settings.

* Add ``transform_pack_to_unit()`` method for purchase batch handler.


0.9.34 (2018-10-19)
-------------------

* Preserve "raw" data record when parsing KeHE invoice file.

* Add probe status for "critical low temp".


0.9.33 (2018-10-17)
-------------------

* Use builtin ``csv.DicReader`` if running on python3.

* Add ``cache_permissions()`` function to ``db.auth`` module.

* Add link to the upgrade, within upgrade success/failure emails.


0.9.32 (2018-10-11)
-------------------

* Fix "off by one" error in SIL writer.

* Use built-in ``csv.writer`` instead of custom one, for python3.


0.9.31 (2018-10-09)
-------------------

* Never record change for ``EmailAttempt``.

* Move the ``filename_column()`` function to ``rattail.db.core`` module.

* Refactor SIL writer a bit, per newer conventions.


0.9.30 (2018-10-03)
-------------------

* Add enum for tempmon disk type.

* Rewrite truck dump claiming logic for purchase batch.


0.9.29 (2018-09-26)
-------------------

* Don't allow NULL for batch ``complete`` flags.

* Add ``item_entry`` field to all product-related batch rows.

* Try to locate product by vendor item code before alt code, for purchase batch.

* Add ``locate_product_for_entry()`` method for purchase batch handler.

* Add basic "out of stock" awareness for vendor invoices, receiving.


0.9.28 (2018-09-20)
-------------------

* Let caller decide whether to auto-create departments for category import.


0.9.27 (2018-09-20)
-------------------

* Make sure we create unit item before the pack which references it.

* Add ``locate_product()`` method for 'purchase' batch handler.

* Prefer truck dump child row over parent, wrt case_quantity.

* Add app setting to show/hide product images for mobile purchasing.

* Add new "partially claimed" status for truck dump parent batch rows.


0.9.26 (2018-08-24)
-------------------

* Add new "quick receive" settings for mobile receiving.

* Increase size of ``Category.code`` to 20 chars.


0.9.25 (2018-08-14)
-------------------

* Various tweaks for refresh of receiving batch.

* Add ``PurchaseBatchRowClaim.is_empty()`` convenience method.

* Add backref for ``ProductCost._vendor_catalog_rows``.

* Add ``OvernightTask`` for use with overnight automation via Luigi.

* Add app setting for mobile products "quick lookup".

* Add support for ``product_item_id`` field in ProductCost importer.

* Claim 'expired' credits when adding child invoice to truck dump parent.


0.9.24 (2018-07-31)
-------------------

* Configure data versioning within ``make_config()``.


0.9.23 (2018-07-29)
-------------------

* Fix ``str(Message)`` when subject contains unicode chars.


0.9.22 (2018-07-26)
-------------------

* Allow consulting the db for core 'product_key' setting.

* Define some settings for purchasing / receiving.


0.9.21 (2018-07-19)
-------------------

* Add ``api.get_product_by_item_id()`` convenience function.

* Add ``RattailConfig.product_key()`` and ``product_key_title()``.

* Fix batch row count when removing row from batch.

* Various tweaks to purchase batch handler logic.

* Let config define a "not found" product image URL.

* Add ``PurchaseBatch.order_quantities_known`` and ``is_truck_dump_parent()`` etc.

* Add basic ``settings`` module.

* Tweak how we copy product key, do lookup for some receiving batches.

* Send email when upgrade is performed, whether success or failure.


0.9.20 (2018-07-11)
-------------------

* Allow sync of ``unit_uuid`` for Rattail -> Rattail ProductImporter.

* Add generic ``--verbose`` arg for all commands.

* Add ``modified`` timestamp to all batch rows.

* Refactor truck dump "claiming" a bit, add "case quantity differs" status.

* Fix logic for purchase batch ``calc_best_fit()``.

* Don't allow execute of truck dump parent batch until fully claimed by children.

* Increase size of source, consumer fields for datasync change.

* Add customization hook for datasync consumer when fetching local object.


0.9.19 (2018-07-09)
-------------------

* Grow size of ``total_cost`` field for inventory batch rows.


0.9.18 (2018-07-06)
-------------------

* Add new ``backup`` command.

* Add generic ``silent.conf`` config file.

* Defer some imports, to avoid errors when sqlalchemy not installed.


0.9.17 (2018-07-03)
-------------------

* Add ``Product.default_pack``, plus ``is_unit_item()`` and ``is_pack_item()``.


0.9.16 (2018-07-03)
-------------------

* Add customization flags for rattail's Product importer, category fields.

* Add basic support for "command line" filemon action.

* Add setup/teardown handler hooks when cloning a batch.


0.9.15 (2018-07-01)
-------------------

* Add some customization flags for rattail's Product importer.


0.9.14 (2018-06-28)
-------------------

* Fix bug when setting status text for vendor catalog row.

* Allow user to overwrite unit cost for inventory batch rows.

* Show subcommand help as early as possible (avoid logging).

* Add ``credit_total`` field for (batch) purchase credits.

* Add "non-creditable" status for purchase credit.

* Allow refresh for 'completed' batch, by default.


0.9.13 (2018-06-18)
-------------------

* Add ``--max-diffs`` arg for importer commands.


0.9.12 (2018-06-18)
-------------------

* Add ``rattail.time.get_monday()`` convenience function.

* Add index on ``upload_time`` for Trainwreck transaction table.


0.9.11 (2018-06-14)
-------------------

* Fix bug when ``--max-delete`` used for importer commands.

* Cache categories by code instead of number.

* Add ``ExcelWriter.auto_resize()`` method.

* Add ``exempt_from_gross_sales`` flag for department and trainwreck line item.


0.9.10 (2018-06-09)
-------------------

* Add ``update-costs`` command for making future costs become current.

* Add ``Customer.one_person()`` convenience method.


0.9.9 (2018-06-07)
------------------

* Set continuum username for all datasync watchers, if present.

* Allow config to force the ``To:`` address for all generated emails.

* Don't record changes for any model ending in 'Version'.

* Add versioning workaround support for batch actions.


0.9.8 (2018-06-04)
------------------

* Add 'hidden' flag for inventory adjustment reasons.

* Add ``Vendor.abbreviation`` to schema.

* Add "null" datasync consumer.

* Add ``normalize_lastrun()`` convenience method for datasync watchers.

* Make some importers smarter when dealing with NULL primary key values.


0.9.7 (2018-05-30)
------------------

* Add initial support for "variance" inventory batch mode.


0.9.6 (2018-05-25)
------------------

* Add ``RattailConfig.single_store()`` convenience method.

* Add ``BatchHandler.remove_row()`` method.

* Improve default handler logic for purchase batches.

* Add "most of" support for truck dump receiving.

* Add ``runsql`` command, mostly for dev use.

* Add ``--key`` arg for importer commands.


0.9.5 (2018-04-12)
------------------

* Add ``ProductFutureCost`` table, future mode for vendor catalog batch.


0.9.4 (2018-04-09)
------------------

* Tweak some product relationships so can delete a product.

* Tweak how product cost is imported, when new records involved.

* Add ``strip_fieldnames`` kwarg to ``ExcelReader`` constructor.

* Prevent aggressive flush when making purchase from ordering batch.

* Add ``Email.dynamic_to`` flag, to improve admin config UI.

* Use common product mixin for ``VendorCatalogRow`` model.

* Add new status options for vendor catalog rows, tie back to existing cost.


0.9.3 (2018-03-12)
------------------

* Add ``vendor_item_code`` field to purchase credit records.

* Make ``rattail.csvutil.UnicodeReader`` => ``csv.reader`` for python3.


0.9.2 (2018-02-27)
------------------

* Return new batches from ``ImportHandler.make_batches()``.

* Add ship_method, notes_to_vendor for Purchase, PurchaseBatch.

* Don't consider a batch refreshable if it's marked complete.

* Add ``get_email()`` convenience methods to Vendor model.

* Add email attachment MIME type for MS Word .doc files.

* Remove ``rattail.fablib`` subpackage.

* More tweaks for python 3.


0.9.1 (2018-02-15)
------------------

* More tweaks for python 3.

* Set row count when cloning batch.


0.9.0 (2018-02-14)
------------------

* Misc. cleanup for Python 3.

* Ditch older 'progressbar' for newer 'progress' package.

* Remove FormEncode dependency.

* Add 'bcrypt' dependency; remove 'py-bcrypt' for auth.

* Add 'six' to context when rendering email templates.

* Refactor sample web view for new batch, per master changes.

* Add some python3 awareness when installing mod_wsgi.


0.8.55 (2018-02-08)
-------------------

* Optionally suppress warning from psycopg2 about their packaging changes.


0.8.54 (2018-02-07)
-------------------

* Add way to "force versioning" when making new migrations.

* Add 'force' kwarg to ``pod.render_document()``.

* Add ``EmailHandler`` logic, with support for recording ``EmailAttempt``.

* Add "(dry run)" to import logging summary, when applicable.

* Add support for ``pool_pre_ping`` config, for SQLAlchemy engines.

* Copy "safe MIME text" email encoding workaround from Django.


0.8.53 (2018-01-31)
-------------------

* Fix some logging for "bulk" import handlers.

* Tweak how rattail import handler makes its session.


0.8.52 (2018-01-29)
-------------------

* Allow override of most kwargs when sending email.

* Don't supply price from batch when printing labels, unless "static prices".

* Add ``Brand.confirmed`` and unique constraint for ``name``.

* Add basic ``ExcelWriter`` class, plus xlrd and openpyxl dependencies.


0.8.51 (2018-01-24)
-------------------

* Add index to Trainwreck item table, for ``transaction_uuid``.

* Add ``cashback`` field to Trainwreck transaction.


0.8.50 (2018-01-16)
-------------------

* Add some MIME magic for CSV attachments when sending email.

* Don't use DB as fallback when determining data model.

* Add ``case_cost`` property for inventory batch rows.

* Let db config keys be defined as arbitrary list.

* Add install logic for certbot on debian 9.

* Allow certbot to be installed from source, even if package is available.


0.8.49 (2018-01-07)
-------------------

* Add model, importer for InventoryAdjustmentReason.

* Let label batch provide product prices when executing.

* Make ``BatchHandler.execute_many()`` responsible for setting execution details.

* Assume MariaDB is *not* of concern, by default.

* Make ``~/.ssh`` by default, when bootstrapping rattail.

* Add ``postgresql.create_schema()`` fab function.

* Add ``util.get_object_spec()`` convenience function.

* Add first attempt for "importer as batch" feature.


0.8.48 (2018-01-04)
-------------------

* Add ``Product.price_required`` flag to schema.

* Grow cost columns for vendor catalog batches.


0.8.47 (2017-12-19)
-------------------

* Add ``Customer.employee`` convenience property.

* Add ``Person.first_valid_email()`` convenience method.


0.8.46 (2017-12-08)
-------------------

* Add suggested retail for vendor catalog batches.

* Add logging filter for Luigi task summary.


0.8.45 (2017-12-05)
-------------------

* Use bytestring with ``getpass()``.


0.8.44 (2017-12-03)
-------------------

* Add ``Transaction.system_id`` for Trainwreck.


0.8.43 (2017-12-03)
-------------------

* Add "manually priced" flags for price batch.

* Add basic "auto-execute" logic for new batches created via filemon.

* Add "extension" support for all Rattail importers.

* Add way to set label batch description, notes from input data file.

* Add basic "static prices" support for label batches.

* Allow label batches to exist without a "label profile".

* Add default "execute many" behavior for batch handlers.

* Skip some (more) incomplete rows when printing label batch.


0.8.42 (2017-11-19)
-------------------

* Add port for postgres commands, let env define "workon home" for fabric.

* Add init script for Luigi scheduler daemon.

* Add base class for importer diff emails.


0.8.41 (2017-11-12)
-------------------

* Coerce fields to proper list, for importer commands.


0.8.40 (2017-11-12)
-------------------

* Allow specifying sheet by name when creating ExcelReader.

* Add "re-populate on refresh" flag for batch handlers.

* Add support for ``--fields`` and ``--exclude-fields`` importer cmd line args.

* Add ``commit`` flag for ``short_session()``.

* Add ``time.date_range()`` convenience function.


0.8.39 (2017-11-10)
-------------------

* Switch to ``passlib`` for password hashing and verification.

* Add generic ``util.data_diffs()`` function.

* Add ``BatchHandler.cache_model()`` convenience function.


0.8.38 (2017-11-02)
-------------------

* Add ``end_time`` index for Trainwreck transactions

* Add index on ``item_id`` for Trainwreck line items


0.8.37 (2017-11-01)
-------------------

* Add personnel and product flags for Department

* Add convenience for parsing date in Excel reader


0.8.36 (2017-10-29)
-------------------

* Add ``make_username()`` api function


0.8.35 (2017-10-28)
-------------------

* Add cashier ID, name to trainwwreck transaction schema


0.8.34 (2017-10-27)
-------------------

* Delete UserEvent records when parent User is deleted

* Fix setup.py in project template, to include package data by default


0.8.33 (2017-10-26)
-------------------

* Let ``authenticate_user()`` function accept a user object *or* username

* Make rattail <-> rattail datasync use topographic sort


0.8.32 (2017-10-25)
-------------------

* Add speedup for rattail -> rattail AdminUser imports

* Make rattail <-> importers and dataysnc more flexible

* Improve the ``upgrade`` command, to allow better automation


0.8.31 (2017-10-24)
-------------------

* Fix encoding issue when sending email


0.8.30 (2017-10-24)
-------------------

* Add ``item_id`` to Trainwreck schema, rename ``item_scancode``

* Add index on trainwreck ``Transaction.start_time``

* Add ``User.last_login`` to schema

* Add ``Person.users`` relationship

* Make sending email more configurable


0.8.29 (2017-10-19)
-------------------

* Add better str() methods for contact models

* Add 'using' db key when importing from Django

* Add generic datasync consumer for Rattail -> Rattail export

* Let ``time.previous_month()`` calculate arbitrary number of months

* Add versioned models, importers for EmployeeHistory, Note

* Add ``upload_time`` to base Transaction table for trainwreck


0.8.28 (2017-09-29)
-------------------

* Grow size of ``total_cost`` column for inventory batches


0.8.27 (2017-09-28)
-------------------

* Don't auto-assign inventory batch count mode


0.8.26 (2017-09-28)
-------------------

* Add ``time.first_of_month()`` function

* Add basic ``ExcelReader`` class, for convenience..

* Add ``force_yes`` param to ``fablib.apt.install()``


0.8.25 (2017-09-15)
-------------------

* Add ``fablib.mysql.is_mariadb()`` to check for MariaDB

* Refactor ``fablib.python`` somewhat to allow for apt package installs

* Add ``deploy.local_exists()`` convenience method for fablib

* Add ``time.next_month()`` function

* Various importing tweaks...

* Add ``commands.list_argument`` for list-type args


0.8.24 (2017-08-20)
-------------------

* Fix phone_number_2 bug for Employee importer


0.8.23 (2017-08-18)
-------------------

* Fix more str() encoding bugs


0.8.22 (2017-08-18)
-------------------

* Update sample data and importer, per latest schema

* Add ``UpgradeHandler.do_execute()`` and ``mark_executing()``

* Fix ``str(Person)`` encoding bug


0.8.21 (2017-08-15)
-------------------

* Don't allow upgrade command to be specified in Settings table

* Add ``UpgradeHandler.delete_files()`` method

* Add enum for purchase credit status


0.8.20 (2017-08-13)
-------------------

* Update project template to stop referencing 'better' tailbone theme


0.8.19 (2017-08-12)
-------------------

* Fix product price data gap for Rattail -> Rattail importer


0.8.18 (2017-08-11)
-------------------

* Add "zero-all" mode support for inventory batches


0.8.17 (2017-08-10)
-------------------

* Fix broken ``Person.user`` relationship


0.8.16 (2017-08-09)
-------------------

* Add batch descriptions, prev_on_hand for inventory batches, etc.


0.8.15 (2017-08-09)
-------------------

* Capture exit code from upgrade process, use it to indicate success/fail

* Provide default path for rattail sudoers file


0.8.14 (2017-08-08)
-------------------

* Specify ``expire_on_commit`` for rattail db sessions

* Add sample config for with/out versioning


0.8.13 (2017-08-08)
-------------------

* Add ``RattailConfig.get_model()``

* Add email settings for ``rattail import-versions``

* set default runas user for all importers targeting rattail

* add startup check to ensure continuum is functional (if enabled)


0.8.12 (2017-08-08)
-------------------

* Add ``RattailConfig.appdir()`` method

* Make ``RattailConfig.workdir()`` use ``require`` by default

* Improve status tracking for upgrades; add package diff

* Add basic API docs for ``rattail.upgrades`` and ``rattail.win32``


0.8.11 (2017-08-07)
-------------------

* Add common sudoers file for rattail

* Tweak how some batches are populated


0.8.10 (2017-08-07)
-------------------

* Add become/stop root user events to enum

* Add schema for tracking app upgrades

* Add ``rattail upgrade`` command


0.8.9 (2017-08-04)
------------------

* Add schema/enum for recording user events


0.8.8 (2017-08-04)
------------------

* Add ``Customer.active_in_pos_sticky`` flag


0.8.7 (2017-08-03)
------------------

* Update on-order inventory counts when creating new purchase

* Add ``rattail.batch.consume_batch_id()`` convenience function

* Fix str() for MailTemplateNotFound exception

* Add ``previous_month()`` and ``last_of_month()`` convenience functions

* Add ``Subcommand.make_session()`` method


0.8.6 (2017-07-26)
------------------

* Add basic support for native product inventory

* Add generic ``Product.status_code`` field

* Avoid session auto-flush when populating or refreshing a batch


0.8.5 (2017-07-14)
------------------

* Add versioning for products and everything else


0.8.4 (2017-07-14)
------------------

* Add custom status for purchasing batches


0.8.3 (2017-07-14)
------------------

* Add ``util.pretty_boolean()`` convenience function


0.8.2 (2017-07-13)
------------------

* Add ``complete`` flag to all batches

* Add generic reason code for inventory batches

* Add unit cost for inventory batches

* Provide default ``Person.display_name`` when importing customer data


0.8.1 (2017-07-07)
------------------

* Switch license to GPL v3 (no longer Affero)


0.8.0 (2017-07-06)
------------------

Main reason for bumping version is the (re-)addition of data versioning support
using SQLAlchemy-Continuum.  This feature has been a long time coming and while
not yet fully implemented, we have a significant head start.

* Refactored data versioning support! (contact tables only, for now)

* Add basic ``import-versions`` command, for "catching up" versions

* Add ``expect_duplicates`` kwarg to ``cache_model()``

* Add department_number support to Category model importer

* Tweak base ``Importer`` constructor, so ``model_class`` may be more dynamic
  
* Stop providing default value for ``Person.display_name``

* Add basic 'runas' support for datasync

* Replace usage of ``execfile()``

* Cleanup some unicode stuff per py3k effort


0.7.95 (2017-07-01)
-------------------

* Add ``Subcommand.progress_loop()`` convenience method

* Make ``Subcommand.get_runas_user()`` leverage args by default

* Add "magic" for Excel file attachments when sending email

* Add gross and net sales to Trainwreck items

* Install libreoffice-calc with headless soffice


0.7.94 (2017-06-26)
-------------------

* Move logic for refreshing handheld batch status


0.7.93 (2017-06-22)
-------------------

* Optimize local data cache slightly, for importers

* Cascade deletion for handheld / inventory/label batch associations


0.7.92 (2017-06-22)
-------------------

* Add fabric task for installing PHP Composer

* Add status code to (all) batch headers

* Keep track of row count when populating some batches (not yet complete)

* Refactor schema so label/inventory batch may come from multiple handheld batches

* Add way to execute handheld batch "search results", for inventory/label batch


0.7.91 (2017-06-19)
-------------------

* Fix encoding bug when setting user's password


0.7.90 (2017-06-14)
-------------------

* Always install 'six' when making new virtualenv

* Grow the item_type field for trainwreck line items

* Always encode password/salt before attempting auth login


0.7.89 (2017-05-30)
-------------------

* Remove all schema and logic for old-style batches


0.7.88 (2017-05-25)
-------------------

* Remove some deprecated batch handler methods

* Tweak new batch templates per newer conventions

* Add basic ``ProductStoreInfo`` to data model

* Remove all references to old importer frameworks


0.7.87 (2017-05-18)
-------------------

* Tweak product code importer, to detect and warn about unknown product

* Make ``apt dist-upgrade`` non-interactive

* Set ``ImportHandler.enum`` attribute based on config

* Add ``Customer.number`` and ``active_in_pos`` to schema

* Allow importing of ``Customer.person`` primary association

* Add basic support for ``importing.ToRattail.extension_fields``

* Tweak how SQLAlchemy-based importers fetch a single local object

* Add initial support for Trainwreck database

* Tweak ``fablib.postgresql.script()`` to allow running as arbitrary PG user

* Add ``Employee.full_time`` and ``full_time_start`` to schema


0.7.86 (2017-05-05)
-------------------

* Add ``all_fields`` flag to ``Importer.update_object()`` method


0.7.85 (2017-04-18)
-------------------

* Tweak mail template for user feedback, to wrap message body

* Accept a ``python`` arg for ``fablib.python.mkvirtualenv()``


0.7.84 (2017-03-30)
-------------------

* Add ``use_lists`` arg for ``cache.cache_model()``, plus ``CacheKeyNotSupported``

* Tweak constructor for base Importer class

* Add ``--daemonize`` arg to daemon commands: datasync, filemon, bouncer


0.7.83 (2017-03-29)
-------------------

* Tweak output of ``util.pretty_quantity()``

* Make first host data entry win, when duplicates detected in core importer

* Add ``rattail.upgrade_rattail_db()`` fablib function

* Add ``Importer.enum`` convenience attribute

* Add the ``User.active_sticky`` flag for smarter account sync

* Add way to suppress md5-related warning when we ``import appy``

* Add ``ProductCost.discontinued`` flag to schema

* Try to guess first/last name when making new rattail user via command line

* Fix some broken config in project template


0.7.82 (2017-03-25)
-------------------

* Add ``Product.item_id`` and ``item_type``, plus grow description fields

* Add support for importing product unit cost

* Add proper cancel support to base ``Importer`` class

* Add ``PurchaseItem.item_id`` field, ``PurchaseBatchHandler.ignore_cases`` flag


0.7.81 (2017-03-22)
-------------------

* Refactor new project template, to use variations of project name

* Provide default logo for Login page in new project template

* Refactor how/when mail aliases are created for new system users

* Add universal fablib function for cloning PostgreSQL database

* Add ``RattailConfig.demo()`` method

* Tweak deployment of Apache site, for better kwargs support

* Disable some unused commands

* Make ``filename`` arg optional for ``config.batch_filepath()``, ``export_filepath()``

* Tweak method signature for ``BatchMixin.absolute_filepath()``

* Add ``ExportMixin.filepath()`` convenience method

* Make ``util.pretty_hours()`` accept a ``seconds`` arg

* Make ``allow_cancel`` default to false, for ``util.progress_loop()``

* Add ``BatchHandler.populate()`` and ``should_populate()``

* Add ``ModelBase.make_proxy()`` class method

* Change ``BatchMixin.delete_data()`` method to remove entire folder

* Add ``mysql.clone_db()`` fablib function

* Add ``CustomerMailingAddress`` to data model

* Refactor core commands somewhat; add ``--runas`` arg

* Add ``errors`` kwarg to csv readers

* Add ``db.util.short_session()`` context manager

* Add ``poddoc`` module for basic appy.pod integration support

* Add basic ``ReportOutput`` data model

* Add basic 'soffice' daemon / fablib support for headless LibreOffice

* Add sane default handling of PDF attachments when sending email


0.7.80 (2017-03-16)
-------------------

* Don't assume datasync URL is configured, within email previews

* Fix logic for ``util.hours_as_decimal()``


0.7.79 (2017-03-15)
-------------------

* Add new BatchImporter for sake of product image and similar imports


0.7.78 (2017-03-13)
-------------------

* Add ``script()`` and ``set_user_password()`` to postgresql fablib

* Add ``default_dbkey`` for export-rattail commands


0.7.77 (2017-03-09)
-------------------

* Tweak how we exclude product images from rattail export

* Detect, warn about invalid cost in KeHE vendor catalog parser

* Fix ownership bug when uploading Mako template file via fabric

* Add 'identity' kwarg for fablib ``ssh.cache_host_key()``

* Use query.count() if no count provided to ``progress_loop()``


0.7.76 (2017-03-03)
-------------------

* Add ``Product.discontinued`` flag to schema


0.7.75 (2017-03-03)
-------------------

* Allow 'frontend' override for ``apt-get install`` via fabric

* Add ``allow_cancel`` kwarg for ``progress_loop()``


0.7.74 (2017-03-01)
-------------------

* Add product notes, ingredients to schema


0.7.73 (2017-02-24)
-------------------

* Add ``Role.session_timeout`` to schema

* Add notes column to BatchMixin

* Add some product flags (kosher, vegan etc.)

* Add basic ProductImage data model with importer

* Fix bug in ``len(QuerySequence)`` logic

* Add ``export-rattail`` command, plus ProductImage support for Rattail->Rattail


0.7.72 (2017-02-21)
-------------------

* Add initial data models for customer orders


0.7.71 (2017-02-17)
-------------------

* Fix str vs. unicode issue for Product model

* Restrict our version of flufl.bounce per its 3.0 release

* Add FreeTDS logging filter, to help cut down on unwanted email noise


0.7.70 (2017-02-16)
-------------------

* Fix str() methods for various data models


0.7.69 (2017-02-15)
-------------------

* Remove unwanted ``Object.__str__()`` method


0.7.68 (2017-02-14)
-------------------

* Add ``ExportMixin`` and file path getters on config object

* Add global ``NOTSET`` singleton

* Add ``User._messages`` backref for convenience


0.7.67 (2017-02-11)
-------------------

* Add ``pretty_hours()`` and ``hours_as_decimal()`` to ``util`` module


0.7.66 (2017-02-10)
-------------------

* Add ``ProductPrice.active_now()`` convenience method

* Make ``DepositLink.code`` a string

* Add special importer logic for '_deleted_' flag


0.7.65 (2017-02-09)
-------------------

* Add ``RattailConfig.get_store()`` convenience method

* Add unit/pack concept to Product schema, make ``Tax.code`` a string


0.7.64 (2017-02-03)
-------------------

* Add ``createdb`` flag for ``fablib.postgresql.create_user()``

* Add ``warn_only`` flag for ``fablib.ssh.cache_host_key()``

* Add vendor column to pricing batch rows

* Add ``User.is_admin()`` convenience method


0.7.63 (2017-01-30)
-------------------

* Add min diff threshold for pricing batches

* Add ``set_status_per_diff()`` for pricing batch handler


0.7.62 (2017-01-29)
-------------------

* Add ``postgresql.get_version()`` for fabric

* Only install emacs if it not yet installed

* Add basic support for cloning an existing batch as new batch

* Add option for auto-deleting empty batch, when created via filemon


0.7.61 (2017-01-12)
-------------------

* Fix CSV handheld batch parser, to allow decimal amounts


0.7.60 (2017-01-11)
-------------------

* Fix bugs for datasync error email preview

* Various fablib tweaks...


0.7.59 (2017-01-06)
-------------------

* Fix ``set_timezone()`` fabric function, to handle symlink

* Fix typo in label batch handler


0.7.58 (2017-01-03)
-------------------

* Add ``PurchaseCredit.product_discarded``, method for making credits from batch

* Add ``get_received_quantity()`` convenience method for purchasing batch


0.7.57 (2016-12-30)
-------------------

* Add ``Purchase.po_line_number`` for improved PO update support

* Tweak purchase batch handler to allow customizing how row totals are refreshed


0.7.56 (2016-12-20)
-------------------

* Allow custom logic for unit cost cost; tweak enum for 'ordering' batch type

* Disable some importing tests, for now at least...


0.7.55 (2016-12-19)
-------------------

* Fix importer method signature

* Tweak log message for importer results


0.7.54 (2016-12-16)
-------------------

* Use decimal for case/unit quantities in handheld/inventory batches


0.7.53 (2016-12-16)
-------------------

* Add ``empty_zero`` kwarg for ``util.pretty_quantity()``

* Add ``db.util.make_full_description()`` convenience function

* Tweak purchase batch handler logic to account for "product not found"

* Add ``Importer.progress_loop()`` convenience method

* Add basic support for "extension fields" to ``ProductImporter``

* Add ``Product.scancode`` and ``uom_abbreviation`` to schema

* Fix/improve logic for importing 'preferred' pseudo-field for ``ProductCost``


0.7.52 (2016-12-12)
-------------------

* Add ``User.get_short_name()`` convenience method

* Tweak some things to make older SQLAlchemy happy


0.7.51 (2016-12-11)
-------------------

* Use 'rattail.emails' as fallback for tailbone view

* Add way to prevent [STAGE] prefix magic when editing in tailbone

* Remove email configs for tempmon

* Add config for feedback email, let config dictate that's the only one sent


0.7.50 (2016-12-10)
-------------------

* Add ``from_utc`` arg to ``time.localtime()`` function

* Remove tempmon mail templates


0.7.49 (2016-12-10)
-------------------

* Always add [STAGE] email prefix unless running in production mode

* Allow null values for cases/units when parsing CSV handheld file

* Add column for ``Purchase.department``

* Add ``PurchaseCredit`` and friends to schema

* Add ``util.pretty_quantity()`` convenience function


0.7.48 (2016-12-08)
-------------------

* Allow password to be set for ``make-user`` command

* Remove Lance from sample data

* Add support for importing plain password, for sample data


0.7.47 (2016-12-05)
-------------------

* Let email subject be rendered "raw" or as template

* Add base class for tempmon email config, for common sample data

* Add fab function for removing cached SSH host key

* Remove `tempmon-server` command (moved to rattail-tempmon project)


0.7.46 (2016-11-30)
-------------------

* Fix bug when checking probe readings in tempmon-server


0.7.45 (2016-11-30)
-------------------

* Fix some import bugs


0.7.44 (2016-11-30)
-------------------

* Fix syntax bugs


0.7.43 (2016-11-30)
-------------------

* Fix tempmon-server logic a bit, add default email config


0.7.42 (2016-11-30)
-------------------

* Add ``tempmon-server`` command to start/top daemon


0.7.41 (2016-11-22)
-------------------

* Add support for generic pricing batch

* Add initial tempmon data models, server daemon

* Fix bug in vendor item code lookup for invoice batch refresh


0.7.40 (2016-11-21)
-------------------

* Add basic support for receive/cost mode for purchase batches

* Cleanup refresh logic a bit, for vendor invoice batches


0.7.39 (2016-11-19)
-------------------

* Tweak label batch so that product-less rows are allowed


0.7.38 (2016-11-19)
-------------------

* Overhaul the new batch framework...


0.7.37 (2016-11-17)
-------------------

* Add ``RattailConfig.get_enum()`` method

* Delete vendor contact record when deleting associated person


0.7.36 (2016-11-15)
-------------------

* Fix wording for label batch row status


0.7.35 (2016-11-14)
-------------------

* Add ``Vendor.fax_number`` convenience property

* Add ``Person._vendor_contacts`` relationship

* Make ``ProductCost.case_size`` a decimal instead of integer

* Make 'rattail.pod' config a bit more sane

* Add support for importing ``Product.category_code``


0.7.34 (2016-11-10)
-------------------

* Add ``session.no_autoflush`` block when importer creates new SQLAlchemy object


0.7.33 (2016-11-08)
-------------------

* Tweak signature for ``util.progress_loop()`` for simplicity

* Add ``Purchase`` and ``PurchaseBatch`` data models, etc.

* Add ``LabelBatch`` feature, creatable from handheld batch, product query etc.

* Add ``include_deleted`` flag to product lookup api

* Improve relationship between product and batch rows which reference it


0.7.32 (2016-11-04)
-------------------

* Add ``importing.FromDjango`` base class

* Tweak console progress a bit


0.7.31 (2016-11-01)
-------------------

* Fix bug in ``util.progress_loop()`` when no progress factory provided


0.7.30 (2016-10-31)
-------------------

* Fix bug in customer importer when used via datasync


0.7.29 (2016-10-27)
-------------------

* Improve handling of Albert's invoice when item has no case quantity

* Add ``datasync.watchers.NullWatcher``, auto-triggered by 'null' watcher spec

* Add basic API docs for ``rattail.importing`` package

* Refactor some rattail model importers so datasync may leverage them

* Fix timing bug when importing new product cost data


0.7.28 (2016-10-26)
-------------------

* Lots of fablib changes...see commit log

* Fix .gitignore filename in project scaffold

* Fix permission checks, add 'become root' for web menu in scaffold

* Add workaround for Employee importer, if no Person is attached

* Fix a bug with win32 filemon when watching for locks


0.7.27 (2016-10-19)
-------------------

* Add ``util.progress_loop()`` convenience function

* Improve default behavior for ``BatchHandler.refresh_data()``

* Add department number/name columns to product batch rows

* Add ``fablib`` modules: postfix, certbot, corepos, apache

* Improve various fablib modules: apt, postgresql, mysql

* Assume owner name means user:group in ``fablib.mkdir()``

* Add ``fablib.set_timezone()`` convenience function

* Stop granting all perms to 'admin' role (per "become root" tailbone feature)

* Accept extra context when deploying mako template via fablib


0.7.26 (2016-10-10)
-------------------

* Fix chicken vs egg bug when reading db config

* Add ``rattail import-sample`` command for dev/test bootstrap etc.

* Add ``rattail make-config`` command for dev/test bootstrap etc.

* Add ``rattail make-appdir`` command for dev/test bootstrap etc.

* Add ``rattail make-uuid`` command for convenience

* Add first version of project template (pyramid scaffold)

* Overhaul ``rattail make-user`` command to support multiple systems

* Remove deprecated commands: ``adduser``, ``initdb``

* Add some functions for use with sms-admin utility

* Add generic ``rattail.util.prettify()`` function


0.7.25 (2016-10-05)
-------------------

* Be smarter when caching department data, in some importers


0.7.24 (2016-10-04)
-------------------

* Let import handler's ``warnings`` flag get passed to importers

* Let SQLAlchemy-targeting importer override local cache query

* Add ``RattailConfig.setdb()`` method, for ad-hoc settings


0.7.23 (2016-10-04)
-------------------

* Fix minor bugs with Rattail -> Rattail data importers


0.7.22 (2016-10-04)
-------------------

* Fix optimizations for Rattail -> Rattail data importers


0.7.21 (2016-09-28)
-------------------

* Always warn if duplicate keys detected when caching a data model

* Add ``Category.code`` to schema


0.7.20 (2016-09-27)
-------------------

* Fix typo bug


0.7.19 (2016-09-26)
-------------------

* Refactor some things to avoid unwanted eager imports

* Add customization hook for identifying product for vendor catalog row

* Log traceback when error happens for filemon action

* Add 'refreshable' flag to batch handler

* Add basic phone number validation logic, tweak email validation

* Add "full" model importer support, for sake of SMS -> Rattail

* Tweak base importer logic to allow for *not* creating new object


0.7.18 (2016-08-23)
-------------------

* Add support for raw RattailCE data files for handheld batches

* Auto-associate batch row class with batch class

* Add ``BaseFileBatchMixin`` in hopes it makes sense...

* Skip 'removed' rows when creating inventory batch from handheld batch

* Add "count mode" for inventory batches

* When deleting batch, only try to delete its file if it has a filename


0.7.17 (2016-08-18)
-------------------

* Fix import bug in inventory batch handler

* Add hostname to filemon action error email


0.7.16 (2016-08-17)
-------------------

* Allow extra kwargs to be passed to new-style batch handler execute() method

* Add system-wide unique ID for new-style batches

* Add new 'handheld' and 'inventory' batches


0.7.15 (2016-08-13)
-------------------

* Add basic retry mechanism to datasync ``watcher.get_changes()`` logic

* Tweak logic for determining effective importers, in datasync consumer


0.7.14 (2016-08-12)
-------------------

* Add common config for filemon error emails


0.7.13 (2016-08-12)
-------------------

* Send proper email when filemon encounters error while invoking action

* Add ``RattailConfig.getdate()`` convenience method

* Add datasync URL to email template for watcher errors


0.7.12 (2016-08-10)
-------------------

* Log warning instead of error when datasync watcher fails to get changes


0.7.11 (2016-08-10)
-------------------

* Add FormEncode as official dependency

* Add custom email for datasync ``watcher.get_changes()`` errors


0.7.10 (2016-08-10)
-------------------

* Add ``batch_filedir()`` and ``batch_filepath()`` methods to main config object

* Add simple email validator to ``db.util`` module


0.7.9 (2016-08-09)
------------------

* Add product flags for food stamps and tax 1/2/3

* Add ``GPC.type2_upc`` convenience attribute


0.7.8 (2016-07-27)
------------------

* Move ``cache_model()`` method to core ``Importer`` class

* Let ``make_utc()`` use current time as default


0.7.7 (2016-07-08)
------------------

* Add ``Importer.fields_active()`` convenience method

* Tweak CSS to preserve whitespace in import diff email field values


0.7.6 (2016-06-17)
------------------

* Fix timezone bug in shift ``get_date()`` method

* Add special 'authenticated' role, for easier permission management

* Add convenience attributes to ``GPC`` class (``data_str`` and ``data_length``)

* Force session flush after processing changes in datasync consumer thread


0.7.5 (2016-06-10)
------------------

* Add initial/basic support for Shinken monitoring software

* Add generic daemon init script

* Add support for more fields to Employee data importer

* Add default logic for obtaining importers from handler, in new datasync consumer


0.7.4 (2016-06-01)
------------------

* Never update local object's key field(s) when importing

* Add simple attribute so handlers can override diff count in warning emails


0.7.3 (2016-05-27)
------------------

* Add logic for skipping deletion if no key, in import-based datasync consumer


0.7.2 (2016-05-26)
------------------

* Remove redundant "flush" handling from ``ToSQLAlchemy`` importer

* Add comma formatting to counts within import warning diff emails

* Fix delete behavior for ``ToSQLAlchemy`` importer (don't expunge)

* Add datasync consumer base class for new-style importers

* Add support for preferred field in new phone/email importers

* Default to empty list for cache query options in SQLAlchemy importers


0.7.1 (2016-05-17)
------------------

* More tweaks for new importer framework:
   * Pass ``args`` all the way from command -> handler -> importer
   * Add ``BulkImporter`` and ``BulkImportHandler`` base classes
   * Add ``ToRattailHandler``, ``FromRattailHandler`` for convenience
   * Add ``ImportHandler.commit_partial_host`` flag and logic
   * Add ``Importer.empty_local_data`` flag and logic
   * Fix bug where ``Importer.delete`` flag was ON by default
   * Add ``ImportSubcommand.handler_spec`` for simpler subclass config
   * Add "batching" support, with ``--batch`` command line arg

* Remove deprecated Rattail -> Rattail importers


0.7.0 (2016-05-14)
------------------

* Add new/final importing framework, with full test coverage.

* Refactor ``import-rattail`` and ``import-rattail-bulk`` per new framework.

* Add ``AdminUser`` import model, for use with ``import-rattail``.


0.6.26 (2016-05-11)
-------------------

* Pseudo-release to work around PyPI bug?


0.6.25 (2016-05-11)
-------------------

* Remove unused 'ignore role changes' flag for data change recorder.

* Grow size of "change key" columns to 255 chars.

* Refactor "record changes" mechanism to allow custom behavior.


0.6.24 (2016-05-07)
-------------------

* Fix bug when importing new Employee record.


0.6.23 (2016-05-06)
-------------------

* Remove alembic import from ``db.util`` module.


0.6.22 (2016-05-05)
-------------------

* Refactor scheduled/worked shift models to share some logic.

* Make 'tests' a proper subpackage again; add some tests.


0.6.21 (2016-05-03)
-------------------

* Fix bug in ``format_phone_number()`` function.


0.6.20 (2016-05-03)
-------------------

* Fix line endings for email templates.

* Add ``--timeout`` arg support to ``datasync wait`` command.

* Refactor where phone number normalization logic lives.


0.6.19 (2016-05-02)
-------------------

* Add basic user feedback email template.

* Add ``.gitattributes`` file to enforce DOS line endings for mail templates.

* Rename original ``ImportSubcommand`` to ``OldImportSubcommand``.

* Add support for 'normalized_number' field in phone importer.


0.6.18 (2016-04-29)
-------------------

* Add empty ``Watcher.process_changes()`` method for datasync.


0.6.17 (2016-04-28)
-------------------

* Add ``RattailConfig.workdir()`` convenience method.

* Add ``time.get_sunday()`` convenience function.

* Add ``ScheduledShift`` model to schema.


0.6.16 (2016-04-26)
-------------------

* Tweak default behavior for importer-based datasync consumer.


0.6.15 (2016-04-26)
-------------------

* Tweak when we add new data instance to session, to avoid premature flushes.


0.6.14 (2016-04-25)
-------------------

* Add ``WorkedShift`` data model to schema, importer.

* Add bulk Rattail importer, plus various tweaks.


0.6.13 (2016-04-24)
-------------------

* Add ``add_mail_alias()`` fabric function.

* Add ``Watcher.setup()`` method for datasync.

* Add ``Consumer.setup()`` method for datasync.

* Skip data sync for "empty" host record, in importer-based consumers.

* Add ``config.parse_bool()`` function.

* Add ``model_mapper`` and ``model_table`` attributes to base importer class.

* Add base importer and handler for PostgreSQL "bulk copy" importing.

.* Add ``--start-date`` and ``--end-date`` args to importer command.

* Add ``RattailConfig.production()`` method.

* Add multi-batch change transaction support for datasync consumers.

* Provide method by which importers may prevent create/update/delete.

* Add ``data`` kwarg to ``Importer.cache_instance_data()`` method.

* Alter ``make_utc()`` function to allow returning zone-aware time.

* Add initial begin/rollback/commit abstraction to import handlers.

* Add ``invoke_importer()`` method to datasync import consumers.


0.6.12 (2016-04-12)
-------------------

* Fix bug where ``usedb`` flag wasn't being set from ``make_config()``.


0.6.11 (2016-04-06)
-------------------

* Fix bug in ProductCode importer when new records are created.


0.6.10 (2016-04-05)
-------------------

* Fix config bug for recording changes in rattail db.


0.6.9 (2016-04-05)
------------------

* Tweak import logging and warning email templates; add runtime etc.

* Tweak some logging when initial/basic changes are recorded.

* Improve the core importer class to better allow non-SQLAlchemy targets.

* Add new importer-based datasync consumer class.

* Make a copy of the ``RecordRenderer`` class for new importer framework.

* Add host session to main transaction, when importing from SQLAlchemy.

* Add mechanism to record changes only for sessions on certain engines.

* Add ``Importer.get_single_instance()`` for easier customization.


0.6.8 (2016-03-11)
------------------

* Fix ``cmp(GPC)`` behavior when ``other`` is None etc.


0.6.7 (2016-02-27)
------------------

* Add initial color-coded diffs to data import warning emails.

* Fix bug with importing of customer first/last name.

* Tweak ``unicode(Employee)`` output.


0.6.6 (2016-02-27)
------------------

* Add ``date_argument`` back to ``rattail.commands`` root.


0.6.5 (2016-02-27)
------------------

* Make ``commands`` subpackage, add ``rattail-dev`` command.

* Tweak logging wording when datasync threads die from error.


0.6.4
-----

* Make sure message recipients are unique.

* Tweak some wording on data import warnings email template.


0.6.3
-----

* Tweak logging, warning template for new data importers.


0.6.2
-----

* Make config object's underlying db session somewhat configurable.


0.6.1
-----

* Fix bug in Rattail->Rattail import handler.


0.6.0
-----

* Add new importing framework, yay!

* Fix support for 'full_name' field in employee data importer.

* Tweak some ORM mappings, to support cascading deletes.

* Add ``Message.has_recipient()`` method.


0.5.36
------

* Tweak how changes are sorted by class name, in Rattail datasync consumer.

* Add ``metadata`` kwarg to the topographical sortkey function maker.


0.5.35
------

* Change how we sort dependencies when processing datasync changes for rattail.

* Tweak how ``Person.display_name`` is handled during data import.


0.5.34
------

* Check for null password before attempting bcrypt authentication.

* Add recursion support to table dependency sorter function.


0.5.33
------

* Increase field size for ``Change.class_name``.


0.5.32
------

* Sort department associations by name, by default.

* Add ``EmployeeStore`` association model, with import.

* Record change on employee when store/dept association are deleted.


0.5.31
------

* Give vendor catalog rows a default description of empty string.

* Tweak how vendor catalog parsers interpret decimal values.

* Change how a vendor catalog batch gets its vendor (parser needn't declare one).

* Make upgrade of pip optional when doing ``mkvirtualenv()`` via fabric.


0.5.30
------

* Add temp hack to avoid ``Person.modified`` when doing a data dump.

* Only compare 'effective' fields when checking data diff during import.

* Add import normalizers for Department and Employee models.

* Add new ``EmployeeDepartment`` model, and importer.


0.5.29
------

* Bugfix; remove ``progress`` kwarg from (another) importing ``setup()`` method.


0.5.28
------

* Add ``Importer.normalizer_class`` default attribute.


0.5.27
------

* Add ``User.employee`` convenience attribute.

* Remove Python 2.6 from supported versions in trove classifiers.

* Don't use db when fetching timezone from config.

* Remove ``progress`` kwarg from db importing ``setup()`` methods.

* Change how 'ignored' models are handled for rattail datasync consumers.

* Add 'normalizer' concept to data importer.

* Add initial 'messages' support in schema/import.

* Add initial rattail->rattail data importer.


0.5.26
------

* Move "process warnings" logic for importers, to handler for simpler overriding.


0.5.25
------

* Add ``Person.middle_name`` and ``Person.modified``.

* Make datasync errors cause the parent thread to terminate.


0.5.24
------

* Add ``str(RattailError)`` logic.

* Tweak ``repr(Change)`` output, to add ``deleted`` flag.

* Make a more generic dependency sorting function, for datasync.

* Add ``Email.invalid`` flag.

* Record change for Person when email/phone is being deleted.

* Add ``MailingAddress`` to schema.

* Tweak cache API to allow caller to specify query, and prevent duplicate keys.

* Add support for importing ``CustomerPhoneNumber`` data.

* Tweak ORM relationship for ``CustomerPerson.customer``.

* Add ``teardown()`` method for cleanup after data importing.

* Add support for "preferred" pseudo-field when importing phone/email data.


0.5.23
------

* Add ``Category.products`` backref.


0.5.22
------

* Add ``uid`` param to ``bootstrap_rattail()`` fablib function.

* Add delete-orphan cascade for ``Person._customers`` relation.


0.5.21
------

* Don't warn when sending HTML-only email messages.

* Log debug instead of warning when duplicate cache key found.

* Return email/phone when adding to person.


0.5.20
------

* Add warning in ``db.cache.cache_model()`` when duplicate keys are found.

* Raise custom exception when no templates found for email.


0.5.19
------

* Add attachment support to ``mail.send_email()`` function.

* Add "wait for changes" support to datasync command.


0.5.18
------

* Replace ``rsync()`` function in fablib.

* Add ``Email.abstract`` attribute, and tweak fallback key.


0.5.17
------

* Overhaul email framework.


0.5.16
------

* Add support for 'primary' pseudo-field when importing product codes.


0.5.15
------

* Fix possible bug when importing cost preferences.

* Fix bug in importer, when there are no source data records.


0.5.14
------

* Add ``files.move_lpt()`` function, remove ``minimal_move()``.


0.5.13
------

* Fix the db 'dump' function to use unicode and utf-8 file encoding.

* Add ``files.minimal_move()`` function, for "moving" files to LPT ports.


0.5.12
------

* Install ndg-httpsclient also, when installing pip site-wide.

* Fix edge case bug when importing $0 product prices.


0.5.11
------

* Add ``download_db()`` fablib functions for mysql, postgresql.

* Add ``configure_virtualenvwrapper()`` to fablib, for adding per-user config.

* Add ``Deployer`` class to fablib, for ``deploy.sudoers()`` support.

* Always install/upgrade pip and friends when making a new virtualenv.

* Check for existence of MySQL database before dropping it, in fablib.

* Add "watcher consumes self" concept to datasync daemon.

* Add time zone coercion to logged timestamps, if configuring logging in general.


0.5.10
------

* Add ``default.enabled`` config logic for ``rattail.mail``.

* Add ``ErrorTestConsumer`` for testing datasync error handling.

* General overhaul of ``rattail.fablib`` subpackage, to support online docs.

  * Add Mako support to ``deploy()`` functions.

  * Add ``rsync()`` function.

  * Add ``bootstrap_rattail()`` function.

  * Add ``get_debian_version()`` function.

* Fix subtle bug if email template not found.

* Revamp the ``initdb`` command a bit.

* Add ``db_model`` property to ``Command`` class.

* Add docs to ``release`` task.


0.5.9
-----

* Add ability to disable emails on a per-type basis.

* Add basic exception logging to datasync daemon.

* Clean up some logging calls when recording instance changes.

* Improve ``repr(Change)`` output.

* Add some more custom units of measure (packets, doses).

* Tweak startup logic involving config and logging.


0.5.8
-----

* Grow ``DataSyncChange.payload_type`` column.


0.5.7
-----

* Add ``Change.uuid`` as new primary key for the table.

* Add 'datasync' daemon.

* Add ``clonedb`` command.

* Remove version restriction for SQLAlchemy-Utils.

* Improve the ``localtime()`` function a bit.

* Tweak 'settings' API functions so they don't require a session.


0.5.6
-----

* Fix manifest to include email templates.


0.5.5
-----

* Add temporary hack for sake of WinCE label batches.


0.5.4
-----

* Add config to old ``BatchExecutor`` constructor.

* Add ``--no-extend-config`` arg to command line system, for sake of tests.

* Add support for "fallback key" when sending mail with config.

* Add ``ImportHandler`` class, update ``ImportSubcommand`` to use it etc.


0.5.3
-----

* Configure logging when initializing Windows services.


0.5.2
-----

* Fix another dang bug in ``config.get_user_dir()``.


0.5.1
-----

* Fix bug in ``config.get_user_file()`` signature.


0.5.0
-----

The main reason for the version bump here, is the removal of the 'edbob'
dependency.  This has been a long-anticipated event.

* Fix cascade rules for user/role relationships.

* Add default ``repr()`` behavior to data model classes.

* Fix type bug in ``db.api.get_department()``.

* Add custom errors for when SA / Python for Windows Extensions not installed.

* Remove some unused/unwanted command line arguments.

* Move some config-related functions to ``rattail.db.config``.

* Overhaul config system, finally replacing edbob (yay!).

* Remove support for certain deprecated (edbob) config settings.

* Remove ``make-config`` command, and edbob dependency!

* Add ``config`` arg to ``labels.LabelFormatter`` constructor.

* Refactor guts of ``sil.consume_batch_id()`` function.

* Add optional ``progress`` arg to ``BatchHandler.execute()`` method.


0.4.30
------

* Add ``core.UNSPECIFIED`` convenience object.

* Fix data bug in ``user_x_role`` table.


0.4.29
------

* Add config for recycling IMAP connection in bouncer daemon.


0.4.28
------

* Add 2nd version of UNFI catalog parser.


0.4.27
------

* Ignore warnings about running on Python 2.6, we know it's an issue.


0.4.26
------

* Add version restriction for SQLAlchemy-Utils.


0.4.25
------

* Add initial support for email bounce schema, daemon etc.


0.4.24
------

* Add ``files.locking_copy_old()`` function...for now.


0.4.23
------

* Add ``get_store()`` API function.

* Add row to batch prior to cognizing the row.  (If cognize fails, remove row
  from batch.)


0.4.22
------

* Fix bug in KeHe invoice parser, if row has no UPC.


0.4.21
------

* Set default filename for file-based batches if it's safe to do so.

* Add ``MakeFileBatch`` generic filemon action.

* Add ``BatchHandler.executable()`` method, for sake of UI.

* In batch handlers, let ``cognize_row()`` return ``False`` to skip the row.

* Add ``date-organize`` command for help with archiving data files etc.


0.4.20
------

* Add support for configurable Reply-To address when sending email.

* Always upgrade pip (and install wheel) when "installing" pip.

* Add 'key' as 3rd positional / 1st keyword arg to ``cache_model()`` function.

* Give commands a proper ``RattailConfig`` object instance.

* Add ``RattailConfig.getint()`` method to allow a default value.

* Change behavior of ``files.locking_copy()`` function.


0.4.19
------

* Add basic support for email attachments.


0.4.18
------

* Don't normalize ``Employee.display_name`` to null, in importer.


0.4.17
------

* Don't change mode for 'app/log' folder in ``mkvirtualenv()``.

* Add config setting to globally disable sending of emails.

* Add ``User.get_email_address()`` and ``User.email_address``.

* Add ``mail.get_template()``; allow override of subject and recipients.

* Allow override of UID when creating system user via Fabric.

* Add ``grant_mysql_access()`` function for Fabric.

* Fix bug in ``create_mysql_user()`` Fabric function.

* Don't normalize customer name fields to ``None`` when importing.


0.4.16
------

* Add some SSH config stuff for Fabric.

* Add ``get_product_by_vendor_code()`` API function.

* Add ``PathNotFound`` exception, normalize to it within ``locking_copy_test()``.


0.4.15
------

* Add ``--max-updates`` arg to import commands.


0.4.14
------

* Don't normalize ``Product.size`` to null when importing.


0.4.13
------

* Fix constructors etc. for old-style batch providers.


0.4.12
------

* Normalize duplicate source records during data import.

* Make config a required arg to ``BatchProvider`` constructor.

* Tweak ``locking_copy_test()`` to assume destination is always a folder.


0.4.11
------

* Add ``Person.employee`` relationship and ``User.employee`` convenience
  property.

* Change how customer phone data is handled in importer.

* Add ``get_department()`` API function.

* Tweak filemon and dbsync init scripts to avoid issue of root-owned log file.

* Add ``files.locking_copy_test()`` function.


0.4.10
------

* Don't normalize simple instance fields unless they're involved in the import.

* Log warning when duplicate key is detected during import.


0.4.9
-----

* Add ``UnicodeDictWriter`` and ``csvutil`` API docs.

* Various changes to allow custom commands to sit in front of non-Rattail
  database.

* Tweak case quantity in Albert's invoice parser.

* Add ``--warnings`` flag to base import command.

* Fix phone number normalization for customer importer.

* Add ``DataProvider.int_()`` method for importers.

* Add supposed optimization for simple fields within importer.


0.4.8
-----

* Add unit of measure for cubic feet.


0.4.7
-----

* Stop normalizing some fields on data import.

* Catch import error when configuring db in command startup.


0.4.6
-----

* Add deposit links, taxes, product organic flag.

* Improve product and vendor schema some more.

* Revert to simple names and descriptions for model ``unicode()``.

* Add ``GPC.pretty()`` method.

* Add ``order_by`` kwarg to ``db.cache.cache_model()`` function.

* Add ``get_subdepartment()`` API function.

* Add duplicate UPC warning in ``ProductCost`` importer.

* Hopefully fix ``install_pip`` Fabric function.


0.4.5
-----

* Add ``status_text`` field to batch row tables.

* Add ``BatchHandler.make_batch()`` method.

* Add ``FileBatchHandler`` class.

* Add ``repr()`` for batch models.

* Add vendor catalog batch importer.

* Add vendor invoice batch importer.

* Add some docs for new batch system.

* Add initial ``RattailConfig`` class.

* Make sure ``unzip`` is installed when fabricating POD stuff.

* Fix some string formatting for Python 2.6.


0.4.4
-----

* Make ``Employee.person`` column unique.

* Try again to make database stuff an optional dependency...

* Increase size of ``ProductCost.code`` column.

* Add ``Product.case_pack`` column.

* Add ``encoding_errors`` kwarg to ``UnicodeWriter`` class constructor.


0.4.3
-----

* Fix Alembic ``env.py`` script to accommodate Continuum.

* Add ``Product.deleted`` column.


0.4.2
-----

* Fix password prompt on Windows for ``make-user`` command.


0.4.1
-----

* Rework how Continuum versioning is configured.


0.4.0
-----

This version primarily got the bump it did because of the addition of the data
import framework and support for SQLAlchemy-Continuum versioning.  There were
several other minor changes as well.

* Allow Fabric ``env`` to override POD download URL.

* Quote packages when installing via Fabric ``pip()`` function.

* Add ``time.make_utc()`` function.

* Add ``db.util.maxlen()`` function.

* Add ``set_regular_price()`` and ``set_current_sale_price()`` API functions.

* Add ``db.cache.cache_model()`` function.

* Add ``csvutil.UnicodeWriter`` class.

* Add ``db.importing`` subpackage.

* Add ``ImportSubcommand`` as base class for data import subcommands.

* Add ``import-csv`` command.

* Fix encoding issue when sending email with non-ASCII chars in message.

* Increase length of ``Vendor.name`` column.

* Add encoding support to ``files.count_lines()``.

* Add initial versioning support with SQLAlchemy-Continuum.


0.3.50
------

* Add Alembic files to the manifest.


0.3.49
------

* Make all constraint and index names explicit.

* Add core Alembic migration repository.


0.3.48
------

* Fix filemon fallback watcher to ignore things which aren't files.


0.3.47
------

* Pause execution within filemon action loops (fix CPU usage).

* Add fallback watcher feature for filemon on Windows.


0.3.46
------

* Add ``Product.pretty_upc`` and improve ``unicode(Product)``.

* Make ``Vendor.id`` unique; add ``get_vendor()`` API function.

* Change default batch purge date to 60 days out instead of 90.

* Make SIL writer use a temp path if caller doesn't provide one.

* Add ``Product.cost_for_vendor()`` method.

* New batch mixin system...

* Split ``db.model`` into subpackage.


0.3.45
------

* Quote PG username when setting password via Fabric.

* Allow override of progress text in ``sil.Writer.write_rows()``.

* Move bcrypt requirement into 'auth' extra feature.


0.3.44
------

* Fix some string literal bugs.


0.3.43
------

* Add ``shell=False`` arg to some Fabric calls for PostgreSQL.


0.3.42
------

* Add ``consume_batch_id()`` convenience method to ``sil.Writer`` class.

* Add mail alias option to ``make_system_user()`` Fabric function.

* Add virtualenvwrapper to profile script for root and current user.

* Make alembic a core requirement, for now...


0.3.41
------

* Add ``fablib`` subpackage.

* Add ``obfuscate_url_pw()`` to ``db.util`` module.

* Add ``temp_path()`` method to ``rattail.sil.Writer`` class.


0.3.40
------

* Allow overriding key used to determine mail template name.

* Add ``Store.database_key`` column.

* Move some function logic to ``db.util``.

* Add ``csvutil.UnicodeDictReader`` class.


0.3.39
------

* Let mail template paths be specified as relative to a Python package.


0.3.38
------

* Tweak ``BatchProvider`` constructor, to prepare for edbob removal.

* Email notification rewrite.

* Improve Unicode handling within some label printing logic.


0.3.37
------

* Add ``Product.not_for_sale`` flag.


0.3.36
------

* Add ``time`` module.


0.3.35
------

* Fix bug in SIL writer (make sure all writes use instance method).


0.3.34
------

* Add error handling when attempting user authentication with non-ASCII characters.

* Add timeout to ``locking_copy()``.


0.3.33
------

* Add ``User.active`` and disallow authentication for inactive users.


0.3.32
------

* Add ``ReportCode`` and ``Product.report_code`` to schema.

* Fix ``Product.family`` relationship.

* Add ``rattail.config`` module, currently with ``parse_list()`` function only.


0.3.31
------

* Fix unicode bug in filemon config parsing on Python 2.6.


0.3.30
------

* File Monitor overhaul!

   * New configuration syntax (old syntax still supported but deprecated).
   * Class-based actions.
   * Configure keyword arguments to action callables.
   * Configure retry for actions.
   * Add (some) tests, docs.


0.3.29
------

* Add support for older SQLAlchemy (0.6.3 specifically).


0.3.28
------

* Accept config section name within ``rattail.db.util.get_engines()`` and
  ``rattail.db.util.get_default_engine()``.

* Remove deprecated ``record_changes`` option in ``[rattail.db]`` config
  section.

* Remove deprecated ``rattail.db.init()`` function stub.


0.3.27
------

* Don't require bcrypt unless 'db' feature is requested.


0.3.26
------

* Add ``filemon.util.raise_exception`` for simple file monitor testing.

* Add tox support; fix several test oddities.

* Fix thread naming bug in Windows file monitor.


0.3.25
------

* Require process elevation for ``make-user`` command.

* Use 64-bit registry key when hiding user account on 64-bit Windows.

* Refactor to remove namespace structure.


0.3.24
------

* Stop using ``logging.get_logger()`` adapter wrapper, until we know how to do
  it right.


0.3.23
------

* Use ``find_packages()`` again, as the last build was broken.  (But still
  exclude tests.)


0.3.22
------

* Add some error checking when starting Linux daemons.

* Add ``'uid'`` and ``'username'`` to logger adapter context dict.

* Add initial POD integration module.

* Stop using ``find_packages()``; it was including tests.

* Add "lock" support to Windows file monitor.


0.3.21
------

* Add custom ``LoggerAdapter`` implementation; used by file monitor.
    
  Hopefully this does a better job and avoids some wheel reinvention.


0.3.20
------

* Better leverage config when initializing Win32 services.


0.3.19
------

* Define ``Command`` and ``Subcommand`` classes.
    
  These are (finally) no longer borrowed from ``edbob``, yay.

* Add SQLAlchemy to core dependencies.

* Database config/init overhaul.
    
  This contains some not-very-atomic changes:

  * Get rid of ``get_session_class()`` function and return to global
    ``Session`` class approach.
  * Primary database ``Session`` is now configured as part of command
    initialization, by default.
  * Make ``config`` object available to subcommands, and ``Daemon`` instances
    (the beginning of the end for ``edbob.config``!).
  * Add ``--stdout`` and ``--stderr`` arguments to primary ``Command``.  These
    are in turn made available to subcommands.
  * Overhauled some subcommand logic per new patterns.
  * Get rid of a few other random references to ``edbob``.
  * Added and improved several tests.
  * Added ability to run tests using arbitrary database engine.


0.3.18
------

* Populate ``rattail.db.model.__all__`` dynamically.

* Add ``util.load_entry_points()``.


0.3.17
------

* Add SQLAlchemy engine poolclass awareness to config file.


0.3.16
------

* Make ``get_sync_engines()`` require a config object.

* Add ``getset_factory()`` to ``rattail.db.core``.

* Dont auto-import ``core`` and ``changes`` from ``rattail.db``.

* Handle keyboard interrupt when running dbsync on Linux console.

* Make ``rattail.db.model`` the true home for all models.


0.3.15
------

* Removed global ``Session`` from ``rattail.db``.
    
  A Session class may now be had via ``get_session_class()``.

* Removed reliance on ``edbob.db.engines``.

* Added initial docs (barely, mostly for testing Buildbot).

* Updated tests to work on Python 2.6.

* Improved init scripts to create PID file parent directory as needed.

* Allow Windows file monitor installation with custom user account.


0.3.14
------

* Improve ``make-user`` command somewhat.
    
  Allow username etc. to be overridden; add sanity check if running on platform
  other than win32.


0.3.13
------

* Fix ``ChangeRecorder.is_deletable_orphan()`` for SQLAlchemy 0.7.
    
  Apparently ``Mapper.relationships`` is not available until SQLAlchemy 0.8 and
  later...


0.3.12
------

* Add ``deleted`` attribute to ``repr(Change)``.

* Add "deletable orphan" awareness when recording changes.
    
  Turns out there was a long-standing bug where orphans which were deleted from
  the host would be marked as "changed" (instead of deleted), causing the store
  databases to keep the orphan.


0.3.11
------

* Added ``mail.send_message()`` etc.


0.3.10
------

* Altered ``dump`` command to allow easy overriding of data model.


0.3.9
-----

* Add all of ``data`` folder to manifest.

* Replaced ``insserv`` calls with ``update-rc.d`` in Fabric script.

* Fixed bug in ``price_check_digit()``; added tests.

* Fixed bug in ``upce_to_upca()``; added tests.

* Added ``get_employee_by_id()`` convenience function.

* Refactored model imports, etc.
    
  This is in preparation for using database models only from ``rattail``
  (i.e. no ``edbob``).  Mostly the model and enum imports were affected.

* Added remaining values from ``edbob.enum`` to ``rattail.enum``.

* Added ``get_setting()`` and ``save_setting()`` to ``db.api``.


0.3.8
-----

* Overhauled db sync somewhat; made a little more customizable, added tests.


0.3.7
-----

* Fixed db sync to properly handle ``Family`` deletions.


0.3.6
-----

* Fixed bug in ``Product.full_description``.

* Added ``core.Object`` class.

* Made ``enum`` module available from root namespace upon initial import.

* Added ``util`` module, for ``OrderedDict`` convenience.

* Add ``Family`` and ``Product.family``.


0.3.5
-----

* Declare dependencies instead of relying on edbob.

* Added ``db.auth`` module.

* Added ``initdb`` command.

* Added the ``adduser`` command.

* Pretend ``commands.Subcommand`` is defined in ``rattail``.


0.3.4
-----

* Fixed ``Customer._people`` relationship cascading.


0.3.3
-----

* Fixed bugs with ``CustomerGroupAssignment``.
    
  Now orphaned records should no longer be allowed.

* Fixed ``CustomerPerson`` to require customer and person.

* Added ``--do-not-daemonize`` flag to ``dbsync`` command on Linux.

* Overhauled some database stuff; added tests.

* Added some ``CustomerEmailAddress`` tests, removed some unused tests.


0.3.2
-----

* Fixed bug in ``csvutil.DictWriter``; added tests.


0.3.1
-----

* Added ``Product.full_description`` convenience attribute.

* Added ``--do-not-daemonize`` arg to ``filemon`` command on Linux.

* Added ``dump`` command.


0.3a43
------

* Added unicode-aware CSV reader.


0.3a42
------

* Fixed dbsync bug when deleting a ``CustomerGroup``.
    
  Any customer associations which still existed were causing database integrity
  errors.


0.3a41
------

* Added ``get_product_by_code()`` API function.


0.3a40
------

* Added proper ``init.d`` support to Linux dbsync daemon.
    
   * Added ``--pidfile`` argument to ``dbsync`` command.
   * Added ``configure_dbsync`` Fabric command.

* Added ``files.overwriting_move()`` convenience function.

* Added ``--all`` argument to ``purge-batches`` command.

* Added ``ProductCode``, ``Product.codes`` to data model.

* Fixed ``db.cache`` module so as not to require initialization.


0.3a39
------

* Added ``make-user`` command for creating Windows system user account.

* Added avatar image, who knows when that will be useful.
    
  This was created in the hopes it could be used to programmatically set the
  Windows user "tile" image; but that proved unfruitful.

* Changed Linux file monitor to leverage local code instead of ``edbob``.

* Added ``Batch.rows`` property, deprecated ``Batch.iter_rows()``.

* Improved ``sil.Writer.write_rows()``.
    
  This method now allows explicitly specifying the row count, and accepts a
  progress factory.


0.3a38
------

* Changed home folder of system user account to ``/var/lib/rattail``.

* Slight overhaul of Linux file monitor.
    
  This includes the following:
    
  * "More native" Linux file monitor (i.e. less reliant on ``edbob``; current
    code is more or less copied from that project).
  * Addition of ``--pidfile`` command argument on Linux.

* Added (Linux) file monitor configuration to Fabric script.
    
  Also improved ``create_user`` to allow overwriting some settings.

* Fixed file monitor service registration on Windows with ``--auto-start``.

* Fixed "process elevation check" on Windows XP.

* Overhaul of Windows file monitor.
    
  This includes:

  * "More native" Windows file monitor (i.e. less reliant on ``edbob``; current
    code is more or less copied from that project).
  * Improve base class for services, to handle the case where the Windows event
    log is full and can't be written to.  (This prevented the file monitor from
    starting on a machine where the log was full.)


0.3a37
------

* Added ``temp_path()`` function in ``files`` module.


0.3a36
------

* Fixed lingering issues from ``Vendor.contacts`` mapping tweak.


0.3a35
------

* Updated ``repr()`` output for model classes.

* Improved ``find_diffs()`` function.

* Added ``db.model`` module.
    
* Tweaked some ORM mappings.


0.3a34
------

* [feature] Changed some logging instances from ``INFO`` to ``DEBUG``.

  I was just getting tired of the noise.

* [feature] Added ``create_user`` Fabric command.
    
  This creates the ``rattail`` user on a Linux environment.  Probably needs
  some improvement but it's a start.

* [bug] Fixed ``instances_differ()`` function for SQLAlchemy < 0.8.
    
  Presumably the use of ``Mapper.column_attrs`` was not a good idea anyway.
  I'm not quite sure what functionality it adds over ``.columns``.

  (fixes #9)


0.3a33
------

* [general] Tweaked Fabric script to remove egg info before building a
  release.

* [feature] Added ``mail`` module; delegates to ``edbob``.

* [feature] Added ``Session`` to ``db`` module; delegates to ``edbob``.

* [feature] Added ``db.diffs`` module.


0.3a32
------

- Made product cache include *all* costs if so requested.  (Silly oversight.)


0.3a31
------

- [bug] Made change recorder better able to handle new "sets" of related
  objects.  A situation occurred where multiple related objects were being
  introduced to the database within the same session.  Somehow a dependent
  object was being processed first, and its UUID value could not be determined
  since its "upstream" object did yet have one either.  This commit improves
  this situation so that the upstream object will be given an UUID value first,
  if it doesn't yet have one.  The dependent object will then reuse the
  upstream object's UUID as normal.


0.3a30
------

- [feature] Added ``console`` module.  For now this only delegates to
  ``edbob.console``.

- [feature] Added ``get_product_cache()`` function to ``db.cache`` module.
  This is probably the first of many such convenience functions.


0.3a29
------

- [feature] Made Palm conduit unregistration more graceful.  Now this will
  "succeed" even if the conduit isn't actually registered.
  fixes #7

- [feature] Improved Palm conduit (un)registration logic.  Now this can handle
  the case where Hotsync Manager is not installed on the local machine.  The
  code was refactored to make things cleaner also.
  fixes #8

- [feature] Added admin rights check for Palm conduit registration.  Now the
  registration process is checked for an "elevated token" and if none is found,
  a message is displayed and it exits without attempting the registration.
  fixes #3

- [feature] Added admin rights check for Windows file monitor registration.
  Now the registration process is checked for an "elevated token" and if none
  is found, a message is displayed and it exits without attempting the
  registration.
  fixes #5

- [feature] Added ``make-config`` command.  This may need some work yet, to
  better handle the namespace package situation.

- [feature] Added ``Employee.user`` association proxy attribute.

- [feature] Pretend all models and enumerations from ``edbob`` are part of
  ``rattail``.  Some day this will actually be the case.  Client code should be
  able to avoid the ``edbob`` namespace now so that porting will be easier.

- [bug] Fixed issue with recording changes when SQLAlchemy >= 0.8.0.
  Apparently ``RelationshipProperty.remote_side`` is now a ``set`` and doesn't
  support indexing.


0.3a28
------

- [feature] Added ``csvutil`` module.  Currently this only adds some better
  ``DictWriter`` support for Python versions older than 2.7.

- [feature] Added Palm OS app interface.  This adds the Palm HotSync conduit,
  which is used to create CSV files when a handheld running the Rattail app is
  synced with its desktop PC.

- [feature] Added ``files`` module.  This will eventually supercede
  ``edbob.files``, but for now this commit adds only three functions.  These
  just so happened to be ones needed to support some code involving inventory
  count batches.

- [feature] Added ``wince`` module.  This module is used to interface with the
  Rattail app for Windows CE handheld devices.

- [feature] Added new batch system, which will eventually replace the old one.
  Hopefully they can play nicely in parallel, in the meantime.

- [feature] Added `purge-batches` command.  This command will delete forever
  all batches whose purge date has passed.  It is meant to be run on a
  scheduled basis, e.g. nightly.

- [feature] Added "case" value to ``UNIT_OF_MEASURE`` enumeration.

0.3a27
------

- [feature] Added custom `Thread` implementation.  This overrides the default
  behavior of `threading.Thread` by ensuring the system exception hook is
  invoked in case an error occurs within the thread.

0.3a26
------

- [feature] Added `get_product_by_upc()` API function.  This is a convenience
  function which will return a single `Product` instance, or `None`.  It is the
  first of hopefully many API functions.

- [feature] Added SIL columns `F188`, `R71` and `R72`.  These have been added
  to support inventory count batches.

- [bugfix] Fixed `Batch.drop_table()` to handle case where row table doesn't
  exist.  While theoretically this method *shouldn't* encounter a missing
  table, in practice it does happen occasionally.  Now this situation is
  handled gracefully instead of raising an exception.

0.3a25
------

- [bug] Fixed ``Vendor.contacts`` relationship (added 'delete-orphan').

- [feature] Added ``Department.subdepartments`` relationship.

0.3a24
------

- [feature] Added ``__eq__()`` and ``__ne__()`` methods to ``GPC`` class.

- [general] Moved ``GPCType`` SQLAlchemy type class to ``rattail.db`` module.
  This was necessary to make the ``GPC`` class more generally available to
  callers who don't want or need SQLAlchemy to be installed.

- [general] Moved enumerations from database extension to "core" ``enum``
  module.  This is mostly for convenience to callers.

- [bug] Fixed a few bugs with label batches.  These existed mostly because this
  feature hasn't been used in production...

- [feature] Added ``default_format`` attribute to ``LabelFormatter`` class.
  Now when a label profile is edited, this default format is used if no format
  is provided by the user.

- [feature] Changed ``LabelProfile.get_formatter()`` method so that it assigns
  the formatter's ``format`` attribute using the value from the profile.  The
  formatter is free to use or ignore this value, at its discretion.

- [feature] Improved the database synchronizer so that it is *somewhat*
  tolerant of database server restarts.  This likely will need further
  improvement as more testing is done.  The current implementation wraps the
  entire sync loop in a ``try/catch`` block and when a disconnect is detected,
  will wait 5 seconds before re-entering the loop and trying again.

0.3a23
------

- [general] Fixed namespace packages, per ``setuptools`` documentation.

- [feature] Added connection timeout support to ``CommandNetworkPrinter``.

0.3a22
------

- [feature] Added ``LabelProfile.visible`` field.

- [feature] Added generic ``CommandNetworkPrinter`` label printer class.  This
  class sends textual commands directly to a networked printer.

0.3a21
------

- [feature] Refactored database synchronization logic into a proper class,
  which can be overridden based on configuration.

0.3a20
------

- [feature] Tweaked the SIL writer so that it doesn't quote row values when
  they're of data type ``float``.

- [bug] Fixed database sync to properly handle ``Vendor`` deletions.  Now any
  associated ``ProductCost`` records are also deleted, so no more foreign key
  violations.

0.3a19
------

- [bug] Fixed "price toggle" bug in database sync.  It was noticed that
  whenever a product's regular price did not change, yet the product instance
  itself *did* have a change, the regular price association was being removed
  in one sync, then reestablished in the next sync (then removed, etc.).  The
  sync operation now ensures the relationship is removed only when it really
  should be, and that it remains intact when that is appropriate.

0.3a18
------

- [bug] Added special delete logic to the database sync.  Currently, only the
  Department and Subdepartment classes are affected.  When deletions of these
  classes are to be synced between databases, some effort is made to ensure
  that associations with any dependent objects (e.g. Product) are removed
  before the primary instance (e.g. Department) is deleted.

0.3a17
------

- [bug] Added 'delete, delete-orphan' to cascade on ``Product.costs``
  relationship.  This was causing an error when syncing databases.

0.3a16
------

- [bug] Added 'delete, delete-orphan' to cascade on ``Product.prices``
  relationship.  This was causing an error when syncing databases.

0.3a15
------

- [bug] Fixed database sync logic to ensure ``Product`` changes are processed
  before ``ProductPrice`` changes.  Since the underlying tables are mutually
  dependent, the ``dependency_sort()`` call can't *quite* take care of it.  Now
  a lexical sort is applied to the class names before the dependency sort
  happens.  This is somewhat of a hack, merely taking advantage of the fact
  that "Product" comes before "ProductPrice" when lexically sorted.  If other
  mutually-dependent tables come about in the future, this approach may need to
  be revised if their class names don't jive.

0.3a14
------

- [bug] Fixed database synchonization logic to properly handle merging
  ``Product`` instances between database sessions.  Since ``Product`` is so
  interdependent on ``ProductPrice``, a pretty custom merge hack is required.

0.3a13
------

- [bugfix] Fixed ``rattail.db.record_changes()`` so that it also ignores
  ``UserRole`` instance changes if configuration dictates that ``Role`` changes
  are to be ignored.

0.3a12
------

- [bugfix] Fixed foreign key uuid handling in ``rattail.db.record_changes()``.
  Some tables are meant to be used solely as providers of "association proxy"
  fields, the ``uuid`` column is not only a primary key, but also a *foreign
  key* to the "primary" entity table.  In such cases, the uuid value was not
  present at session flush time, so a new one was being generated.
  Unfortunately this meant that the ``Change`` record would point to a
  nonexistent entity record, so the sync would not work.  Now uuid fields are
  inspected to determine if a foreign key is present, in which case the
  relationship is traversed and the true uuid value is used.

- [feature] Added "extra classes" configuration for the ``load-host-data``
  command.  This is necessary when initially populating a "store" (er,
  "non-host") database instance if custom schema extensions are in use (and
  need to be synchronized with the host).

0.3a11
------

- Add R49 SIL column.

- Add ``rattail.pricing`` module.

0.3a10
------

- Ignore batch data when recording changes.

0.3a9
-----

- Bump edbob dependency.

0.3a8
-----

- Tweak database sync.

- Tweak batch processing.

0.3a7
-----

- Add ``Vendor.special_discount``.

0.3a6
-----

- Bump edbob dependency.

0.3a5
-----

- Added ``Store`` and related models.

- Added ``Customer.email_preference`` field.

- Added ``load-host-data`` command.

- Added database changes/synchronization framework.

- Fixed batch table create/drop.

0.3a4r1
-------

- Added ``Product.cost``, ``Product.vendor``.

- Added basic one-up label printing support.

- Added initial batch support, with ``PrintLabels`` provider.

- Added GPC data type.

- Changed internal name of file monitor Windows service.

- Added progress support for label printing.

- Label profiles moved from config to database model.

- Removed ``rattail.db.init_database()`` function.

- Moved some enum values from db extension to core (``rattail.enum`` module).

- Improved SIL support: moved ``rattail.sil`` to subpackage, added ``Writer``
  class etc.

- Fixed file monitor in Linux.

- Added ``delete-orphan`` to ``Vendor.contacts`` relationship cascade.

0.3a4
-----

- Update file monitor per changes in ``edbob``.

0.3a3
-----

- Move database extension to subdir (``rattail.db.extension``).

- Make database extension require ``auth`` extension.

- Fix ``rattail.db.init()``.

- Add lots of classes to database extension model.

- Add ``rattail.labels`` module.

- Add ``rattail.db.cache`` module.

- Add SIL output functions.

- Remove some batch code (for now?).

0.3a2
-----

- Added Windows file monitor service.

0.3a1
-----

-  Refactored to rely on `edbob <http://edbob.org/>`_.  (Most of Rattail's
   "guts" now live there instead.)
