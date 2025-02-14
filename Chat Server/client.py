import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

def receive_message(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            print "\n" + msg
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

thread = threading.Thread(target=receive_message, args=(client,))
thread.daemon = True
thread.start()

print "Connected to chat. Type messages and press ENTER to send."

while True:
    msg = raw_input()
    if msg.lower() == "exit":
        break
    client.send(msg)

client.close()
