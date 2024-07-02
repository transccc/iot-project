import time
import machine
from machine import Pin
from dht import DHT11
import ujson
import boot

# DHT11 sensor 
dht11_pin = machine.Pin(27)
dht11 = DHT11(dht11_pin)

# Reed Switch 
reed_switch_pin = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

#OUTPUT pin to pico LED
led = Pin("LED", Pin.OUT)

def read_reed_switch():
    return reed_switch_pin.value() == 0  # Reed switch is active when the magnet is close
#50 = DOOR IS OPEN
#0 = DOOR IS CLOSED

def main_loop():
    reed_status = "50"
    while True:
        try:
            # Blink the LED to indicate the loop is running
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
            
            # Read the reed switch
            current_reed_status = read_reed_switch()
            if current_reed_status:
                 reed_status = "50"
            else:
                reed_status = "0"
            # Read DHT11 temperature and humidity
            dht11.measure()
            temperature_dht11 = dht11.temperature()
            humidity_dht11 = dht11.humidity()
            print(f"DHT11 Temperature: {temperature_dht11} °C, Humidity: {humidity_dht11}%, Reed Status: {reed_status}")
            
            # JSON payload
            payload = {
                "temperature": temperature_dht11,
                "humidity": humidity_dht11,
                "reed_status": reed_status
            }
            payload_json = ujson.dumps(payload)  # Convert payload to JSON string 
            
            if boot.client:
                boot.client.publish('main', payload_json) # Publish the payload 
                print("Published:", payload_json)
            else:
                print("MQTT client is not initialized")
            
        except OSError as e:
            print(f"Failed to read from DHT11 sensor: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(2)

try:
    if boot.client:     # Check client
        main_loop()
    else:
        print("MQTT client is not initialized")
except Exception as e:
    print(f"ERROR {e}")
    time.sleep(10)
finally:
    if boot.client:
        boot.client.disconnect()
