from flask import Flask, request, url_for, render_template
import os, logging
from dotenv import load_dotenv
from components.DatabaseGateway import DatabaseGateway

print(os.environ.get('PYTHONPATH'))

app = Flask(__name__)

gateway = DatabaseGateway()

@app.route('/')
def get_main_page():
    return render_template('main.html')

@app.route('/gainer')
def get_gainer_report():
    data = gateway.get_data("1","Gainer")
    tradeinfo = gateway.get_data("1","TradeInfo")
    if tradeinfo is not None:
        lastupdated = tradeinfo["last_updated"]
    print(data)
    return render_template('gainer.html', tickers=data, date=lastupdated )

@app.route('/loser')
def get_loser_report():
    data = gateway.get_data("1","Loser")
    tradeinfo = gateway.get_data("1","TradeInfo")
    if tradeinfo is not None:
        lastupdated = tradeinfo["last_updated"]
    print(data)
    return render_template('loser.html', tickers=data, date=lastupdated )

@app.route('/active')
def get_active_report():
    data = gateway.get_data("1","Active")
    tradeinfo = gateway.get_data("1","TradeInfo")
    if tradeinfo is not None:
        lastupdated = tradeinfo["last_updated"]
    print(data)
    return render_template('active.html', tickers=data, date=lastupdated )

if __name__ == "__main__":
    app.run(debug=False, port=8001)