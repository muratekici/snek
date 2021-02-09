
# **snek**

<img src="/files/game2.png" alt="snek" width="400"/>

## Group Members:
* Ali Furkan Budak
* Murat Ekici

## Description:

A multiplayer snake game which you can play with your friends.

Snek is a game of survival and the last player standing wins the game. Snakes can grow by eating food and can die by crashing into walls, crashing into the body of another snake or head bumping to a bigger snake. 

## Quickstart

* Install the requirements 

```bash
pip3 install -r requirements.txt
```

* Run the application

```bash
python3 main.py [name, "server"]
```

The name argument given to the application saves your snake name. If you give server as the name, your program will serve as a server for other players to join and play the game. After you run the application, a list will appear on the terminal which asks for your ip address. You can choose the ip adress you will use from there. Then it will ask you the ip address of the server. Wait for server to start to game after you join. Have fun!

OS: ```macOS Catalina 10.14.6```, ```Ubuntu 18.04```

Python Version: ```3.9.0```

## **Network Challenges**
Network challenges, the presentation and screenshots from the game are in the "files" folder.


## Packets:

Client/Player uses TCP packets to communicate with the server. There are 3 types of packets: 

* "JOIN_REQUEST" is for connecting to the server

* "LEAVE_REQUEST" is when leaving the game

* "MOVE_REQUEST" is for sending the movement information to the server


Server broadcasts UDP packets to communicate with the players. There are 5 types of packets: 

* "SNAKES" is for sending the snake's initial location before starting the game

* "START_GAME" is for starting the game

* "FOOD_SPAWN" is for sending the location of the food to be spawned

* "MOVEMENTS" is for sending the movement information of all the snakes at each time step

* "SNAKES" is for sending the snake's initial location before starting the gamesent with UDP broadcast when someone opens his/her chat application. 

* "SNAKE_LEFT" is for sending confirming the left request and making sure every client deletes the corresponding snake. This is also used when a user lag's too much.


#### Note: UDP packets are sent 2 times for safety.
