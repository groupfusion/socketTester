
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QComboBox, QGroupBox
from tcp_client import SocketClient

class ClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.client = None
        self.encoding = 'utf-8'
        self.initUI()

    def initUI(self):
        client_layout = QVBoxLayout()

        # 网络设置组
        network_settings_group = QGroupBox("Network Settings")
        network_settings_layout = QVBoxLayout()

        # 主机和端口输入布局
        host_port_layout = QHBoxLayout()
        host_label = QLabel('Host:')
        self.client_host_input = QLineEdit()
        self.client_host_input.setText('127.0.0.1')
        host_port_layout.addWidget(host_label)
        host_port_layout.addWidget(self.client_host_input)

        port_label = QLabel('Port:')
        self.client_port_input = QLineEdit()
        self.client_port_input.setText('12345')
        host_port_layout.addWidget(port_label)
        host_port_layout.addWidget(self.client_port_input)
        network_settings_layout.addLayout(host_port_layout)

        # 编码选择框
        encoding_layout = QHBoxLayout()
        encoding_label = QLabel('Encoding:')
        self.client_encoding_combobox = QComboBox()
        encodings = ['utf-8', 'gbk']
        self.client_encoding_combobox.addItems(encodings)
        self.client_encoding_combobox.setCurrentText('utf-8')
        self.client_encoding_combobox.currentTextChanged.connect(self.update_client_encoding)
        encoding_layout.addWidget(encoding_label)
        encoding_layout.addWidget(self.client_encoding_combobox)
        network_settings_layout.addLayout(encoding_layout)

        # 连接和断开按钮
        button_layout = QHBoxLayout()
        self.client_connect_button = QPushButton('Connect to Server')
        self.client_connect_button.clicked.connect(self.connect_client)
        button_layout.addWidget(self.client_connect_button)

        self.client_disconnect_button = QPushButton('Disconnect from Server')
        self.client_disconnect_button.clicked.connect(self.disconnect_client)
        self.client_disconnect_button.setEnabled(False)
        button_layout.addWidget(self.client_disconnect_button)
        network_settings_layout.addLayout(button_layout)

        network_settings_group.setLayout(network_settings_layout)
        client_layout.addWidget(network_settings_group)

        # 消息组
        messages_group = QGroupBox("Messages")
        messages_layout = QVBoxLayout()

        # 消息输入和发送布局，添加 message 输入框前的 label
        send_layout = QHBoxLayout()
        message_label = QLabel('Message:')
        send_layout.addWidget(message_label)
        self.client_message_input = QLineEdit()
        send_layout.addWidget(self.client_message_input)
        self.client_send_button = QPushButton('Send Message')
        self.client_send_button.clicked.connect(self.client_send_message)
        self.client_send_button.setEnabled(False)
        send_layout.addWidget(self.client_send_button)
        messages_layout.addLayout(send_layout)

        # 日志显示区域
        self.client_log_text = QTextEdit()
        self.client_log_text.setReadOnly(True)
        messages_layout.addWidget(self.client_log_text)

        messages_group.setLayout(messages_layout)
        client_layout.addWidget(messages_group)

        self.setLayout(client_layout)

    def connect_client(self):
        host = self.client_host_input.text()
        try:
            port = int(self.client_port_input.text())
        except ValueError:
            self.client_log_text.append('Invalid port number. Please enter a valid integer.')
            return

        self.client = SocketClient(host, port, self.client_log_callback, self.encoding)
        self.client.connect()
        self.client_connect_button.setEnabled(False)
        self.client_disconnect_button.setEnabled(True)
        self.client_send_button.setEnabled(True)

    def disconnect_client(self):
        if self.client:
            self.client.disconnect()
            self.client_connect_button.setEnabled(True)
            self.client_disconnect_button.setEnabled(False)
            self.client_send_button.setEnabled(False)

    def client_send_message(self):
        message = self.client_message_input.text()
        if message:
            if self.client:
                self.client.send_message(message)
            self.client_message_input.clear()

    def client_log_callback(self, message):
        self.client_log_text.append(message)

    def update_client_encoding(self, new_encoding):
        self.encoding = new_encoding
        self.client_log_text.append(f"Client encoding set to {new_encoding}")
        if self.client:
            self.client.change_encoding(new_encoding)