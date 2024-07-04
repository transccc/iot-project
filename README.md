# Smart Door + 2
**Author**: Per Karlsson Kremer (pk222yh)


## Project Overview
Smart Door + 2 is a project that uses local hosting for real-time analysis of temperature, humidity, and door status. It provides both historical data overview and real-time push notifications about the status of a door and its historical status in relation to temperature. The purpose of the project is to monitor the insulation of a room, particularly through the status of one door, and to provide real-time updates about that door. It incorporates humidity as a data point to allow for the analysis of other factors, such as whether a window was opened, without directly monitoring the windows.
.



 **Total Time Estimate**: 5-15 hours. Due to the local hosting nature of this project, the actual time required can vary significantly based on skill level and the number of issues encountered, which may not be covered in this tutorial.

**OS**: Windows 11

## Objective
I chose to build this project to monitor the temperature and humidity in my room. The project aims to collect data about the room's climate  and analyze how these conditions are influenced by air exchange between my room and the rest of the house. The analysis of that can hence provide insight into the room's insulation, which often causes the temperatures in my room to exceed those outside or in other parts of the house. Additionally, the design includes real-time updates, allowing me to receive push notifications about whether the door to my room is open. I used a locally hosted platform because I wanted to learn more about networks and Node-Red. Although the project does not create a multi-client MQTT network, it still a good start. 


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
  |  Power bank            | Power source     | Depends|
  





## Computer Setup
### Chosen IDE
-  **IDE:** VSCode for its good UI and its many features, along with my prior experience using it.


