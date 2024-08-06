from flask import Flask, request, url_for, render_template, jsonify
import os, logging
from components.DatabaseGateway import DatabaseGateway

print(os.environ.get('PYTHONPATH'))

app = Flask(__name__)

gateway = DatabaseGateway()

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

@app.route('/')
def get_main_page():
    return render_template('main.html')

@app.route('/gainer')
def get_gainer_report():
    data = get_gainer_data()
    lastupdated = get_last_updated()
    print(data)
    return render_template('gainer.html', tickers=data, date=lastupdated )

@app.route('/loser')
def get_loser_report():
    data = get_loser_data()
    lastupdated = get_last_updated()
    print(data)
    return render_template('loser.html', tickers=data, date=lastupdated )

@app.route('/active')
def get_active_report():
    data = get_active_data()
    lastupdated = get_last_updated()
    print(data)
    return render_template('active.html', tickers=data, date=lastupdated )

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify(message='I am healthy')

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello, World!')

if __name__ == "__main__":
    app.run(debug=False, port=8001)