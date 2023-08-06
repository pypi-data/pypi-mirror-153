## -*- mode: conf; -*-

<%text>############################################################</%text>
#
# ${app_title} web app
#
<%text>############################################################</%text>


<%text>##############################</%text>
# rattail
<%text>##############################</%text>

[rattail.config]
require = %(here)s/rattail.conf


<%text>##############################</%text>
# pyramid
<%text>##############################</%text>

[app:main]
use = egg:${pyramid_egg}

# TODO: you should disable these first two for production
pyramid.reload_templates = true
pyramid.debug_all = true
pyramid.default_locale_name = en
# pyramid.includes = pyramid_debugtoolbar

beaker.session.type = file
beaker.session.data_dir = %(here)s/sessions/data
beaker.session.lock_dir = %(here)s/sessions/lock
beaker.session.secret = ${beaker_secret}
beaker.session.key = ${beaker_key}

pyramid_deform.tempdir = %(here)s/data/uploads

exclog.extra_info = true

# required for tailbone
rattail.config = %(__file__)s

[server:main]
use = egg:waitress#main
host = ${pyramid_host}
port = ${pyramid_port}

# NOTE: this is needed for local reverse proxy stuff to work with HTTPS
# https://docs.pylonsproject.org/projects/waitress/en/latest/reverse-proxy.html
# https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html
# trusted_proxy = 127.0.0.1

# TODO: leave this empty if proxy serves as root site, e.g. http://rattail.example.com/
# url_prefix =

# TODO: or, if proxy serves as subpath of root site, e.g. http://rattail.example.com/backend/
# url_prefix = /backend


<%text>##############################</%text>
# logging
<%text>##############################</%text>

[handler_console]
level = INFO

[handler_file]
args = (${repr(os.path.join(appdir, 'log', 'web.log'))}, 'a', 1000000, 100, 'utf_8')
