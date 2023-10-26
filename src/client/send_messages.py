import string
import random
import tcp_client
import time

def generate_message():
    message = ""
    for i in range(10):
        message += random.choice(string.ascii_letters)
    return message

def send_message():
    message = generate_message()
    tcp_client.send_message_from_client(message)

while True:
    try:
        send_message()
        time.sleep(3)
    except KeyboardInterrupt:
        print("Message exchange interrupted")
        # tcp_client.close_connection()
        break
        

    