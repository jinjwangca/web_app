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
    if data is not None:
        analyze_gainer(data)
        analyze_loser(data)
        analyze_active(data)
    print(" message processing finished")

def analyze_gainer(data):
    gainer = data["top_gainers"]
    lastupdated = data["last_updated"]
    if gainer is not None:
        move_to_history(lastupdated, gateway.get_data("1","Gainer"), "GainerHistory")
        gateway.delete_all_data("Gainer")
        gateway.add_data("1",gainer,"Gainer")
        print(gateway.get_all_data('Gainer'))

def analyze_loser(data):
    loser = data["top_losers"]
    lastupdated = data["last_updated"]
    if loser is not None:
        move_to_history(lastupdated, gateway.get_data("1","Loser"), "LoserHistory")
        gateway.delete_all_data("Loser")
        gateway.add_data("1",loser,"Loser")
        print(gateway.get_all_data('Loser'))

def analyze_active(data):
    active = data["most_actively_traded"]
    lastupdated = data["last_updated"]
    if active is not None:
        move_to_history(lastupdated, gateway.get_data("1","Active"), "ActiveHistory")
        gateway.delete_all_data("Active")
        gateway.add_data("1",active,"Active")
        print(gateway.get_all_data('Active'))

def move_to_history(lastupdated, data, collection):
    if lastupdated is not None:
        gateway.add_data(lastupdated, data, collection)

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