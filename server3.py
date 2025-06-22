import threading
import socket

class ChatServer:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []
        self.running = True

    def start(self):
        """Start the server and begin listening for connections."""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            print(f"Server started on {self.host}:{self.port}")
            self.receive_connections()
        except Exception as e:
            print(f"Server error: {e}")
            self.shutdown()

    def broadcast(self, message):
        """Send a message to all connected clients."""
        message_str = message.decode('utf-8') if isinstance(message, bytes) else message
        for client in self.clients:
            try:
                client.send(message_str.encode('utf-8'))
            except:
                self.remove_client(client)

    def handle_client(self, client):
        """Handle messages from a specific client."""
        while self.running:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                self.remove_client(client)
                break

    def remove_client(self, client):
        """Remove a client from the server."""
        if client in self.clients:
            index = self.clients.index(client)
            nickname = self.nicknames[index]
            self.clients.remove(client)
            self.nicknames.remove(nickname)
            try:
                client.close()
            except:
                pass
            self.broadcast(f'{nickname} has left the chat room!')

    def receive_connections(self):
        """Accept incoming client connections."""
        while self.running:
            try:
                print('Server is running and listening ...')
                client, address = self.server.accept()
                print(f'Connection established with {address}')
                client.send('nickname?'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                if not nickname or nickname.strip() == "":
                    client.send('Invalid nickname! Disconnecting...'.encode('utf-8'))
                    client.close()
                    continue
                self.nicknames.append(nickname)
                self.clients.append(client)
                print(f'The nickname of this client is {nickname}')
                self.broadcast(f'{nickname} has connected to the chat room')
                client.send('you are now connected!'.encode('utf-8'))
                thread = threading.Thread(target=self.handle_client, args=(client,), daemon=True)
                thread.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break

    def shutdown(self):
        """Shut down the server and close all connections."""
        self.running = False
        for client in self.clients[:]:
            self.remove_client(client)
        try:
            self.server.close()
        except:
            pass
        print("Server shut down.")

def main():
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()