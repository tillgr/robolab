import json
import paho.mqtt.client as mqtt #import the client
import time

class Communication:
    """
        Class to hold the MQTT client
        Feel free to add functions, change the constructor and the example send_message() to satisfy your requirements and thereby solve the task according to the specifications
    """
    def on_connect(self):
        #client = mqtt.Client(client_id="039", clean_session=False, protocol=mqtt.MQTTv31)
        #client.on_message = on_message # Assign pre-defined callback function to MQTT client
        self.client.username_pw_set('039', password='vasil241') # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/039', qos=1) # Subscribe to topic explorer/xxx
        client.loop_start()
        while True:
	           input('Press Enter to continue...\n')

    def __init__(self, mqtt_client):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message
        self.on_connect()
        self.quit_connection()

        # ADD YOUR VARIABLES HERE

        self.planet_string= '''
            {
                "from":"client",
                "type":"testplanet",
                "payload":
                    {
                        "planetName":"Kashyyyk"
                    }
            }
        '''
    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED
    def on_message(self, client, data, message):
        """ Handles the callback if any message arrived """
        print('Got message with topic "{}":'.format(message.topic))
        data = json.loads(message.payload.decode('utf-8'))
        print(json.dumps(data, indent=2))
        print("\n")

        pass

    def send_message(self, topic, message):
        """ Sends given message to specified channel """
        #msg = json.loads(self.planet_string)
        self.client.publish("explorer/039", payload=self.planet_string, qos=1)
        pass

    def quit_connection(self):
        client.loop_stop()
        client.disconnect()