### Steps for Computer Setup
1. **Flashing:**
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
![Alt text](https://github.com/transccc/iot-project/blob/main/pictures/Screenshot%202024-06-29%20002548.png)

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
I used Node-Red and InfluxDB as the main platforms for this project. Node-Red provides real-time data analysis with the help of its flow. It is a locally hosted platform with many options, allowing the creation of a full dashboard and data storage with InfluxDB, along with direct HTTP POST requests to Pushbullet. The data is sent using a local MQTT broker for easy integration with Node-Red. At first, I considered using the Node-Red UI for visualisation, but I chose not to because it could not easily provide a aesthetically pleasing dashboard and had no storage capabilities of itself. MQTT, which intigrates with Node-RED, operates on a publish/subscribe model. A client publishes "packets" to a specific topic, and these packets are then received by all clients that have subscribed to that topic. In this case the Pico sends data to the same topic that Node-RED is subscribed to. Node-RED then in turn handles the data to send it to InfluxDB and Pushbullet. For a more in-depth explanation, refer to the connectivity section of this tutorial. The following section will explain how to set up the broker, which acts as the central hub for managing subscriptions and client communications.
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
 -  Add MQTT_USER and MQTT_PASS to the keys.py file so that MQTTClient() can use these credentials to connect to the broker. The client, which is pico_client, subscribes to the "main" topic in my code, but this can be omitted if the Pico only needs to publish data, as only the TCP connection established by client.connect() is required to publish. Both MQTT_USER and MQTT_PASS are important for future instructions as they serve as security credentials that must match the broker's configuration, as does the topic "main".
  
### Setting Up Mosquitto and Node-RED for MQTT Communication

### 1. Download and Install Mosquitto

First, download [Mosquitto](https://mosquitto.org/download/).

After downloading, locate the "mosquitto.conf" file in the newly created Mosquitto folder with admin and add the following lines at the end:
```
listener 1883
allow_anonymous false
password_file C:\Program Files\mosquitto\passwd
```
After configuring the configuration file, create a file named "passwd".

Then, open the Command Prompt as an administrator and navigate to the Mosquitto folder with:
```
cd "C:\Program Files\mosquitto"
```
Execute mosquitto_passwd by typing: 
```
mosquitto_passwd -H sha512 -b passwd MQTT_USER MQTT_PASS
```
Remember the MQTT_USER, MQTT_PASS from earlier? These should match the values in the cmd. These details will also be used in localhost:1880 when creating the MQTT input node in Node-RED. Something not working, look below
### ⚠️ Firewall Configuration and path

1. **Configure Firewall**: Ensure your firewall allows traffic on the default MQTT port 1883. Failure to do so can prevent clients (e.g., Pico) from connecting to the broker.

2. **Verify Password File Path**: Ensure the path C:\Program Files\mosquitto\passwd is correct:
    - Right-click on mosquitto.exe and select "Properties".
    - Check the "Location" to confirm the path.
    - If the path is different, adjust it accordingly.

3. **Add Mosquitto to System Path**:
    - Open sysdm.cpl.
    - Click on the "Advanced" tab.
    - Click on "Environment Variables".
    - In the "System variables" section, find the Path variable and click "Edit".
    - Click "New" and add the path to Mosquitto.



### 2. Install Node-RED

Next, install Node-RED by running the following command in the Command Prompt:

```
npm install -g --unsafe-perm node-red
```

### 3. Download and Execute the Bash Script

After this, you can  download the bash script [here](https://github.com/transccc/iot-project/blob/main/mosquitto_bash_script.bat)(You should also have it in the "iot-project-main" folder if you downloaded the repository). This script allows you to start up Mosquitto and Node-RED easily. 
- **Run the script**
- ⚠️ If on windows 10 this may not work, start them both manually
### 4. Set Up Node-RED

Configure Node-RED to work with your MQTT setup:

- **Open Node-RED**: In your web browser, go to localhost:1880.
- **Import the Node-RED Flow**: Download the Node-RED flow from [here](https://github.com/transccc/iot-project/blob/main/node-red_flow) or copy from the repository.
  - In Node-RED, use the import function to import the flow file.
- **Configure the MQTT Input Node**:
  - Locate the MQTT input node in the imported flow, double-click to edit its properties, and update the username, password, and topic fields to match the values provided in the bash script.
<br><br>
- **The imported flow should look something like this:**
![Alt text](https://github.com/transccc/iot-project/blob/main/pictures/Screenshot%202024-07-04%20072238.png)
### 5. Set Up push notifications via HTTP Request in Node-RED

To enable push notifications, with the help of Pushbullet with a  webhook:

- **Create a Pushbullet Account**:
  - Go to the [Pushbullet website](https://www.pushbullet.com/).
  - Sign up for a new account.
- **Generate a Pushbullet Token**:
  - Once logged in, navigate to your account settings.
  - Generate an access token. This token will be used to authenticate your requests.
- **Configure Node-RED for Pushbullet push notifications**:
  - In Node-RED, add go to the Door open functions 

  - Use the following command:
    ```
    curl -u "YOUR_ACCESS_TOKEN_HERE:" https://api.pushbullet.com/v2/users/me
    ```

    This will provide the necessary information to fill out the push notification [functions](https://github.com/transccc/iot-project/tree/main/Node-RED-Functions) in node-red.
### Setting Up InfluxDB

1. **Download and Install InfluxDB**:
   - Go to the [InfluxData Downloads page](https://www.influxdata.com/downloads/).
   - Select the appropriate version for your operating system and follow the instructions to download and install InfluxDB.

2. **Launch InfluxDB**:
   - Start InfluxDB:
     ```
     influxd
     ```
    - or by simply running the .exe file directly


3. **Access InfluxDB UI**:
   - Open your web browser and go to http://localhost:8086.
   - Follow the on-screen instructions to set up InfluxDB.

4. **Create an Account and Configure InfluxDB**:
   - Create an account by providing the necessary details.
   - Set up your organization and save the organization name.
   - Create a bucket and save the bucket name.
   - Generate an API token and save it for future use.

5. **Configure InfluxDB in Node-RED**:
   - Open Node-RED in your web browser (http://localhost:1880).
   - Open the InfluxDB node and configure it:
     - **Server**: Enter http://localhost:8086.
     - **Token**: Enter the API token you generated.
     - **Organization**: Enter the organization name.
     - **Bucket**: Enter the bucket name.

- For more detailed instructions and if you encounter bugs, use the [InfluxDB Documentation](https://docs.influxdata.com/influxdb/v2.0/get-started/) and the [Node-RED Documentation](https://nodered.org/docs/). There are also plenty of resources and other tutorials on YouTube that may help you expand the project and learn more about Node-RED.


 ### Core functionalites of the code
The "main_loop()" function orchestrates the core operations of the device, including blinking the LED, checking the reed switch status, reading temperature and humidity from the DHT11 sensor, and publishing this data to an MQTT broker.
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
The rest of the code can be found in the [project repository](https://github.com/transccc/iot-project/tree/main/pymakpro) folder. 
## Transmitting the Data / Connectivity
### Data Transmission Details
Wi-Fi is used primaliy used in this projet to connect devices within the network. This is connection is done trough a central hub: The Wi-Fi router. The project also uses Wi-Fi for the HTTP post request, which instead sends the data to the router then to the Pushbullet which then sends the message as a notfication to my phone as a webhook. As seen in the previously mentioned code, the code operates trough
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
Wi-Fi provides a fast and easy connection between devices and is a convenient solution for this project, as it was easy to set up and required no extra parts. The obvious disadvantage of Wi-Fi is its limited range; this project can only effectively work at a fixed location close to a router. Wi-Fi also consumes a significant amount of battery power compared to solutions like LoRa. However, both of these are not issues for the current setup, as it involves a door, which is most likely near a router and someone who can replace and charge the power bank. However, for different projects using only a DHT11 sensor, this is a clear disadvantage.
<br>
<br>
As previously seen in the code section, MQTT is used to transmit data to a broker, specifically a local broker using Mosquitto. This process involves connecting to Wi-Fi and then to the MQTT broker that is locally hosted. The client publishes messages to this broker in the form of packets (handled by the library in simple.py) that contain a JSON payload, which is the information used in Node-RED

The payload includes temperature, humidity, and reed switch status data, which a dictionary is created to and then casted into a JSON string:
```
 payload = {
                "temperature": temperature_dht11,
                "humidity": humidity_dht11,
                "reed_status": reed_status
            }
payload_json = ujson.dumps(payload)
```
This JSON payload is then published in a packet to the MQTT broker as follows:

```
  if boot.client:
                boot.client.publish('main', payload_json)
                print("Published:", payload_json)
            else:
                print("MQTT client is not initialized")
```
In this context, "main" is the topic name included in the packet headers, which the broker uses to categorize and distribute the message to subscribers such as Node-RED.The broker manages topics, and clients subscribe to receive messages. In this project, both Node-RED and the Pico subscribe to the "main" topic, although subscription is not required for publishing. When the Pico publishes a packet with a JSON payload, the local Mosquitto broker ensures that Node-RED receives it. With QoS set to 0, MQTT relies on TCP-level acknowledgments and does not provide additional message delivery guarantees. Node-RED then processes the packets. The data from the Pico is in JSON format, containing readings from the DHT11 sensor (temperature and humidity) and the status of the reed switch. These JSON packets are published every three seconds. In Node-RED, the second node in the flow, a JSON node, parses the JSON string created by "ujson.dumps(payload)" into JavaScript objects. These objects' properties are then used in directly for InfluxDB, as seen [here](https://github.com/transccc/iot-project/blob/main/Node-RED-Functions/Format_for_InfluxDB.js), to be converted into values such as floats for InfluxDB. They are also used in the filter and switch nodes to form the body of an HTTP POST request. MQTT's way of neatly handling real-time data is essential for applications that require quick updates and responses and using a local broker like Mosquitto boosts security and cuts latency as the data stays in the local network. This setup is also higly customisable  Node-RED receives the data from the Pico and processes this information in various ways. For instance, Node-RED can redirect the incoming data to InfluxDB for storage and visualization, allowing for analysis and monitoring of the sensor data over time and in real-time. Node-RED can also send real-time push notifications via HTTP POST requests to Pushbullet, providing a funcional webhook that alerts about whether the door is open. This versatility is the main reason for the usage of node-red, all locally hosted, quick and analysable 



## Presenting the Data
### Configuring a Dashboard in InfluxDB

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
   - Click on "_measurement" and select "sensor_data".
   - In the field window, select the fields "reed_status", "humidity", and "temperature".

6. **Visualize Data**:
   - Adjust the settings as necessary to optimize the visualization.
   - You should now see a graph displaying temperature data over time.
![Alt text](https://github.com/transccc/iot-project/blob/main/pictures/Sk%C3%A4rmbild%202024-06-30%20033916.png)
### InfluxDB
I chose InfluxDB because of its strength in time series. It can easily save data over a period for later visual analysis. This is done by observing how the graphs change, especially regarding whether the door was open and the room's climate. The UI can also be designed without necessarily knowing how to write Flux. On the other hand, the data-saving abilities sometimes made it difficult to make changes, as new data types would conflict with previous readings. This largely made me choose to do the HTTP post request in Node-RED instead of webhook in InfluxDB, as I had to create new buckets which took excessive time, due to my inability to properly delete them via the terminal. For the push notification automation process, I went straight to Node-RED to set up the HTTP post to Pushbullet. This is  not dependent on InfluxDB, and the project would work just fine without it. Still, I wanted to have an active component in my project.
- Data is saved indefinitely as soon as the data arrives i.e 3 seconds

## Finalizing the design
Overall, I was satisfied with the project. I did not foresee it going this far, including building out extra features like alerts or even setting up Mosquitto properly. It has been valuable for me, as I've tried building similar locally hosted servers but never managed to finalize the design I was aiming for. For future projects, it would be preferable to use Grafana for a better UI and alert system, which was primarily solved with ad hoc solutions this time due to the project unfolding rather than being planned from the beginning. If it weren't for the lack of a LoRa module, I would have likely implemented that instead, using a Helium network or something similar, which would have been more enjoyable for me, as I enjoy decentralized networks. 

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>
<body>
    <table align="center">
        <tr>
            <td colspan="2" style="text-align: center;">
                <img src="https://github.com/transccc/iot-project/blob/main/pictures/%20PXL_20240629_053358524.jpg" alt="Alt text 1" height="500"/>
                <div class="caption">Setup with part of a plastic bottle as a container for the breadboard and a reed switch on the door next to a neodymium magnet. The power bank is taped onto the plastic bottle and connected with the Pico through a hole in the back of the bottle.</div>
            </td>
        </tr>
        <tr>
            <td>
                <img src="https://github.com/transccc/iot-project/blob/main/pictures/PXL_20240629_232829722.jpg" alt="Alt text 2" width="500" height="500"/>
                <div class="caption">Wiring of the breadboard that is inside the bottle</div>
            </td>
            <td>
                <img src="https://github.com/transccc/iot-project/blob/main/pictures/Pushbulletscreen.png" alt="Alt text 3" height="500"/>
                <div class="caption">Pushbullet push notifications when opening/closing the door</div>
            </td>
        </tr>
    </table>
</body>
</html>
