# Smart Door + 1



## Project Overview
Smart Door + 1 is a project that uses local hosting for real-time analysis of temperature, humidity, and door status. It provides both historical data overview and real-time notifications about the status of a door and its historical status in relation to temperature. The purpose of the project is to monitor the insulation of a room, particularly through the status of one door, and to provide real-time updates about that door. It incorporates humidity as a data point to allow for the analysis of other factors, such as whether a window was opened, without directly monitoring the windows.
.



 **Total Time Estimate**: 10-20 hours. Due to the local hosting nature of this project, the actual time required can vary significantly based on skill level and the number of issues encountered, which may not be covered in this tutorial.

## Objective
I chose to build this project to monitor the temperature and humidity in my room. The project aims to collect data about the room's climate  and analyze how these conditions are influenced by air exchange between my room and the rest of the house. The analysis of that can hence provide insight into the room's insulation, which often causes the temperatures in my room to exceed those outside or in other parts of the house. Additionally, the design includes real-time updates, allowing me to receive notifications about whether the door to my room is open. I used a locally hosted platform because I wanted to learn more about networks and Node-Red. Although the project does not create a multi-client MQTT network, it still a good start. 


## Material

| **Component**                            | **Specification**                                         | **Source**                                                                       |
|-----------------------------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------|
| Raspberry Pi Pico WH                    | Microcontroller                                           | Elektrokit (109 kr)                                                              |
| USB cable A-male - microB-male 1.8m| Cable for connecting Raspberry Pi Pico to computer        | Elektrokit (39 kr) |
| Jumper wires 40-pin 30cm female/male            | Jumper wires for breadboard connections                   | Elektrokit (49 kr)|
| Digital Temperature and Humidity Sensor DHT11(With pull-up resistor) | Measures temperature and humidity                        | Elektrokit (49 kr)                                                               |
| Reed Switch Module Mini                 | Magnetic switch for detecting door open/close state       | Elektrokit (25 kr)                                                               |
| Breadboard                              | Board for connecting electronic components                | Elektrokit (49 kr)                                                               |
| Resistor carbon film 0.25W 330ohm  3x                | Current limiting to keep the power bank active            | Elektrokit (1*3 kr)|
  |  Magnet Neo35 Ø5mm x 5mm                | Magnet for    Reed Switch Module Mini        | Elektrokit (11 kr )|
  |  Jumper wires 40-pin 30cm male/male             | Jumper wires for breadboard connection      | Elektrokit (49 kr )|
  

### Images



## Computer Setup
### Chosen IDE
- - **IDE:** VSCode for its user-friendly interface and its many features, along with my prior experience using it.


