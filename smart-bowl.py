import paho.mqtt.client as mqtt
import time
import tkinter as tk
import threading

BROKER = "broker.hivemq.com"
SUB_TOPIC = "smart-bowl/weight"
PUB_TOPIC = "smart-bowl/weight-status"
FULL_BOWL_IMG_PATH = "img.png"
EMPTY_BOWL_IMG_PATH = "img2.png"



# callback function to process incoming MQTT messages
def on_message(client, userdata, message):
    global amount_of_food_grams
    amount_of_food_grams = int(str(message.payload.decode("utf-8")))
    print("Received message: " + str(amount_of_food_grams) + " grams was added")
    
# updates the weight in the bowl 
def update_label():
    global amount_of_food_grams
    amount_of_food_grams -= 10
    if amount_of_food_grams < 0:
        amount_of_food_grams = 0
        
    amount_label.config(text=str(amount_of_food_grams) + " grams")
    client.publish(PUB_TOPIC, str(amount_of_food_grams))

def update_loop():
    while True:
        update_label()
        time.sleep(1)
        
        # changes the image from empty bowl to full and vice versa
        img = ''
        if amount_of_food_grams <= 0:
            img = tk.PhotoImage(file = EMPTY_BOWL_IMG_PATH)
        else:
            img = tk.PhotoImage(file = FULL_BOWL_IMG_PATH)
        update_img(img)

def update_img(img):
    image_label.configure(image=img)

# creates client 
client = mqtt.Client()
client.connect(BROKER)
client.subscribe(SUB_TOPIC)
client.on_message = on_message
client.loop_start()

amount_of_food_grams = 0

# creates GUI
root = tk.Tk()
root.geometry("400x400")
root.iconbitmap("favicon.ico")
root.title("Smart Bowl")

amount_label = tk.Label(root, text=str(amount_of_food_grams) + " grams", font=("Arial", 32))
amount_label.pack(pady=20)

image = tk.PhotoImage(file=EMPTY_BOWL_IMG_PATH)
image_label = tk.Label(root, image=image, width=300, height=300)
image_label.pack()


update_thread = threading.Thread(target=update_loop)
update_thread.start()

root.mainloop()


