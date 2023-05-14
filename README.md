# smart-bowl-IoT
IOT course, HIT // Final Project // Semester B, 2023

The YouTube video link for the presentation recording is [here](#)
Served By: 

> Sergey Juchenko 319365102  |  Vladimir Poplavski 336137468  | Viktor Rokitko 336484951


## Description
This project consists of three scripts that communicate with a smart bowl through an MQTT broker. The smart bowl measures the weight of the food and sends the data to a subscriber script that updates a GUI displaying the weight of the bowl. The publisher script allows the user to add food to the bowl by clicking a button on the GUI. When the button is pressed, a message is published to the broker, which is then received by the subscriber script. The scripts also log the timestamp and weight of the food added to a SQLite database.

## Dependencies
The project requires the following dependencies:

paho-mqtt==1.5.1
pillow==8.1.2
tkinter
SQL lite

## Usage
To run script:
run smart-bowl.py
run RELAY.py   --> click on Connect 
run application.py

## License
This project is licensed under the MIT License.



