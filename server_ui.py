from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QComboBox, QGroupBox
from tcp_server import SocketServer

class ServerUI(QWidget):

    def __init__(self):
        super().__init__()
        self.server = None
        self.encoding = 'utf-8'
        self.initUI()

    def initUI(self):
        server_layout = QVBoxLayout()

        # 网络设置组
        network_settings_group = QGroupBox("Network Settings")
        network_settings_layout = QVBoxLayout()

        # 主机和端口输入布局
        host_port_layout = QHBoxLayout()
        host_label = QLabel('Host:')
        self.server_host_input = QLineEdit()
        self.server_host_input.setText('127.0.0.1')
        host_port_layout.addWidget(host_label)
        host_port_layout.addWidget(self.server_host_input)

        port_label = QLabel('Port:')
        self.server_port_input = QLineEdit()
        self.server_port_input.setText('12345')
        host_port_layout.addWidget(port_label)
        host_port_layout.addWidget(self.server_port_input)
        network_settings_layout.addLayout(host_port_layout)

        # 编码选择框
        encoding_layout = QHBoxLayout()
        encoding_label = QLabel('Encoding:')
        self.server_encoding_combobox = QComboBox()
        encodings = ['utf-8', 'gbk']
        self.server_encoding_combobox.addItems(encodings)
        self.server_encoding_combobox.setCurrentText('utf-8')
        self.server_encoding_combobox.currentTextChanged.connect(self.update_server_encoding)
        encoding_layout.addWidget(encoding_label)
        encoding_layout.addWidget(self.server_encoding_combobox)
        network_settings_layout.addLayout(encoding_layout)

        # 启动和停止按钮
        button_layout = QHBoxLayout()
        self.server_start_button = QPushButton('Start Server')
        self.server_start_button.clicked.connect(self.start_server)
        button_layout.addWidget(self.server_start_button)

        self.server_stop_button = QPushButton('Stop Server')
        self.server_stop_button.clicked.connect(self.stop_server)
        self.server_stop_button.setEnabled(False)
        button_layout.addWidget(self.server_stop_button)
        network_settings_layout.addLayout(button_layout)

        network_settings_group.setLayout(network_settings_layout)
        server_layout.addWidget(network_settings_group)

        # 消息组
        messages_group = QGroupBox("Messages")
        messages_layout = QVBoxLayout()

        # 消息输入和发送布局，添加 message 输入框前的 label
        send_layout = QHBoxLayout()
        message_label = QLabel('Message:')
        send_layout.addWidget(message_label)
        self.server_message_input = QLineEdit()
        send_layout.addWidget(self.server_message_input)
        self.server_send_button = QPushButton('Send Message')
        self.server_send_button.clicked.connect(self.server_send_message)
        self.server_send_button.setEnabled(False)
        send_layout.addWidget(self.server_send_button)
        messages_layout.addLayout(send_layout)

        # 日志显示区域
        self.server_log_text = QTextEdit()
        self.server_log_text.setReadOnly(True)
        messages_layout.addWidget(self.server_log_text)

        messages_group.setLayout(messages_layout)
        server_layout.addWidget(messages_group)

        self.setLayout(server_layout)

    def start_server(self):
        host = self.server_host_input.text()
        try:
            PORT_RANGE = range(0, 65535)
            port = int(self.server_port_input.text())
            if port not in PORT_RANGE:
                self.server_log_text.append('Ensure that the port number is between 0 and 65535.')
        except ValueError:
            self.server_log_text.append('Invalid port number. Please enter a valid integer.')
            return

        self.server = SocketServer(host, port, self.server_log_callback, self.encoding)
        self.server.start()
        self.server_start_button.setEnabled(False)
        self.server_stop_button.setEnabled(True)
        self.server_send_button.setEnabled(True)

    def stop_server(self):
        if self.server:
            self.server.stop()
            self.server_start_button.setEnabled(True)
            self.server_stop_button.setEnabled(False)
            self.server_send_button.setEnabled(False)

    def server_send_message(self):
        message = self.server_message_input.text()
        if message:
            if self.server:
                self.server.send_message_to_clients(message)
            self.server_message_input.clear()

    def server_log_callback(self, message):
        self.server_log_text.append(message)
        if self.server:
            self.server_send_button.setEnabled(self.server.has_clients_connected())

    def update_server_encoding(self, new_encoding):
        self.encoding = new_encoding
        self.server_log_text.append(f"Server encoding set to {new_encoding}")
        if self.server:
            self.server.change_encoding(new_encoding)