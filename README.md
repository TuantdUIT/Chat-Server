# Chat Server Project

## Overview

This project implements a multi-client chat application using the **TCP/IP protocol**. The server facilitates communication between multiple clients, broadcasting messages and managing client connections, while each client provides a graphical user interface (GUI) built with Tkinter for sending and receiving messages in real-time.

## Why TCP/IP Protocol?

The TCP/IP protocol was selected for this project due to its reliability and robustness, making it ideal for a chat application:

- **Connection-oriented**: Establishes a stable connection between the server and clients before data exchange.
- **Reliable data transmission**: Ensures data packets are delivered accurately without loss or corruption.
- **Error detection and correction**: Automatically detects errors and retransmits missing or corrupted packets.
- **Ordered delivery**: Guarantees messages arrive in the same order they were sent.

## Project Structure

The project consists of two Python scripts:

- **`server3.py`**: Implements the chat server, which listens for client connections, manages nicknames, and broadcasts messages.
- **`client3.py`**: Implements the chat client with a Tkinter-based GUI, allowing users to connect to the server, set a nickname, and exchange messages.

### Server (`server3.py`)

The server is responsible for:

- Listening for client connections on a specified host (`127.0.0.1`) and port (`55555`).
  - You need to open the Command Prompt and run the (`netstat`) command. This will display a list of local addresses along with the ports currently in use by the system. Make sure to choose a port that is not already in use.
- Requesting and storing unique nicknames for each client.
- Broadcasting messages from one client to all connected clients.
- Handling client disconnections and notifying others when a client leaves.
- Managing multiple clients concurrently using threading.

**Key Features**:

- Utilizes TCP sockets (`socket.AF_INET`, `socket.SOCK_STREAM`) for reliable communication.
- Maintains lists of connected clients and their nicknames.
- Includes error handling for connection issues and invalid nicknames.
- Supports graceful shutdown via `KeyboardInterrupt`.

### Client (`client3.py`)

The client provides a user-friendly interface for interacting with the server. It:

- Establishes a TCP connection to the server.
- Prompts the user to enter a nickname via a Tkinter dialog.
- Displays messages in a scrollable text area, limiting the history to the last 10 messages.
- Allows users to send messages via an entry field or by clicking a "Send" button.
- Runs a separate thread to receive messages from the server in real-time.

**Key Features**:

- Built with Tkinter for a simple, cross-platform GUI.
- Supports real-time message sending and receiving.
- Handles server disconnections by displaying error messages.
- Closes the socket connection cleanly when the GUI window is closed.

## Requirements

- Python 3.x
- Tkinter library (typically included with Python standard installation)

## Installation

1. Clone or download the project repository.
2. Ensure Python 3.x is installed on your system.

## How to Run

1. **Start the Server**:

   - Open a terminal and navigate to the project directory.
   - Run the server script:
     ```bash
     python server3.py
     ```
   - The server will start and listen on `127.0.0.1:55555`.

2. **Start the Clients**:

   - Open additional terminals for each client.
   - Run the client script in each terminal:
     ```bash
     python client3.py
     ```
   - A Tkinter window will prompt for a nickname.
   - Enter a nickname to connect to the server and start chatting.

3. **Chat**:

   - Type messages in the client's entry field and press "Enter" or click "Send".
   - Messages from all clients will appear in the chat area of each connected client.
   - Close the client window to disconnect from the server.

4. **Stop the Server**:
   - Press `Ctrl+C` in the server terminal to shut down the server gracefully.

## Example Usage

- Server starts: `Server started on 127.0.0.1:55555`.
- Client 1 connects with nickname "Tuan": `Tuan has connected to the chat room`.
- Client 2 connects with nickname "Duy": `Duy has connected to the chat room`.
- Tuan sends: `Tuan: Hello, Duy!` (displayed in both clients' chat areas).
- Duy replies: `Duy: Hi, Tuan!` (displayed in both clients' chat areas).
- Duy closes her window: `Duy has left the chat room!`.

## Limitations

- The server operates on localhost (`127.0.0.1`), restricting connections to the same machine. To allow remote clients, change the host to `0.0.0.0` or a specific IP address.
- The client GUI limits chat history to 10 messages to manage memory usage.
- No encryption or authentication is implemented, making the application unsuitable for secure communication.
- Empty or invalid nicknames result in immediate client disconnection.

## Troubleshooting

- **Connection refused**: Ensure the server is running before starting clients.
- **Tkinter not found**: Install Tkinter using your package manager (e.g., `sudo apt-get install python3-tk` on Ubuntu).
- **Invalid nickname**: Enter a non-empty nickname when prompted by the client.
