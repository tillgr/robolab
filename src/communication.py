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
        self.client.username_pw_set('039', password='aEraXzm9Xq') # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/039', qos=1) # Subscribe to topic explorer/xxx
        self.client.loop_start()
        self.send_message("","")



        '''
        while True:
            self.send_message1("","")
            input('Press Enter to continue...\n')
        '''



    def __init__(self, mqtt_client):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message
        self.on_connect()
        time.sleep(2)
        self.quit_connection()

        # ADD YOUR VARIABLES HERE

        planetName="Kashyyyk" #receives planet name
        type=""  #receives path or planet
        #Coordinates
        startX=""  #punkt = f"x:{startX}"
        startY=""
        start_punkt=('startX','startY','startDirection')
        endY=""
        endX=""
        end_punkt=('endX','endY')
        targetX=""
        targetY=""
        target_punkt=('targetX','targetY')
        #Directions in degrees
        #NORTH = 0
        #EAST = 90
        #SOUTH = 180
        #WEST = 270
        startDirection=""
        endDirection=""

        pathStatus="" #receives blocked|free
        pathweight="" #when blocked (-1) ,when free (>0)



    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED
    def on_message(self, client, data, message):
        """ Handles the callback if any message arrived """
        print('Got message with topic "{}":'.format(message.topic))
        data = json.loads(message.payload.decode('utf-8'))
        print(json.dumps(data, indent=2))
        print("\n")

        pass

    def send_message1(self, topic, message):
        """ Sends given message to specified channel """
        #msg = json.loads(self.planet_string)
        self.client.publish("Kashyyyk-039",'{"from": "client","type": "path","payload": {"startX": "<Xs>","startY": "<Ys>","startDirection": "<Ds>","endX": "<Xe>","endY": "<Ye>","endDirection": "<De>","pathStatus": "free|blocked" }}')
        #'{"from":"client","type":"testplanet","payload":{planetName}')
        pass

    def send_message(self, topic, message):
        """ Sends given message to specified channel """
        #msg = json.loads(self.planet_string)
        self.client.publish("explorer/039",'{"from": "client","type": "ready"}')
        pass

    def quit_connection(self):
        self.client.loop_stop()
        self.client.disconnect()
