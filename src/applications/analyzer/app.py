from flask import Flask, request, Response
from flask_restful import Resource, Api
from components.DatabaseGateway import DatabaseGateway
import requests
import pika, sys, os, time

print(os.environ.get('PYTHONPATH'))

app = Flask(__name__)

gateway = DatabaseGateway()

def callback(ch, method, properties, body):
    print("processing trade info")
    print(f"Received {body}")
    data = gateway.get_data("1","TradeInfo")
    print(data)
    gainer = data["top_gainers"]
    print("----------------------------")
    if gainer is not None:
        gateway.delete_all_data("Gainer")
        gateway.add_data("1",gainer,"Gainer")
        print(gateway.get_all_data('Gainer'))
    print("----------------------------")
    loser = data["top_losers"]
    if loser is not None:
        gateway.delete_all_data("Loser")
        gateway.add_data("1",loser,"Loser")
        print(gateway.get_all_data('Loser'))
    print("----------------------------")
    active = data["most_actively_traded"]
    if active is not None:
        gateway.delete_all_data("Active")
        gateway.add_data("1",active,"Active")
        print(gateway.get_all_data('Active'))
    print(" message processing finished")

def consume_rabbit_mq():
    url = os.getenv("RABBITMQURL", "")
    queue_name = "analyzer"
    try:
        params=pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(queue_name, callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        connection.close()
    except Exception as e:
        pass

@app.route('/analyze', methods=['POST'])
def analyze_trade_info():
    consume_rabbit_mq()

if __name__ == '__main__':
    analyze_trade_info()
    #app.run(debug=False, port=8003)