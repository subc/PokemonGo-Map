import multiprocessing

# Server Socket
bind = 'unix:/run/gunicorn.sock'
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 500
timeout = 10
keepalive = 3
debug = True
spew = False

# Logging
logfile = '/var/log/gunicorn/app.log'
loglevel = 'debug'
#logconfig = '/var/flask/matome/matome/config/gunicorn/gunicorn-log.conf'

# Process Name
proc_name = 'gunicorn_app'


