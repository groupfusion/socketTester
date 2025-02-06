import socket
import threading

class UDPClient:
    def __init__(self, host, port, log_callback, encoding='gbk'):
        self.host = host
        self.port = port
        self.log_callback = log_callback
        self.encoding = encoding
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving = False
    def send_message(self, message, client_address):
        try:
            encoded_message = message.encode(self.encoding)
            self.client_socket.sendto(encoded_message, client_address)
            self.log_callback(f"Sent to {client_address}: {message} ")
        except UnicodeEncodeError:
            self.log_callback(f"Error encoding message with {self.encoding} for {client_address}: UnicodeEncodeError")
        except Exception as e:
            self.log_callback(f"Error sending message to {client_address}: {e}")