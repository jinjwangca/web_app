from flask import Flask, request, Response, url_for, render_template
from flask_restful import Resource, Api
from components.DatabaseGateway import DatabaseGateway
import requests
import pika, os, logging

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

@app.route('/collect', methods=['GET'])
def collect_trade_info():
    url = os.getenv("TRADEINFOURL", "")
    r = requests.get(url)
    data = r.json()
    if data is not None:
        gateway.delete_all_data("TradeInfo")
        print("all records deleted from TradeInfo")
        print(gateway.get_all_data('TradeInfo'))
        gateway.add_data("1",data,"TradeInfo")
        print("before send rabbit mq")
        send_rabbit_mq("analyze")
    return data

if __name__ == '__main__':
    collect_trade_info()
    #app.run(debug=False, port=8002)