from flask import Flask, request
import json
import clickhouse_connect
import signal


from time import sleep
from threading import Thread
 

app = Flask(__name__)
hostName = "127.0.0.1"
serverPort = 8000

event_manager = ""

class EventManager():
    def __init__(self):
        self.watch_event_counter = 0
        self.watch_event_csv_buffer = ""
        self.client = clickhouse_connect.get_client(host='clickhouse', username='royanegar_user', password='1234')

        daemon = Thread(target=self.periodic_flusher, args=(10,), daemon=True, name='Background')
        daemon.start()

    def new_watch_event(self, event):
        self.watch_event_counter += 1
        self.watch_event_csv_buffer += event
        if (self.watch_event_counter == 100):
            self.flush()

    def periodic_flusher(self, interval_sec):
        while True:
            sleep(interval_sec)
            print('periodic flusher trigerd!')
            self.flush()

    def flush(self):
        print("start flush 'watch_event' logs to clickhouse...")
        self.client.raw_insert(table="watch_event", column_names=["user", "slug", "at"], insert_block=self.watch_event_csv_buffer, fmt="CSV")

        print("watch_event writed to clickhouse, count: ", self.watch_event_counter)

        self.watch_event_counter = 0
        self.watch_event_csv_buffer = ""


def handle_event(req_type, event):
    if (req_type == "application/json"):
        tmpl = "{user},{slug},{at}\n"
        csv_event = tmpl.format(user=event["user"], slug=event["slug"], at=event["at"])
        event_manager.new_watch_event(csv_event)
    else:
        None

@app.route('/', methods=['POST'])
def event():
    req_type = request.headers.get("content-type")
    req_event = request.get_json()
    handle_event(req_type, req_event)
    return "", 204
    

if __name__ == "__main__":
    event_manager = EventManager()

    app.run(host='0.0.0.0', port=serverPort)

    # event_manager.flush()
    
    print("Server stopped.") 