import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []

def handle_client(client_socket, addr):
    print "Client connected:", addr
    while True:
        try: 
            msg = client_socket.recv(1024)
            if not msg:
                break
            print addr, ":", msg
            for client in clients:
                if client != client_socket:
                    client.send(msg)
        except:
            break
    
    print "Client disconnected:", addr
    clients.remove(client_socket)
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print "Server started on port", PORT

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
