from flask import Flask, request, url_for, render_template, jsonify
from prometheus_client import Counter, Gauge, generate_latest
import time
import os, logging
from components.DatabaseGateway import DatabaseGateway

print(os.environ.get('PYTHONPATH'))

app = Flask(__name__)

gateway = DatabaseGateway()

# Define metrics for each endpoint
REQUEST_COUNT_HOME = Counter('http_requests_home_total', 'Total number of HTTP requests for /')
REQUEST_RATE_HOME = Gauge('http_requests_home_rate', 'Rate of HTTP requests per second for /')

REQUEST_COUNT_GAINER = Counter('http_requests_gainer_total', 'Total number of HTTP requests for /gainer')
REQUEST_RATE_GAINER = Gauge('http_requests_gainer_rate', 'Rate of HTTP requests per second for /gainer')

REQUEST_COUNT_LOSER = Counter('http_requests_loser_total', 'Total number of HTTP requests for /loser')
REQUEST_RATE_LOSER = Gauge('http_requests_loser_rate', 'Rate of HTTP requests per second for /loser')

REQUEST_COUNT_ACTIVE = Counter('http_requests_active_total', 'Total number of HTTP requests for /active')
REQUEST_RATE_ACTIVE = Gauge('http_requests_active_rate', 'Rate of HTTP requests per second for /active')

REQUEST_COUNT_HELLO = Counter('http_requests_hello_total', 'Total number of HTTP requests for /hello')
REQUEST_RATE_HELLO = Gauge('http_requests_hello_rate', 'Rate of HTTP requests per second for /hello')

# Store timestamps and counts for rate calculation
endpoint_metrics = {
    '/': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_HOME, 'rate': REQUEST_RATE_HOME},
    '/gainer': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_GAINER, 'rate': REQUEST_RATE_GAINER},
    '/loser': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_LOSER, 'rate': REQUEST_RATE_LOSER},
    '/active': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_ACTIVE, 'rate': REQUEST_RATE_ACTIVE},
    '/hello': {'last_time': time.time(), 'last_count': 0, 'count': REQUEST_COUNT_HELLO, 'rate': REQUEST_RATE_HELLO}
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

def get_gainer_data():
    return gateway.get_data("1","Gainer")

def get_loser_data():
    return gateway.get_data("1","Loser")

def get_active_data():
    return gateway.get_data("1","Active")

def get_last_updated():
     tradeinfo = gateway.get_data("1","TradeInfo")
     if tradeinfo is not None:
         lastupdated = tradeinfo["last_updated"]
     return lastupdated

@app.route('/metrics')
def metrics():
    # Generate the latest metrics in Prometheus format
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify(message='I am healthy')

@app.route('/')
def get_main_page():
    # Increment the counter for / endpoint
    REQUEST_COUNT_HOME.inc()
    update_rate('/')
    return render_template('main.html')

@app.route('/gainer')
def get_gainer_report():
    # Increment the counter for /gainer endpoint
    REQUEST_COUNT_GAINER.inc()
    update_rate('/gainer')
    data = get_gainer_data()
    lastupdated = get_last_updated()
    print(data)
    return render_template('gainer.html', tickers=data, date=lastupdated )

@app.route('/loser')
def get_loser_report():
    # Increment the counter for /loser endpoint
    REQUEST_COUNT_LOSER.inc()
    update_rate('/loser')
    data = get_loser_data()
    lastupdated = get_last_updated()
    print(data)
    return render_template('loser.html', tickers=data, date=lastupdated )

@app.route('/active')
def get_active_report():
    # Increment the counter for /active endpoint
    REQUEST_COUNT_ACTIVE.inc()
    update_rate('/active')
    data = get_active_data()
    lastupdated = get_last_updated()
    print(data)
    return render_template('active.html', tickers=data, date=lastupdated )

@app.route('/hello', methods=['GET'])
def hello():
    # Increment the counter for /hello endpoint
    REQUEST_COUNT_HELLO.inc()
    update_rate('/hello')
    data = get_active_data()
    return jsonify(message='Hello, World!')

if __name__ == "__main__":
    app.run(debug=False, port=8001)