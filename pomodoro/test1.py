import sys
import subprocess
import time
from openai import OpenAI
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from base import read_json, env
from cedar.utils import logger, init_logger

init_logger(log_file=env["log_path"])


class WorkerThread(QThread):
    """
        创建一个新的工作线程，用于处理用户输入和响应。
    """
    # 定义信号，用于在主线程中更新 UI
    update_text_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, env):
        super().__init__()
        self.env = env
        self.config = read_json(self.env["config_path"])["chat_plugin"]
        self.last_question = None

    def run(self):
        with keyboard.GlobalHotKeys({"<cmd>+<space>": self.on_activate}) as h:
            logger.info("监听已启动 (按 esc 退出)")
            h.join()  # 保持监听

    def on_activate(self):
        logger.info("检测到热键触发")
        # 获取用户输入，执行 command + c
        process = subprocess.Popen(
            ["osascript", "-e",
             'tell application "System Events" to keystroke "c" using {command down}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        try:
            clipboard_content = subprocess.check_output(["pbpaste"])
            question = clipboard_content.decode("utf-8")
            time.sleep(0.5)
            if question == self.last_question:
                logger.info("重复提问，等待一会")
                time.sleep(1)
                self.last_question = None
                return

            self.last_question = question
            logger.info(f"用户输入: {question}")
            self.stream_response(question)
        except subprocess.CalledProcessError as e:
            logger.error(f"无法读取剪贴板内容: {e}")

    def stream_response(self, question):
        try:
            client = OpenAI(
                api_key=self.config["api_key"],
                base_url=self.config["base_url"],
            )
            stream = client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": self.config["system_content"]},
                    {"role": "user", "content": question},
                ],
                temperature=0.3, # 设置温度为 0.5 以获得更可控的回答
                stream=True,
            )
            first_chunk = True
            for i, chunk in enumerate(stream):
                if first_chunk:
                    self.update_text_signal.emit("\n---------------------\n")
                    first_chunk = False
                if chunk.choices[0].delta.content:
                    logger.info(chunk.choices[0].delta.content)
                    content = chunk.choices[0].delta.content
                    self.update_text_signal.emit(content)
        except Exception as e:
            self.error_signal.emit(f"出现未知错误: {str(e)}")


class QuickAnswerApp(QMainWindow):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.init_ui()
        self.worker = WorkerThread(env)
        self.worker.update_text_signal.connect(self.update_text)
        self.worker.error_signal.connect(self.update_text)
        self.worker.start()

    def init_ui(self):
        self.setWindowTitle("快捷回答")
        self.setGeometry(100, 100, 400, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.text_box = QTextEdit(self)
        self.text_box.setFont(QFont("San Francisco", 12))
        self.text_box.setStyleSheet("background-color: #333233; border: none; color: white;")
        self.text_box.setReadOnly(True) # 设置为只读模式 
        # self.text_box.setWordWrapMode(Qt.TextWordWrap)  # 开启自动换行
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)

        container = QWidget() # 创建一个容器，用于包含布局
        container.setLayout(layout)
        self.setCentralWidget(container) # 将容器设置为窗口的中央部件

    def update_text(self, text):
        self.text_box.insertPlainText(text)
        self.text_box.verticalScrollBar().setValue(self.text_box.verticalScrollBar().maximum())


if __name__ == "__main__":
    logger.info("启动快捷回答")
    logger.info("{}".format(sys.argv))
    app = QApplication(sys.argv)
    window = QuickAnswerApp(env)
    window.show()
    sys.exit(app.exec_())