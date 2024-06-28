# Door Temperature Monitor



## Short Project Overview
This project involves setting up an MQTT broker and Node-Red to monitor IoT devices, specifically focusing on integrating various sensors and ensuring reliable data transmission.

**Approximate Time to Complete:**
- Total: 51 hours
  - Setup: 1 hours
  - Research: 5 hours
  - Mosquitto Setup: 20 hours
  - Node-Red Setup: 15 hours
  - InfluxDB Setup: 10 hours 

## Objective
### Why I Chose the Project
I primarily chose to build this project because I enjoy local hosting and wanted to learn more extensively about networks.

### Purpose
The device serves to monitor temperature in relation to a door opening and allows for historical data analysis.

### Insights Expected
This project aims to provide insights into the reliability of different sensors, the efficiency of MQTT for data transmission, and the practical challenges of integrating multiple sensors in an IoT setup.

## Material

## Material

| **Material**                                | **Specification**                                                                                 | **Source**                                                                                       |
|---------------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Raspberry Pi Pico WH                        | Microcontroller                                             | Elektrokit (109 kr)                                                                              |
| USB-Cable A-male to Micro B 5p Male 1.8m    | Cable for connecting Raspberry Pi Pico to computer                                             | Elektrokit (included in the Start Kit - Applied IoT at Linnaeus University, 2024)                |
| Lab-Cable 30cm Female/Male                  | Jumper wires for breadboard connections                                                          | Elektrokit (included in the Start Kit - Applied IoT at Linnaeus University, 2024)                |
| Digital Temperature and Humidity Sensor DHT11 | Measures temperature and humidity                                                                | Elektrokit (49 kr)                                                                               |
| Reed Switch Module Mini                     | Magnetic switch for detecting door open/close state                                              | Elektrokit (25 kr)                                                                               |
| Breadboard                                  | Board for connecting electronic components                                           | Elektrokit (49 kr)                                                                               |


### Images


## Computer Setup
### Chosen IDE
- **IDE:** VSCode with MicroPython

## Computer Setup
### Chosen IDE
- **IDE:** VSCode with MicroPython

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
     - Selecting development mode in Pymakr will now automatically upload the files to the device.
   - Install Node-Red, Mosquitto, and InfluxDB.
## Putting Everything Together
### Circuit Diagram
![Alt text](https://github.com/transccc/iot-project/blob/main/Screenshot%202024-06-26%20233441.png)



## Platform
### Choice of Platform
I used Node-Red and InfluxDB as the primary platforms for this project. Node-Red offers robust real-time data analysis and integration capabilities, along with active notifications. It provides a locally hosted platform with numerous solutions, enabling the creation of a comprehensive dashboard with the help of InfluxDB. The data is transmitted using a local MQTT broker (Mosquitto) for seamless integration with Node-Red.

- **Local Setup:** Chosen for enhanced control and privacy, avoiding dependency on external cloud services.
- **Free Services:** Utilized to keep costs low.
- **Functionality:** Real-time data transmission, monitoring, customizable dashboards, and notifications via Pushbullet

## Transmitting the Data / Connectivity
### Data Transmission Details
- **Data Frequency:** Sent every 3 seconds.
- **Wireless Protocols:** WiFi for local transmission.
- **Transport Protocols:** MQTT for efficient, low-overhead communication, HTTP to Pushbullet for realtime notfications. 

### Design Choices
- **Data Transmission:** Chose MQTT for its lightweight protocol, suitable for IoT. Additionally, HTTP is used to send notifications to Pushbullet, ensuring timely alerts.
- **Wireless Protocols:** WiFi provides sufficient range and speed for this application, considering the local environment.

## Presenting the Data
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

