import sys
import rumps
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """PyQt 窗口类"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt 窗口")
        self.setGeometry(100, 100, 400, 300)

        # 创建一个简单的布局
        layout = QVBoxLayout()
        label = QLabel("欢迎使用 PyQt 窗口！")
        button = QPushButton("点击我")
        button.clicked.connect(self.on_button_click)
        layout.addWidget(label)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_click(self):
        """按钮点击事件"""
        print("按钮被点击了！")


class StatusBarApp(rumps.App):
    """状态栏应用类"""
    def __init__(self, name, icon=None, title=None, menu=None):
        super().__init__(name, icon=icon, title=title, menu=menu)
        self.app = QApplication(sys.argv)  # 创建 PyQt 应用实例
        self.window = MainWindow()  # 创建 PyQt 窗口实例

    @rumps.clicked("显示 PyQt 窗口")
    def show_pyqt_window(self, _):
        """通过状态栏菜单项触发 PyQt 窗口显示"""
        self.window.show()

    @rumps.clicked("退出")
    def quit_app(self, _):
        """退出应用"""
        self.app.quit()
        rumps.quit()


if __name__ == "__main__":
    app = StatusBarApp("MyApp", icon="icon.png", title="状态栏应用")
    app.run()