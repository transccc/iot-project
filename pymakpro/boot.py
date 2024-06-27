import keys
import network
from time import sleep
from simple import MQTTClient

client = None  # Global client variable

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.active(True)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)
        while not wlan.isconnected():
            sleep(1)
        print('Connected on {}'.format(wlan.ifconfig()[0]))

def setup_mqtt():
    global client
    try:
        print("Setting up MQTT connection...")
        client = MQTTClient('pico_client', '192.168.1.225', user=keys.MQTT_USER, password=keys.MQTT_PASS)
        client.connect()
        client.subscribe('main')
        print("MQTT setup complete")
    except Exception as e:
        print("Failed to setup MQTT: {}".format(e))

# Initialization sequence
connect_wifi()
setup_mqtt()

