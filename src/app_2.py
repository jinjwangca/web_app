from flask import Flask
from prometheus_client import Counter, Gauge, generate_latest
import time

app = Flask(__name__)

# Define metrics for each endpoint
REQUEST_COUNT_HOME = Counter('http_requests_home_total', 'Total number of HTTP requests for /')
REQUEST_RATE_HOME = Gauge('http_requests_home_rate', 'Rate of HTTP requests per second for /')

REQUEST_COUNT_API = Counter('http_requests_api_total', 'Total number of HTTP requests for /api')
REQUEST_RATE_API = Gauge('http_requests_api_rate', 'Rate of HTTP requests per second for /api')

# Store timestamps and counts for rate calculation
endpoint_metrics = {
    '/': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_HOME, 'rate': REQUEST_RATE_HOME},
    '/api': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_API, 'rate': REQUEST_RATE_API}
}

def update_rate(endpoint):
    metrics = endpoint_metrics[endpoint]
    current_time = time.time()
    elapsed_time = current_time - metrics['last_time']
    request_count = metrics['count']._value.get()

    if elapsed_time > 0:
        rate = (request_count - metrics['last_count']) / elapsed_time
        metrics['rate'].set(rate)

    metrics['last_time'] = current_time
    metrics['last_count'] = request_count

@app.route('/')
def home():
    # Increment the counter for / endpoint
    REQUEST_COUNT_HOME.inc()
    update_rate('/')
    return "Hello from / endpoint!"

@app.route('/api')
def api():
    # Increment the counter for /api endpoint
    REQUEST_COUNT_API.inc()
    update_rate('/api')
    return "Hello from /api endpoint!"

@app.route('/metrics')
def metrics():
    # Generate the latest metrics in Prometheus format
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    app.run(debug=True)