### Steps for Computer Setup
1. **Flashing Firmware:**
   - Hold the BOOTSEL button and plug in the Pico WH with the USB cable.
   - Drag the [firmware file](https://micropython.org/download/RPI_PICO_W/) into the drive that pops up (RPI-RP2).

2. **Installation:**
   - Install [VSCode](https://code.visualstudio.com/download).
   - Install [Node.js](https://nodejs.org/en).
   - Install Pymakr in VSCode:
     - Open VSCode and click on the extension tab on the left-hand side.
     - Search for "Pymaker" and install it.
     - On the left-hand side, a new icon for Pymakr should appear. Click on it and select "Create Project".
     - Create a folder and then select "Use this folder". A window will appear asking for the project name. Enter your desired project name, then select "empty" when asked for a template.
     - Click "Add Device" located under the empty project in the Pymakr tab, then select your device and click "OK".
     - Selecting the lighting icon and then selecting development mode in Pymakr will now automatically upload the files to the device.
## Putting Everything Together
### Circuit Diagram
![Alt text](https://github.com/transccc/iot-project/blob/main/Screenshot%202024-06-29%20002548.png)

Additionally, use female-to-male wires to connect the reed switch at an appropriate location where the magnet can detect when the door is closed.
### Electrical Calculations
- I needed to add 3 extra 330 ohm resistors for the power bank to recognize the device as drawing power. These 3 resistors were added in parallel, as seen in the image above. 

  With the help of:

  $\frac{1}{R_{\text{total}}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3}$

  For three 330 ohm resistors:

  $\frac{1}{R_{\text{total}}} = \frac{1}{330} + \frac{1}{330} + \frac{1}{330}$

  $\frac{1}{R_{\text{total}}} = \frac{3}{330}$

  $R_{\text{total}} = \frac{330}{3} = 110 \ \Omega$

  Using Ohm's Law ($V = IR$)  and V = 5 V:

  $I = \frac{V}{R} = \frac{5V}{110 \, \Omega} \approx 45.45 \ mA$

This current draw is sufficient for the power bank to recognize the device as active and continuously supply power. Additionally, given the voltage, the power dissipation across the resistors is well within safe limits, preventing any risk of damage. The power bank can supply a maximum current of 2 A, which is more than adequate for this setup.





## Platform
### Choice of Platform
I used Node-Red and InfluxDB as the main platforms for this project. Node-Red provides real-time data analysis with the help of its flow. It is a locally hosted platform with many options, allowing the creation of a full dashboard and data storage with InfluxDB, along with direct HTTP POST requests to Pushbullet. The data is sent using a local MQTT broker for easy integration with Node-Red. At first, I considered using the Node-Red UI for visualisation, but I chose not to because it could not easily provide a aesthetically pleasing dashboard and had no data storage capabilities. 
## The Code
### Set up Wi-Fi and MQTT credentials 
- In the code boot.py you may notice that there are keys
  ```
  def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.active(True)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)
        while not wlan.isconnected():
            sleep(1)
        print('Connected on {}'.format(wlan.ifconfig()[0]))
  ```
- Create a separate file named keys.py where wlan.connect can use to connect to the Wi-Fi. The same goes for the MQTT connection in:
  ```
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
  ```
 -  Add MQTT_USER and MQTT_PASS in the keys.py file so that MQTTClient() gets the required parameters and thereby can subscribe. It is also important to note that the client, which is the pico_client, subscribes to the topic 'main'. It is hence important to set up the topic to match the one the broker is creating. Both the MQTT_PASS and MQTT_USER are important to note for future instructions, as they are the security parameters that the broker should also be set up with accordingly.
  
### Setting Up Mosquitto and Node-RED for MQTT Communication

### 1. Download and Install Mosquitto

First, download [Mosquitto](https://mosquitto.org/download/).

After downloading, locate the `mosquitto.conf` file in the newly created Mosquitto folder and add the following lines at the end:
```
listener 1883
allow_anonymous false
password_file C:\Program Files\Mosquitto\passwd
```
### ⚠️ Firewall Configuration

When setting up Mosquitto as your MQTT broker, ensure that your firewall is configured to allow traffic on the default MQTT port 1883. Failure to do so can prevent devices and clients from connecting to the broker.

### 2. Install Node-RED

Next, install Node-RED by running the following command in the Command Prompt:

```
npm install -g --unsafe-perm node-red
```

### 3. Download and Execute the Bash Script

After this, you can easily download the provided bash script [here](https://github.com/transccc/iot-project/blob/main/mosquitto_bash_script). This script allows you to seamlessly start up Mosquitto and Node-RED by providing a username, password, and topic. Remember the MQTT_USER, MQTT_PASS, and topic "main" from earlier? These should match the values that you plug into the script. These details will also be used in localhost:1880 when creating the MQTT input node in Node-RED.

- **Download the script**: Click [here](https://github.com/transccc/iot-project/blob/main/mosquitto_bash_script) to download the bash script to your local machine.
- **Execute the script**:
  - Open your terminal.
  - Navigate to the directory where the script is downloaded.
  - Run the script with the command:  
    ```
    bash mosquitto_bash_script.sh
    ```
  - The script will prompt you to enter a username, password, and topic. Note these details as they will be needed later.

### 4. Set Up Node-RED

Configure Node-RED to work with your MQTT setup:

- **Open Node-RED**: In your web browser, go to `localhost:1880`.
- **Import the Node-RED Flow**: Download the Node-RED flow from [here](https://github.com/transccc/iot-project/blob/main/node-red_flow).
  - In Node-RED, use the import function to import the flow file.
- **Configure the MQTT Input Node**:
  - Locate the MQTT input node in the imported flow, double-click to edit its properties, and update the username, password, and topic fields to match the values provided in the bash script.

### 5. Set Up Notifications via HTTP Request in Node-RED

To enable notifications, you will use Pushbullet to send messages. Follow these steps:

- **Create a Pushbullet Account**:
  - Go to the [Pushbullet website](https://www.pushbullet.com/).
  - Sign up for a new account.
- **Generate a Pushbullet Token**:
  - Once logged in, navigate to your account settings.
  - Generate an access token. This token will be used to authenticate your requests.
- **Configure Node-RED for Pushbullet Notifications**:
  - In Node-RED, add go to the Door open functions 

  - Use the following command:
    ```
    curl -u "YOUR_ACCESS_TOKEN_HERE:" https://api.pushbullet.com/v2/users/me
    ```
    This will provide the necessary information to fill out the notification functions in node-red.
### Setting Up InfluxDB

Follow these steps to download, install, and configure InfluxDB, and integrate it with Node-RED:

1. **Download and Install InfluxDB**:
   - Go to the [InfluxData Downloads page](https://www.influxdata.com/downloads/).
   - Select the appropriate version for your operating system and follow the instructions to download and install InfluxDB.

2. **Launch InfluxDB**:
   - Start InfluxDB by running the appropriate command for your operating system. For example, on Windows:
     ```
     influxd
     ```
    - or by simply running the .exe file directly


3. **Access InfluxDB UI**:
   - Open your web browser and go to `http://localhost:8086`.
   - Follow the on-screen instructions to set up your InfluxDB instance.

4. **Create an Account and Configure InfluxDB**:
   - Create an account by providing the necessary details.
   - Set up your organization and save the organization name.
   - Create a bucket and save the bucket name.
   - Generate an API token and save it for future use.

5. **Configure InfluxDB in Node-RED**:
   - Open Node-RED in your web browser (`http://localhost:1880`).
   - Open the InfluxDB node and configure it:
     - **Server**: Enter `http://localhost:8086`.
     - **Token**: Enter the API token you generated.
     - **Organization**: Enter the organization name.
     - **Bucket**: Enter the bucket name.

- For more detailed instructions and troubleshooting, refer to the [InfluxDB Documentation](https://docs.influxdata.com/influxdb/v2.0/get-started/) and [Node-RED Documentation](https://nodered.org/docs/).
 ### Core functionalites of the code
The `main_loop()` function orchestrates the core operations of the device, including blinking the LED, checking the reed switch status, reading temperature and humidity from the DHT11 sensor, and publishing this data to an MQTT broker.
```
  while True:
        try:
            # Blink the LED to indicate the loop is running
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
```
The LED blinks on and off to indicate that the loop is running. This provides a visual confirmation that the device is active.
python
```
            current_reed_status = read_reed_switch()
            reed_status = "50" if current_reed_status else "0"
```
The function read_reed_switch() is called to check the current status of the reed switch. The reed_status is set to "50" if the reed switch is active (door open) and "0" if it is inactive (door closed).
```
dht11.measure()
            temperature_dht11 = dht11.temperature()
            humidity_dht11 = dht11.humidity()
```
The dht11.measure() function reads the current temperature and humidity values from the DHT11 sensor. The values are stored in temperature_dht11 and humidity_dht11.
The rest of the code can be found in the [project repository](https://github.com/transccc/iot-project/tree/main/pymakpro)
## Transmitting the Data / Connectivity
### Data Transmission Details
Wifi is used primaliy used in this projet to connect devices within the network. This is connection is done trough a central hub: The Wi-Fi router. The project also uses wifi for the HTTP post request, which instead sends the data to the router then to the Pushbullet which then sends the message as a notfication to my phone. As seen in the previously mentioned code, the code operates trough
```
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.active(True)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)
        while not wlan.isconnected():
            sleep(1)
        print('Connected on {}'.format(wlan.ifconfig()[0]))
```
which 
```
wlan = network.WLAN(network.STA_IF)
```
Creates an instance of the wlan from the WLAN class with the help of STA-IF that is a parameter that sets the device to station mode, i.e connecting mode. 
```
wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)
```
Uses the ID and Password of the network to connect to the network
```
print('Connected on {}'.format(wlan.ifconfig()[0]))
```
Gives the ip adress of the Pico in the network 
<br>
<br>
As previously seen in the code section, MQTT is used to transmit data to a broker, specifically a local broker using Mosquitto. This process involves connecting to Wi-Fi and then to the MQTT broker on the local host. The client publishes messages to this broker in the form of a JSON payload.

The payload includes temperature, humidity, and reed switch status data:
```
 payload = {
                "temperature": temperature_dht11,
                "humidity": humidity_dht11,
                "reed_status": reed_status
            }
payload_json = ujson.dumps(payload)
```
This JSON payload is then published to the MQTT broker as follows:

```
  if boot.client:
                boot.client.publish('main', payload_json)
                print("Published:", payload_json)
            else:
                print("MQTT client is not initialized")
```
The broker manages topics, and clients subscribe to get messages. In this project, both Node-RED and the Pico subscribe to the main topic. When the Pico sends a message, the local Mosquitto broker makes sure Node-RED gets it. Node-RED then handles the message. The data from the Pico is in JSON format, with readings from the DHT11 sensor (temperature and humidity) and the status of the reed switch. These JSON messages are sent every three seconds. MQTT handles real-time data, key for apps needing quick updates and responses. Using a local broker like Mosquitto boosts security and cuts latency as the data stays in the local network. This setup is also higly customisable  Node-RED receives the data from the Pico and processes this information in various ways. For instance, Node-RED can redirect the incoming data to InfluxDB for storage and visualization, allowing for analysis and monitoring of the sensor data over time and in real-time. Node-RED can also send real-time notifications via HTTP post requests to Pushbullet, providing alerts about whether the door is open. This versatility is the key reason for the usage of node-red, all locally hosted, quick and analysable 

- **Wireless Protocols:** WiFi for local transmission.
- **Transport Protocols:** MQTT for efficient, low-overhead communication, HTTP to Pushbullet for real-time notfications. 

### Design Choices
- **Data Transmission:** Chose MQTT for its lightweight protocol, suitable for IoT. Additionally, HTTP is used to send notifications to Pushbullet, ensuring timely alerts.
- **Wireless Protocols:** WiFi provides sufficient range and speed for this application, considering the local environment.

## Presenting the Data
### Configuring a Dashboard in InfluxDB

Follow these steps to set up and customize a dashboard in InfluxDB to visualize your sensor data:

1. **Access Dashboards**:
   - Click on "Dashboards" on the left-hand side menu in InfluxDB.

2. **Remove Unnecessary Cells**:
   - Review the default cells in the dashboard.
   - Remove any cells that you find unnecessary by clicking the trash icon or using the cell's menu options.

3. **Add a New Panel**:
   - Click on the "+ Add Cell" button to add a new panel.
   - Choose the "Graph" option for visualizing time-series data.

4. **Configure the Panel**:
   - Click on the newly added panel to configure it.
   - In the configuration options, select the bucket that you connected to Node-RED.

5. **Select Measurement and Fields**:
   - Click on `_measurement` and select `sensor_data`.
   - In the field window, select the fields `reed_status`, `humidity`, and `temperature`.

6. **Visualize Data**:
   - Adjust the settings as necessary to optimize the visualization.
   - You should now see a graph displaying temperature data over time.
### Dashboard
- **Visualization:** InfluxDB dashboard showing real-time temperature, humidity and reed switch data.
- **Data Storage:** Data saved in InfluxDB, preserved indefinitely for historical analysis.
- **Database Choice:** InfluxDB chosen for its time-series data handling capabilities and dashboard functionality.
- **Automation:** Alerts and triggers set up when the door opens. Node-Red automatically sends HTTP POST requests to Pushbullet for real-time notifications when the door opens and closes.
## Implementation Details
Initially, I used the MQTT broker and set it up to start first in a batch file. This allows the localhost to easily open both Node-Red and the broker, and it also creates a topic.

This setup, however, did not solve the issue regarding the client startup with the sensors, which I decided to handle manually. I configured Node-Red to create a graph, aiming for consistency despite the unstable internet connection for my Pico. I also added a collision sensor to measure temperature and detect if the door closes.

The collision sensor was used because I lacked a strong enough magnet for a magnetic sensor. I realized that the collision sensor only sent one signal and would need separate threading to detect movement, leading to program inconsistencies. Due to my inexperience with multithreading, this likely corrupted the files, making the program unable to run.

After a hard reset, I switched to using a magnet, which worked. I had initially assumed the magnet was too weak due to a minor mistake. Removing the collision sensor also reduced power consumption and potential failure points.

I figured out that MQTT connection inconsistency might be due to ID conflicts when the program is already running with a connected ID. The broker maintains the session if the device is already connected. A duplicate connection attempt with the same client ID may be refused. Reconnecting after unplugging and replugging the device resolves the conflict.

Additionally, I realized I forgot to use `sys.exit()`, which helped terminate running instances, allowing the program to run as intended and consistently connect to the MQTT broker. Using the magnet avoided multithreading issues, though it didn't entirely resolve the MQTT problems, it was still an improvement.

Using JSON packages and debug nodes, I was able to print the following results:
### Different Platforms Discussed

