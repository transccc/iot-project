import keys
import network
from time import sleep
from simple import MQTTClient
import machine
import ubinascii
import sys

client = None  # Global client variable

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to network')
        wlan.active(True)
        wlan.config(pm=0xa11140)  # Set WiFi power-saving off (if needed)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)
        print('Waiting for connection...', end='')
        #while not wlan.isconnected() and wlan.status() >= 0:
            #print('.', end='')
            #sleep(1)
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip

def mqtt_callback(topic, msg):
    print(f"Received message from topic {topic.decode('utf-8')}: {msg.decode('utf-8')}")

def connect_mqtt():
    global client
    retries = 5
    client_id = 'pico_client'
    for attempt in range(retries):
        try:
            print(f"Connecting to MQTT broker, attempt {attempt + 1}...")
            port = 1883  
            client = MQTTClient(client_id, '192.168.1.225', port=port, user=keys.MQTT_USER, password=keys.MQTT_PASS)
            client.set_callback(mqtt_callback)
            client.connect()
            client.subscribe('main')  # Subscribe to your topic "main"
            print("Connected to MQTT broker and subscribed to topic 'main'")
            return client
        except Exception as e:
            print(f"Attempt {attempt + 1} of {retries}: Failed to connect to MQTT broker: {e}")
            sleep(2)  # Wait before retrying
    raise Exception("Failed to connect to MQTT broker after multiple attempts")

def disconnect_mqtt():
    if client:
        client.disconnect()
        print("Disconnected from MQTT broker")

# WiFi Connection
try:
    ip = connect_wifi()
except Exception as e:
    print(f"Failed to connect to WiFi: {e}")

# MQTT Connection
try:
    client = connect_mqtt()
    print('MQTT client initialized')
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    client = None

print("boot.py executed")

def main_loop():
    try:
        while True:
            client.check_msg()
            sleep(1)  # Adjust the sleep interval as needed
    except Exception as e:
        print(f"An error occurred: {e}")
        sleep(10)
        machine.reset()

# Terminate any existing instance before running again
if __name__ == "__main__":
    disconnect_mqtt()
    sys.exit() 
