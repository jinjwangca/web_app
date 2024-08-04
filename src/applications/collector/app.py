from flask import Flask, request, Response, url_for, render_template
from flask_restful import Resource, Api
from components.DatabaseGateway import DatabaseGateway
import requests
import pika, os, logging
import schedule
import time

print(os.environ.get('PYTHONPATH'))

app = Flask(__name__)

gateway = DatabaseGateway()

def send_rabbit_mq(message):
    queue_name = "analyzer"
    url = os.getenv("RABBITMQURL", "")
    try:
        params=pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message)
        print ("[x] Message sent to consumer")
        connection.close()
    except Exception as e:
        print(e)
        pass

def retrieve_trade_info():
    url = os.getenv("TRADEINFOURL", "")
    r = requests.get(url)
    data = r.json()
    print(data)
    return data

def save_trade_info(data):
    if data is not None:
        gateway.delete_all_data("TradeInfo")
        gateway.add_data("1",data,"TradeInfo")
    return data

@app.route('/collect', methods=['POST'])
def collect_trade_info():
    print("retrieving trade info")
    data = retrieve_trade_info()
    print("saving trade info to database")
    save_trade_info(data)
    print("sending message to rabbit mq")
    send_rabbit_mq("analyze")

if __name__ == '__main__':
    schedule.every().day.at("18:00").do(collect_trade_info)
    #schedule.every(1).minutes.do(collect_trade_info)
    while True:
        schedule.run_pending()  # Run all scheduled jobs
        time.sleep(10)
    #app.run(debug=False, port=8002)