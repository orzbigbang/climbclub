from uvicorn.config import Config
import multiprocessing


cores = multiprocessing.cpu_count()
workers_per_core = 1
default_web_concurrency = workers_per_core * cores
web_concurrency = max(default_web_concurrency, 2)


class UvicornConfig(Config):
    host = "0.0.0.0"
    port = 8080
    loop = "uvloop"
    proxy_headers = True


def worker_init(worker):
    worker.cfg = UvicornConfig("main:app")


bind = "0.0.0.0:8080"
loglevel = "info"
accesslog = "-"
errorlog = "-"
workers = web_concurrency
worker_class = "uvicorn.workers.UvicornWorker"
worker_tmp_dir = "/dev/shm"
graceful_timeout = 120
timeout = 120
keepalive = 5
