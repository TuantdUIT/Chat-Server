import threading
import socket
import tkinter as tk
from tkinter import simpledialog, scrolledtext, END

class ChatClient:
    def __init__(self, host='127.0.0.1', port=55555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None
        self.running = True

    def connect(self):
        """Establish connection to the server."""
        try:
            self.client.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def set_nickname(self, nickname):
        """Set the client's nickname."""
        self.nickname = nickname if nickname else "Guest"

    def receive_messages(self, chat_area):
        """Receive and process messages from the server."""
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == "nickname?":
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    self.display_message(chat_area, message)
            except:
                self.display_message(chat_area, "Connection closed!")
                self.close()
                break

    def send_message(self, message, chat_area):
        """Send a message to the server."""
        if not message.strip():
            return
        full_message = f'{self.nickname}: {message}'
        try:
            self.client.send(full_message.encode('utf-8'))
        except:
            self.display_message(chat_area, "Failed to send message!")

    def display_message(self, chat_area, message):
        """Display a message in the chat area."""
        if chat_area:
            chat_area.config(state='normal')
            chat_area.insert(END, message + '\n')
            # Limit to 10 messages
            line_count = int(chat_area.index('end-1c').split('.')[0])
            if line_count > 10:
                chat_area.delete('1.0', f'{line_count - 10}.0')
            chat_area.config(state='disabled')
            chat_area.see(END)

    def close(self):
        """Close the client connection."""
        self.running = False
        try:
            self.client.close()
        except:
            pass

class ChatGUI:
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
        self.setup_gui()

    def setup_gui(self):
        """Set up the Tkinter GUI."""
        self.nickname = self.get_nickname()
        self.client.set_nickname(self.nickname)
        self.root.title(f"Chat Client - {self.nickname}")
        self.root.geometry("600x400")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.chat_area = scrolledtext.ScrolledText(
            self.root, state='disabled', wrap=tk.WORD, height=15
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        entry_frame = tk.Frame(self.root)
        entry_frame.pack(padx=10, pady=5, fill=tk.X)

        self.message_entry = tk.Entry(entry_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.message_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(entry_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

    def get_nickname(self):
        """Prompt for nickname using a dialog."""
        self.root.withdraw()
        nickname = simpledialog.askstring("Nickname", "Choose a nickname:", parent=self.root)
        self.root.deiconify()
        return nickname

    def send_message(self, event=None):
        """Handle sending a message."""
        message = self.message_entry.get()
        self.client.send_message(message, self.chat_area)
        self.message_entry.delete(0, END)

    def on_closing(self):
        """Handle window closing."""
        self.client.close()
        self.root.quit()

    def start(self):
        """Start the GUI and receive thread."""
        receive_thread = threading.Thread(
            target=self.client.receive_messages, args=(self.chat_area,), daemon=True
        )
        receive_thread.start()
        self.root.mainloop()

def main():
    client = ChatClient()
    if client.connect():
        gui = ChatGUI(client)
        gui.start()
    else:
        print("Failed to connect to server.")

if __name__ == "__main__":
    main()