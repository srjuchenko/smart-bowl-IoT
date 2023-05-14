import paho.mqtt.client as mqtt
import sqlite3
import time
import tkinter as tk
import threading

CLIENT_ID = "smart-bowl-app-1"
BROKER = "broker.hivemq.com"
PUB_TOPIC = "smart-bowl/add-food"
SUB_TOPIC = "smart-bowl/weight-status"
BACKGROUNG_IMG_PATH = "bowl.png"
GRAMS_TO_ADD = 100

# init DB
conn = sqlite3.connect('smart_bowl.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS food_log
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp TEXT NOT NULL,
              weight INTEGER NOT NULL)''')
c.execute("SELECT * FROM food_log")
print("data in DB:")
print(c.fetchall())

# callback function to update the weight label
def update_label():
    global amount_of_food_grams, amount_label, add_food_button
    if amount_of_food_grams <= 0:
        amount_label.config(text="Empty Bowl", fg="red", font=("Arial", 24, "bold"))
        add_food_button.pack()
    else:
        amount_label.config(text=str(amount_of_food_grams) + " grams", fg="green", font=("Arial", 32, "bold"))
        add_food_button.pack_forget()

# callback function to add food to the bowl
def add_food():
    client.publish(PUB_TOPIC, "ADD")
    add_food_button.pack_forget()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # get the current timestamp
    
    c.execute("INSERT INTO food_log (timestamp, weight) VALUES (?, ?)", (timestamp, GRAMS_TO_ADD))
    conn.commit()  # commit the changes to the database
    update_label()

# callback function to process incoming MQTT messages
def on_message(client, userdata, message):
    global amount_of_food_grams
    if message.topic == "smart-bowl/weight-status":
        amount_of_food_grams = int(str(message.payload.decode("utf-8")))
        print("Received message: " + str(amount_of_food_grams) + " grams")
        update_label()

# creates client
client = mqtt.Client(CLIENT_ID)
client.connect(BROKER)
client.subscribe(SUB_TOPIC)
client.on_message = on_message
client.loop_start()

# creates GUI
root = tk.Tk()
root.geometry("400x400")
root.iconbitmap("favicon.ico")
root.title("Application")

background_image = tk.PhotoImage(file=BACKGROUNG_IMG_PATH)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

amount_of_food_grams = 0
amount_label = tk.Label(root, text="0 grams", fg="green", font=("Arial", 32, "bold"))
amount_label.pack(pady=20)

add_food_button = tk.Button(root, text="Add Food", bg="blue", fg="black", font=("Arial", 16), command=add_food)
add_food_button.pack(pady=20)
update_label()

root.mainloop()

