import socket
import threading

class UDPServer:
    def __init__(self, host, port, log_callback, encoding='gbk'):
        self.host = host
        self.port = port
        self.log_callback = log_callback
        self.encoding = encoding
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving = False

    def start(self):
        try:
            
            self.server_socket.bind((self.host, self.port))
            self.log_callback(f"UDP Server listening on {self.host}:{self.port} ")
            self.receiving = True
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            self.log_callback(f"UDP Server error: {e}")

    def receive_messages(self):
        while self.receiving:
            try:
                data, client_address = self.server_socket.recvfrom(1024)
                try:
                    message = data.decode(self.encoding)
                    self.log_callback(f"Received from {client_address}: {message}")
                except UnicodeDecodeError:
                    self.log_callback(f"Error decoding data from {client_address}: UnicodeDecodeError (Encoding: {self.encoding})")
            except Exception as e:
                self.log_callback(f"Error receiving message: {e}")
                break

    def stop(self):
        self.receiving = False
        if self.server_socket:
            try:
                self.server_socket.close()
                self.log_callback("UDP Server stopped.")
            except Exception as e:
                self.log_callback(f"Error stopping UDP server: {e}")

    
