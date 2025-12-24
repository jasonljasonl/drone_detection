# Drone Detection WebApp

## Description
This application is a real-time drone detection WebApp. It allows you to simulate drones, retrieve their data via **MAVLink**, and display their positions on a dynamic map in real time using **Leaflet**. It also includes a system for detecting drones with virtual radars, storing events in a database, and creating logs.

**Note:** If you are looking at this project right now, you won't see the drone simulation files. I plan to add them soon to make it easier for everyone to run the simulation, sorry! 😃

## Tools Used
- **Backend**: Django, Django Channels, Python
- **Messaging**: Kafka
- **Drone Simulation**: ArduPilot, MAVLink
- **Frontend**: React + Leaflet
- **System**: Linux Ubuntu virtual machine

## How It Works
1. A drone is simulated via ArduPilot on an Ubuntu virtual machine.
2. The drone's data (ID, GPS coordinates) is retrieved via MAVLink.
3. This data is sent to Kafka on two topics:
   - **Topic 1**: drone GPS coordinates.
   - **Topic 2**: distance calculation between the drone and the radars.
4. Django Channels listens to the Kafka topics and forwards the data to the frontend for real-time display on a Leaflet map.

## Radar Modeling
- A function calculates the distance between each radar and the simulated drone.
- If the distance is less than or equal to **(exemple:) 500 m**, the drone is recorded in the database as detected, including:
  - Drone ID
  - GPS coordinates
  - Detection time
  - Detecting radar
- A log is also created for each detection with the same information.

## Frontend
- The frontend uses **React** and **Leaflet** to display:
  - Simulated drones
  - Radars
- Positions are updated in real time, allowing visualization of drone movements and detection zones.

## Global Workflow
1. Start the Ubuntu virtual machine.
2. Simulate the drone via ArduPilot.
3. Retrieve MAVLink data.
4. Send the data to Kafka.
5. Django Channels (websocket) receives the data and forwards it to the frontend for dynamic map display.
6. Calculate radar-drone distances. If a drone is within a radar detection range, store detected drones in the database + create a log file.

## Visual Workflow

```text
Drone simulated (ArduPilot on VM)
        |
        v
Retrieve data via MAVLink (ID, GPS)
        |
        v
       Kafka
  (topic 1: GPS coordinates, topic 2: radar distance)
        |
        v
 Django Channels (websocket)
  (receives messages and forwards to frontend)
        |
        v
Frontend React + Leaflet
  (real-time dynamic map display)
        |
        v
Calculate radar-drone distance
  If ≤ threshold (example: 500 m)::
    - Store in database
    - Create log
    
```
## Goal
Provide a real-time drone monitoring and detection interface, extensible to multi-drone and multi-radar scenarios.


