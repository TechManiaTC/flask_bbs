#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

import app

sys.path.insert(0, abspath(dirname(__file__)))
application = app.create_app('development')

"""
建立一个软连接
ln -s /var/www/flask_bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf

ln -s /var/www/flask_bbs/bbs.nginx /etc/nginx/sites-enabled/bbs



➜  ~ cat /etc/supervisor/conf.d/bbs.conf

[program:flask_bbs]
command=/usr/local/bin/gunicorn wsgi --bind localhost:5000 --workers 3 --worker-class gevent
directory=/var/www/flask_bbs
autostart=true
autorestart=true




/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:2001
--pid /tmp/飙泪og.pid
"""
