# Door Temperature Monitor



## Short Project Overview
This project involves setting up an MQTT broker and Node-Red to monitor IoT devices, specifically focusing on integrating various sensors and ensuring reliable data transmission.

**Approximate Time to Complete:**
- Total: 140 hours
  - Setup: 20 hours
  - Research: 40 hours
  - Mosquitto Setup: 60 hours
  - Node-Red Configuration: 20 hours

## Objective
### Why I Chose the Project
I primarily chose to build this project because I enjoy local hosting and wanted to learn more extensively about networks.

### Purpose
The device serves to monitor temperature in relation to a door opening and allows for historical data analysis.

### Insights Expected
This project aims to provide insights into the reliability of different sensors, the efficiency of MQTT for data transmission, and the practical challenges of integrating multiple sensors in an IoT setup.

## Material
### List of Material
1. **Raspberry Pi Pico WH**
   - Source: Elektrokit (included in the Start Kit - Applied IoT at Linnaeus University, 2024)
2. **USB-Cable A-male to Micro B 5p Male 1.8m**
   - Source: Elektrokit (included in the Start Kit - Applied IoT at Linnaeus University, 2024)
3. **Lab-Cable 30cm Female/Male**
   - Source: Elektrokit (included in the Start Kit - Applied IoT at Linnaeus University, 2024)
4. **Digital Temperature and Humidity Sensor DHT11**
   - Source: Elektrokit (included in the Start Kit - Applied IoT at Linnaeus University, 2024)
5. **Reed Switch Module Mini**
   - Source: Elektrokit (included in the Sensor Kit - 25 modules)

### Images


## Computer Setup
### Chosen IDE
- **IDE:** VSCode with MicroPython

### Steps for Computer Setup
1. **Flashing Firmware:**
   - Hold BOOTSEL, plugg in the device with the USB and then flashh via the UF2 bootloader, by draging the file into the driver.
2. **Plugin Installation:**
   - Install Node.js, Micropython, Node-red and Mosquitto

## Putting Everything Together
### Circuit Diagram


### Electrical Calculations


## Platform
### Choice of Platform
- **Local Installation:**
  - Using a local MQTT broker (Mosquitto) for data handling.
- **Comparison:**
  - Local installation vs. cloud-based solutions.
  - Chose local for greater control and lower latency.

## Implementation Details
Initially, I used the MQTT broker and set it up to start first in a batch file. This allows the localhost to easily open both Node-Red and the broker, and it also creates a topic.

This setup, however, did not solve the issue regarding the client startup with the sensors, which I decided to handle manually. I configured Node-Red to create a graph, aiming for consistency despite the unstable internet connection for my Pico. I also added a collision sensor to measure temperature and detect if the door closes.

The collision sensor was used because I lacked a strong enough magnet for a magnetic sensor. I realized that the collision sensor only sent one signal and would need separate threading to detect movement, leading to program inconsistencies. Due to my inexperience with multithreading, this likely corrupted the files, making the program unable to run.

After a hard reset, I switched to using a magnet, which worked. I had initially assumed the magnet was too weak due to a minor mistake. Removing the collision sensor also reduced power consumption and potential failure points.

I figured out that MQTT connection inconsistency might be due to ID conflicts when the program is already running with a connected ID. The broker maintains the session if the device is already connected. A duplicate connection attempt with the same client ID may be refused. Reconnecting after unplugging and replugging the device resolves the conflict.

Additionally, I realized I forgot to use `sys.exit()`, which helped terminate running instances, allowing the program to run as intended and consistently connect to the MQTT broker. Using the magnet avoided multithreading issues, though it didn't entirely resolve the MQTT problems, it was still an improvement.

### Example Output
Using JSON packages and debug nodes, I was able to print the following results:
*(Include example output here)*

### Different Platforms Discussed

