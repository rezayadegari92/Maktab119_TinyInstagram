# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8004"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
worker_connections = 1000
threads = 4
max_requests = 1000
max_requests_jitter = 50

# Timeout
timeout = 120
keepalive = 10

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Process naming
proc_name = "tiny_instagram"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (for production)
keyfile = None
certfile = None

# Application
wsgi_module = "core.wsgi:application"
worker_tmp_dir = "/dev/shm"

# Reload
reload = False
reload_engine = "auto"

# Development vs Production
if os.getenv('DEBUG', 'False') == 'True':
    reload = True
    workers = 2
    loglevel = "debug"
else:
    reload = False
    workers = multiprocessing.cpu_count() * 2 + 1
    loglevel = "info"
