from flask import Flask, request
from confluent_kafka import Producer
import os

server_port = value = os.getenv("PORT") 
kafka_servers = value = os.getenv("KAFKA_SERVERS") 

app = Flask(__name__)
producer = Producer({'bootstrap.servers': kafka_servers})

def handle_event(req_type, event):
    if (req_type == "application/json"):
        tmpl = "{user},{slug},{at}\n"
        csv_event = tmpl.format(user=event["user"], slug=event["slug"], at=event["at"])
        producer.produce("watch_events", csv_event)
    else:
        None

@app.route('/', methods=['POST'])
def event():
    req_type = request.headers.get("content-type")
    req_event = request.get_json()
    handle_event(req_type, req_event)
    return "", 204
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=server_port)
    