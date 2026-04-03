from flask import Flask, Response, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# 🔥 Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP Requests', 
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'Request latency',
    ['endpoint']
)

IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'Number of requests in progress'
)

# 🔹 Home endpoint
@app.route("/")
def home():
    IN_PROGRESS.inc()
    start_time = time.time()

    try:
        time.sleep(random.uniform(0.1, 0.5))  # simulate work
        status = 200
        return "Hello TRAVIS HEAD 🚀"
    finally:
        REQUEST_COUNT.labels(method="GET", endpoint="/", status=status).inc()
        REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)
        IN_PROGRESS.dec()

# 🔹 Error endpoint (for testing alerts)
@app.route("/error")
def error():
    IN_PROGRESS.inc()
    start_time = time.time()

    try:
        time.sleep(0.2)
        status = 500
        return "Something went wrong!", 500
    finally:
        REQUEST_COUNT.labels(method="GET", endpoint="/error", status=status).inc()
        REQUEST_LATENCY.labels(endpoint="/error").observe(time.time() - start_time)
        IN_PROGRESS.dec()

# 🔹 Metrics endpoint
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
