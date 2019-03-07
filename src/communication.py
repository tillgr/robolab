import json
import paho.mqtt.client as mqtt #import the client
import time

class Communication:
    """
        Class to hold the MQTT client
        Feel free to add functions, change the constructor and the example send_message() to satisfy your requirements and thereby solve the task according to the specifications
    """

        # ADD YOUR VARIABLES HERE
    def on_message(self, client, data, message):
        """ Handles the callback if any message arrived """
        print('Got message with topic "{}":'.format(message.topic))
        data = json.loads(message.payload.decode('utf-8'))
        print(json.dumps(data, indent=2))
        print("\n")
        pass
        # Variables
        """
        so now i have to implement the logic with control structures ;)
        data["payload"]["planetname"] --> this is how to get to a inner dictionary
        """
        # so now I have to turn some variables into arrays because of many messages
        self.type = data["type"]
        #
        if self.type == "planet":

            self.planetName = data["payload"]["planetName"]
            #erste Startkoordinaten (add_path)
            self.startX = float(data["payload"]["startX"])
            self.startY = float(data["payload"]["startY"])

        elif self.type == "path":

            #self.startX = float(data["payload"]["startX"])
            #self.startY = float(data["payload"]["startY"])
            self.startDirection = data["payload"]["startDirection"]
            self.endDirection = data["payload"]["endDirection"]
            #korrigierter Endknoten (add_path)
            self.endY = float(data["payload"]["endX"])
            self.endX = float(data["payload"]["endY"])
            #pfadSTATUS und wichtung (add_path)
            self.pathStatus = data["payload"]["pathStatus"]
            self.pathWeight = float(data["payload"]["pathWeight"])

            # erstellen der Karte (add_path)
        elif self.type == "pathUnveiled":
            self.startX = float(data["payload"]["startX"])
            self.startY = float(data["payload"]["startY"])
            self.startDirection = data["payload"]["startDirection"]
            self.endY = float(data["payload"]["endX"])
            self.endX = float(data["payload"]["endY"])
            self.endDirection = data["payload"]["endDirection"]
            self.pathStatus = data["payload"]["pathStatus"]
            self.pathWeight = float(data["payload"]["pathWeight"])
            #pfadauswahl günstigere Richtung (add_path)
        elif self.type == "pathSelect":
            self.startDirection = data["payload"]["startDirection"]

            # target_route
        elif self.type == "target":
            self.targetX = float(data["payload"]["targetX"])
            self.targetY = float(data["payload"]["targetY"])

        # тука съшо трябва да добавя за финалните съобщения логиката !!!
        #self.start_punkt = (self.startX,self.startY)
        #self.end_punkt = (self.endX,self.endY)
        #self.target_punkt = (self.targetX,self.targetY)

    # JSON objects (Templates for messages)
    first_message = '''
        {
        "from": "client",
        "type": "ready"
        }
    '''
    second_message = '''
        {
        "from": "client",
        "type": "path",
        "payload": [
            {
            "startX": "<Xs>",
            "startY": "<Ys>",
            "startDirection": "<Ds>",
            "endX": "<Xe>",
            "endY": "<Ye>",
            "endDirection": "<De>",
            "pathStatus": "free|blocked"
            }
        ]
        }
    '''
    third_message= '''
        {
        "from": "client",
        "type": "pathSelect",
        "payload": [
            {
            "startX": "<Xs>",
            "startY": "<Ys>",
            "startDirection": "<Ds>"
            }
        ]
        }
    '''
    target_reached = '''
        {
            "from": "client",
            "type": "targetReached",
            "payload": [
            {
            "message": "The target was reached successfully "
            }
        ]
        }
    '''
    exploration_completed = '''
            {
                "from": "client",
                "type": "explorationCompleted",
                "payload": ]
                    {
                    "message": "The planet was fully explored"
                    }
            ]
            }
        '''

    def on_connect(self):
            #client = mqtt.Client(client_id="039", clean_session=False, protocol=mqtt.MQTTv31)
            #client.on_message = on_message # Assign pre-defined callback function to MQTT client
        self.client.username_pw_set('039', password='aEraXzm9Xq') # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/039', qos=1) # Subscribe to topic explorer/xxx
        self.client.loop_start()
        self.send_message("","")
        input('Press Enter to continue...\n')
        print(self.planetName)
        print(self.startY)

    def on_message_catch(self, client, data, message):
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise

    def __init__(self, mqtt_client):
            #""" Initializes communication module, connect to server, subscribe, etc. """
            # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message_catch
        self.on_connect()
        #self.quit_connection()

    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED

    def send_message(self, topic, message):
        """ Sends given message to specified channel """
        #msg = json.loads(self.planet_string)
        self.client.publish("explorer/039",self.first_message)
        pass

    def quit_connection(self):
        self.client.loop_stop()
        self.client.disconnect()
