# mqtt client
import json
import paho.mqtt.client as paho

class MQTTClient():

    def __init__(self, topic, host="localhost", port=1883):
        self.host = host
        self.port = port
        self.id = 123 #placeholder

    def on_log(self, client, obj, level, string):
        print(string)

    def on_publish(self, client, userdata, mid):
        print ("published updates")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(len(msg.payload)))
        self.process_message(json.loads(msg.payload))

    def _send_msg(self, topic, msg, retain = False):
        (rc, mid) = self.client.publish(topic, msg, qos=1, retain=retain)

    def process_message(self, msg):
        raise NotImplementedError()

    def subscribe(self, topic):
        self.client.subscribe(topic, qos = 1)

    def _connect(self):
        self.client = paho.Client(self.id) #expects an id.
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.connect(self.host, self.port, keepalive=600)

    def _start(self):
        self.client.loop_forever()
