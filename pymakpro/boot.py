import keys
import network
from time import sleep
from simple import MQTTClient

client = None  # Global for client

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)# Creates an instance wlan that is set to station mode 
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.active(True)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)# Connect to Wi-Fi using credentials
        while not wlan.isconnected():
            sleep(1)
        print('Connected on {}'.format(wlan.ifconfig()[0])) # Print the IP of the pico

def setup_mqtt():
    global client
    try:
        print("Setting up MQTT connection...")
        client = MQTTClient('pico_client', '192.168.1.225', user=keys.MQTT_USER, password=keys.MQTT_PASS) #Creates an instance client with given parameters 
        client.connect()#Establishes a TCP connection to the MQTT broker
        client.subscribe('main')#Subscribe to the 'main' topic, not really necessary in this case as the Pico does not receive packets in this implementation
        print("MQTT setup complete")
    except Exception as e:
        print("Failed to setup MQTT: {}".format(e))


connect_wifi()# Connect to Wi-Fi
setup_mqtt()# Set up MQTT client and subscribe to topic

