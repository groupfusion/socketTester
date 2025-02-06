import sys
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from server_ui import ServerUI
from client_ui import ClientUI
from udp_server_ui import UDPServerUI
from icon_pic import socket_ico

class SocketApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        # 创建选项卡
        tab_widget = QTabWidget()

        # 创建服务器选项卡
        server_tab = ServerUI()
        tab_widget.addTab(server_tab, "Server")

        # 创建客户端选项卡
        client_tab = ClientUI()
        tab_widget.addTab(client_tab, "Client")

        # 创建udp选项卡
        udp_tab = UDPServerUI()
        tab_widget.addTab(udp_tab, "Udp")

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        # 设置窗口属性
        self.setWindowTitle('Socket Utils')
        self.setGeometry(300, 300, 1200, 800)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SocketApp()
    # 设置窗口图标
    # 设置窗口图标
    logo = QPixmap()
    logo.loadFromData(base64.b64decode(socket_ico))
    icon = QIcon()
    icon.addPixmap(logo, QIcon.Normal, QIcon.Off)
    ex.setWindowIcon(icon)
    sys.exit(app.exec_())