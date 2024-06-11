import paho.mqtt.client as mqtt

# Define the MQTT broker address and port
broker_address = "192.168.1.165"
port = 1883

# Define the topic to publish to
topic = "example/topic"

# Define the message to publish
message = "Hello, MQTT!"

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message published")

# Create a MQTT client instance
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the broker
client.connect(broker_address, port)

# Publish the message to the topic
client.publish(topic, message)

# Disconnect from the broker
client.disconnect()
