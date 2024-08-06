from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Define the metric to count the number of requests
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests')

@app.route('/')
def home():
    # Increment the counter on each request
    REQUEST_COUNT.inc()
    return "Hello, World!"

@app.route('/metrics')
def metrics():
    # Generate the latest metrics in Prometheus format
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    app.run(debug=True)
