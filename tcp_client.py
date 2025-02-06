import socket
import threading

class SocketClient:
    def __init__(self, host, port, log_callback, encoding='utf-8'):
        self.host = host
        self.port = port
        self.log_callback = log_callback
        self.encoding = encoding
        self.client_socket = None
        self.receiving = False

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.log_callback(f"Connected to server at {self.host}:{self.port} (Encoding: {self.encoding})")
            self.receiving = True
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            self.log_callback(f"Connection error: {e}")

    def receive_messages(self):
        while self.receiving:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                try:
                    message = data.decode(self.encoding)
                    self.log_callback(f"Received from server: {message}")
                except UnicodeDecodeError:
                    self.log_callback(f"Error decoding data from server: UnicodeDecodeError (Encoding: {self.encoding})")
            except Exception as e:
                self.log_callback(f"Error receiving message: {e}")
                break

    def send_message(self, message):
        try:
            encoded_message = message.encode(self.encoding)
            self.client_socket.sendall(encoded_message)
            self.log_callback(f"Sent to server: {message} ")
        except UnicodeEncodeError:
            self.log_callback(f"Error encoding message with {self.encoding}: UnicodeEncodeError")
        except Exception as e:
            self.log_callback(f"Error sending message: {e}")

    def disconnect(self):
        self.receiving = False
        if self.client_socket:
            try:
                self.client_socket.close()
                self.log_callback("Disconnected from server.")
            except Exception as e:
                self.log_callback(f"Error disconnecting from server: {e}")

    def change_encoding(self, new_encoding):
        self.encoding = new_encoding
        self.log_callback(f"Client encoding changed to {new_encoding}")