import communication
import paho.mqtt.client as mqtt
import uuid


client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                     clean_session=False,
                     protocol=mqtt.MQTTv31)

c = communication.Communication(client)
print(c.foo())
