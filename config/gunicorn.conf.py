# config/gunicorn.conf.py
import multiprocessing
import os

# Worker configuration
workers = 2
threads = 4
worker_class = "gthread"

# Timeout settings - INCREASED for image processing
timeout = 120  # increased from 30 to 120 seconds for image processing
graceful_timeout = 120
keep_alive = 5

# Memory optimization
max_requests = 500  # reduced from 1000 to 500
max_requests_jitter = 50
preload_app = True

# File upload limits
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

def when_ready(server):
    print("Gunicorn is ready!")