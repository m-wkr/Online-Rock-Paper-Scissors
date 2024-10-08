# Online-Rock-Paper-Scissors

Online Rock Paper Scissors is a simplistic recreation of the game stated, provided by a server script for validating user inputs and handling socket connections to host the game, and a client script for connecting to the centralized server. 

## What changes may I need to configure to connect to the server?

By default, the client files are configured to run on the same machine as the server. However, when you are hosting the server file, depending on whether it is hosted online or not, the IP string value held in the **RPS_c.py** file may need to be altered to establish a connection as required.

This is determined by the conditions below:

| Server Placement | IP type needed |
| ---------------- | -------------- |
| Locally hosted | Local IP Address |
| Remotely hosted | Global IP Address |

### How do I run it?

1. Run the **RPS_s.p** file in the server folder on the server machine
2. Configure any change of IP addresses in the **RPS_c.py** file/s to ensure it matches the server machine's IP
3. Distribute the client folder to any machines you will use to connect to the server
4. Run two instances of the client **RPS_c.py** file between one or more machines
5. Press the menu's connect button to join the round matching screen to play