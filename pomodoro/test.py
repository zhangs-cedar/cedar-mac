import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("内嵌网页浏览器")
        self.setGeometry(100, 100, 1000, 600)

        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建垂直布局
        layout = QVBoxLayout(main_widget)

        # 创建分割窗口
        splitter = QSplitter()

        # 创建左侧列表
        self.web_list = QListWidget()
        self.web_list.addItems(["kimi", "豆包", "deepseek","知乎"])
        self.web_list.itemClicked.connect(self.on_item_clicked)

        # 创建右侧网页显示区域
        self.stacked_widget = QStackedWidget()

        # 将左侧列表和右侧网页显示区域添加到分割窗口
        splitter.addWidget(self.web_list)
        splitter.addWidget(self.stacked_widget)

        # 设置分割窗口的初始大小比例
        splitter.setSizes([200, 800])

        # 将分割窗口添加到布局
        layout.addWidget(splitter)

        # 初始化网页
        self.init_web_pages()

    def init_web_pages(self):
        # 初始化每个网页的 QWebEngineView 实例并加载对应的 URL
        for item_text in ["kimi", "豆包", "deepseek","知乎"]:
            web_view = QWebEngineView()
            if item_text == "kimi":
                url = "https://www.kimi.com"
            elif item_text == "豆包":
                url = "https://www.doubao.com"
            elif item_text == "deepseek":
                url = "https://chat.deepseek.com"
            elif item_text == "知乎":
                url = "https://zhida.zhihu.com/"
            web_view.load(QUrl.fromUserInput(url))
            self.stacked_widget.addWidget(web_view)

        # 默认显示第一个网页
        self.stacked_widget.setCurrentIndex(0)

    def on_item_clicked(self, item):
        # 获取点击的列表项
        if item:
            # 切换到对应的网页
            index = self.web_list.row(item)
            self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())