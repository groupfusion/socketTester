from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QComboBox, QGroupBox
from udp_server import UDPServer
from udp_client import UDPClient
class UDPServerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.is_listening = False
        self.udp_server = None
        self.udp_client = None
        self.initUI()

    def initUI(self):
        udp_server_layout = QVBoxLayout()

        # 网络设置组
        network_settings_group = QGroupBox("Server")
        network_settings_layout = QVBoxLayout()

        # 主机和端口输入布局
        host_port_layout = QHBoxLayout()
        host_label = QLabel('Host:')
        self.udp_server_host_input = QLineEdit()
        self.udp_server_host_input.setText('127.0.0.1')
        host_port_layout.addWidget(host_label)
        host_port_layout.addWidget(self.udp_server_host_input)

        port_label = QLabel('Port:')
        self.udp_server_port_input = QLineEdit()
        self.udp_server_port_input.setText('12346')
        host_port_layout.addWidget(port_label)
        host_port_layout.addWidget(self.udp_server_port_input)
        network_settings_layout.addLayout(host_port_layout)

        # 合并后的启动/停止按钮
        self.start_stop_button = QPushButton('Start Listening')
        self.start_stop_button.clicked.connect(self.toggle_listening)
        network_settings_layout.addWidget(self.start_stop_button)

        network_settings_group.setLayout(network_settings_layout)
        udp_server_layout.addWidget(network_settings_group)


        # 消息组
        messages_group = QGroupBox("Messages")
        messages_layout = QVBoxLayout()

        # 日志显示区域
        self.udp_server_log_text = QTextEdit()
        self.udp_server_log_text.setReadOnly(True)
        messages_layout.addWidget(self.udp_server_log_text)

        messages_group.setLayout(messages_layout)
        udp_server_layout.addWidget(messages_group)

        # 客户端组
        client_group = QGroupBox("Client")
        client_layout = QVBoxLayout()

        # 客户端 IP 地址输入框
        client_ip_layout = QHBoxLayout()
        client_ip_label = QLabel('IP Address:')
        self.client_ip_input = QLineEdit()
        self.client_ip_input.setText('127.0.0.1')
        client_ip_layout.addWidget(client_ip_label)
        client_ip_layout.addWidget(self.client_ip_input)

        # 客户端端口输入框
        client_port_label = QLabel('Port:')
        self.client_port_input = QLineEdit()
        self.client_port_input.setText('12346')
        client_ip_layout.addWidget(client_port_label)
        client_ip_layout.addWidget(self.client_port_input)
        client_layout.addLayout(client_ip_layout)

        # 客户端消息输入框 发送按钮
        client_message_layout = QHBoxLayout()
        client_message_label = QLabel('Message:')
        self.client_message_input = QLineEdit()
        client_message_layout.addWidget(client_message_label)
        client_message_layout.addWidget(self.client_message_input)
        client_send_button = QPushButton('Send')
        client_send_button.clicked.connect(self.send_to_client)
        client_message_layout.addWidget(client_send_button)
        client_layout.addLayout(client_message_layout)

        client_group.setLayout(client_layout)
        udp_server_layout.addWidget(client_group)

        self.setLayout(udp_server_layout)

    def toggle_listening(self):
        if self.is_listening:
            # 如果正在监听，停止服务器
            self.stop_server()
            self.start_stop_button.setText('Start Listening')
        else:
            # 如果未监听，启动服务器
            self.start_server()
            self.start_stop_button.setText('Stop Listening')
        self.is_listening = not self.is_listening

    def start_server(self):
        host = self.udp_server_host_input.text()
        try:
            port = int(self.udp_server_port_input.text())
        except ValueError:
            self.udp_server_log_text.append('Invalid port number. Please enter a valid integer.')
            return

        self.udp_server = UDPServer(host, port, self.udp_server_log_callback)
        self.udp_server.start()

    def stop_server(self):
        if self.udp_server:
            self.udp_server.stop()

    def udp_server_log_callback(self, message):
        self.udp_server_log_text.append(message)

    def send_to_client(self):
        
        # 获取客户端 IP 地址
        client_ip = self.client_ip_input.text()
        try:
            # 获取客户端端口号，并转换为整数
            client_port = int(self.client_port_input.text())
        except ValueError:
            # 若端口号输入无效，记录日志并返回
            self.udp_server_log_text.append('Invalid client port number. Please enter a valid integer.')
            return
        # 获取要发送的消息
        message = self.client_message_input.text()
        self.udp_client = UDPClient(client_ip, client_port, self.udp_server_log_callback)
        if message and client_ip and client_port:
            # 若消息、IP 地址和端口号都不为空
            client_address = (client_ip, client_port)
            
            if self.udp_client:
                # 若 UDP 服务器已启动，调用服务器的 send_message 方法发送消息
                self.udp_client.send_message(message, client_address)
                # 清空消息输入框
                self.client_message_input.clear()
        else:
            # 若消息、IP 地址或端口号为空，记录日志
            self.udp_server_log_text.append('Please fill in client IP, port and message.')