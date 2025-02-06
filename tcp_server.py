import socket
import threading

class SocketServer:
    def __init__(self, host, port, log_callback, encoding='utf-8'):
        self.host = host
        self.port = port
        self.log_callback = log_callback
        self.encoding = encoding
        self.server_socket = None
        self.accepting_clients = False
        self.client_sockets = {}  # 改为字典，键为客户端地址，值为客户端套接字

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.log_callback(f"Server listening on {self.host}:{self.port} (Encoding: {self.encoding})")
            self.accepting_clients = True
            # 启动线程来处理客户端连接
            threading.Thread(target=self.accept_clients).start()
        except Exception as e:
            self.log_callback(f"Server error: {e}")

    def accept_clients(self):
        while self.accepting_clients:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.client_sockets[client_address] = client_socket
                self.log_callback(f"Accepted connection from [{client_address[0]}:{client_address[1]}]")
                # 为每个客户端连接创建一个新线程
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except OSError:
                break

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                try:
                    message = data.decode(self.encoding)
                    self.log_callback(f"Received from [{client_address[0]}:{client_address[1]}]: {message}")
                except UnicodeDecodeError:
                    self.log_callback(f"Error decoding data from [{client_address}]: UnicodeDecodeError (Encoding: {self.encoding})")
        except Exception as e:
            self.log_callback(f"Error handling client [{client_address}]: {e}")
        finally:
            if client_address in self.client_sockets:
                del self.client_sockets[client_address]
            client_socket.close()
            self.log_callback(f"Connection with [{client_address}] closed")

    def stop(self):
        self.accepting_clients = False
        # 关闭所有已连接的客户端套接字
        for client_socket in self.client_sockets.values():
            try:
                client_socket.close()
            except Exception as e:
                self.log_callback(f"Error closing client socket: {e}")
        self.client_sockets = {}

        if self.server_socket:
            try:
                self.server_socket.close()
                self.log_callback("Server stopped.")
            except Exception as e:
                self.log_callback(f"Error stopping server: {e}")

    def send_message_to_clients(self, message):
        for client_address, client_socket in self.client_sockets.items():
            try:
                encoded_message = message.encode(self.encoding)
                client_socket.sendall(encoded_message)
                self.log_callback(f"Sent to [{client_address[0]}:{client_address[1]}]: {message} ")
            except UnicodeEncodeError:
                self.log_callback(f"Error encoding message with {self.encoding} for {client_address}: UnicodeEncodeError")
            except Exception as e:
                self.log_callback(f"Error sending message to {client_address}: {e}")

    def has_clients_connected(self):
        return len(self.client_sockets) > 0

    def change_encoding(self, new_encoding):
        self.encoding = new_encoding
        self.log_callback(f"Server encoding changed to {new_encoding}")