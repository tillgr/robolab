#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file
import json
import time


class Communication:
    planetName = ""
    receivedMessages = []
    debugMessages = []
    channel = ""

    msg_ready = {
        "from": "client",
        "type": "ready"
    }

    def __init__(self, mqtt_client):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message_catch

        # ADD YOUR VARIABLES HERE
        self.on_connect()

        # choose if on test planet:
        inp = input("planet name: ")
        self.planetName = inp

        if inp == "":
            self.send_message("", self.msg_ready, "explorer/039")
        else:
            msg_testplanet = {
                "from": "client",
                "type": "testplanet",
                "payload": {
                    "planetName": self.planetName
                }
            }
            self.send_message("", msg_testplanet, "explorer/039")
            self.send_message("", self.msg_ready, "explorer/039")
            self.channel = f"planet/{self.planetName}-039"
            # change channel
            self.client.subscribe(self.channel, qos=1)

    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED
    def on_message(self, client, data, message):
        """ Handles the callback if any message arrived """
        print('Got message with topic "{}":'.format(message.topic))
        data = json.loads(message.payload.decode('utf-8'))
        print(json.dumps(data, indent=2))
        print("\n")

        if data["from"] == "server":
            self.receivedMessages.append(data)
            print(self.receivedMessages)
        elif data["from"] == "debug":
            self.debugMessages.append(data)

    # publish a message
    def send_message(self, topic, message, channel):
        """ Sends given message to specified channel """
        self.client.publish(channel, json.dumps(message))

        time.sleep(2)

    # subscribe to server
    def on_connect(self):
        self.client.username_pw_set('039', password='aEraXzm9Xq')  # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/039', qos=1)  # Subscribe to topic explorer/xxx
        self.client.loop_start()

    def on_message_catch(self, client, data, message):
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise

    # quit connection
    def quit_connection(self):
        self.client.loop_stop()
        self.client.disconnect()

    # send path message
    def send_path(self, Xs, Ys, Ds, Xe, Ye, De, status):
        msg_path = {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": Xs,
                "startY": Ys,
                "startDirection": Ds,
                "endX": Xe,
                "endY": Ye,
                "endDirection": De,
                "pathStatus": status
            }
        }

        self.send_message("", msg_path, self.channel)

    def send_pathselection(self, Xs, Ys, Ds):
        msg_pathselection = {
            "from": "client",
            "type": "pathSelect",
            "payload": {
                "startX": Xs,
                "startY": Ys,
                "startDirection": Ds
            }
        }

        self.send_message("", msg_pathselection, self.channel)

        pass

    # deal with received messages
    def get_messages(self):
        return self.receivedMessages

    def clear_messages(self):
        self.receivedMessages.clear()
