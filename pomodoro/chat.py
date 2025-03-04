import fire
import os.path as osp
import tkinter as tk
from openai import OpenAI
import multiprocessing
import subprocess
import time
from threading import Thread
from pynput import keyboard
from base import read_json, env
from cedar.utils import logger, init_logger

init_logger(log_file=env["log_path"])

class QuickAnswerApp:
    def __init__(self, env):
        # 初始化主窗口
        self.env = env
        config = read_json(self.env["config_path"])
        self.root = tk.Tk()
        self.config = config["chat_plugin"]
        self.last_question = None
        self.question = "你是谁"
        self.kjj()  # 进程：快捷键监控触发
        self.setup_window()
        self.create_text_box()

    def on_activate(self):
        logger.info("检测到热键触发")
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)
        # 获取用户输入,执行 command + c
        process = subprocess.Popen(
            ["osascript", "-e",
             'tell application "System Events" to keystroke "c" using {command down}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # 获取脚本的输出和错误信息
        stdout, stderr = process.communicate()
        # 获取剪贴版
        try:
            clipboard_content = subprocess.check_output(["pbpaste"])
            print("剪贴板内容:", clipboard_content.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            print("无法读取剪贴板内容:", e)
            return

        question = clipboard_content.decode("utf-8")
        time.sleep(0.5)
        if question == self.last_question:
            print("重复提问,等待一会")
            time.sleep(1)
            self.last_question = None
            return

        self.last_question = question
        self.question = question
        print("用户输入:", question)
        self.stream_response()

    def worker(self):
        with keyboard.GlobalHotKeys({"<cmd>+<space>": self.on_activate}) as h:
            logger.info("监听已启动 (按 esc 退出)")
            h.join()  # 保持监听

    def kjj(self):
        # 启动流式请求,daemon=True表示该线程为守护线程，即主线程结束时，该线程也会被强制终止
        Thread(target=self.worker, daemon=True).start()

    def setup_window(self):
        # 设置窗口的位置和属性
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - 400) // 2
        y_offset = (screen_height - 150) // 5
        self.root.geometry(f"+{x_offset}+{y_offset}")
        self.root.tk.call("wm", "attributes", ".", "-topmost", True)
        self.root.tk.call("wm", "command", ".", "raise")
        self.root.title("快捷回答")
        self.root.geometry("400x150")

    def create_text_box(self):
        # 创建仿Mac风格的文本框
        self.text_box = tk.Text(
            self.root,
            wrap=tk.WORD,
            font=("San Francisco", 12),
            bg="#333233",
            highlightthickness=0,
        )
        self.text_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def stream_response(self):
        try:
            # 初始化OpenAI客户端
            client = OpenAI(
                api_key=self.config["api_key"],
                base_url=self.config["base_url"],
            )
            # 创建流式请求
            stream = client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {
                        "role": "system",
                        "content": self.config["system_content"],
                    },
                    {"role": "user", "content": self.question},
                ],
                temperature=0.1,
                stream=True,
            )
            # 处理流式响应
            first_chunk = True  # 标记是否是第一个有效内容块
            for i,chunk in enumerate(stream):
                if first_chunk:
                    # 如果是第一个有效内容块，插入分割符
                    self.root.after(0, lambda: self.text_box.insert(tk.END, "\n---------------------\n"))
                    first_chunk = False  # 标记已处理第一个有效内容块
                if chunk.choices[0].delta.content:
                    self.root.after(0, lambda c=chunk: self.text_box.insert(
                        tk.END, c.choices[0].delta.content))
                    self.root.after(0, self.text_box.see, tk.END)
        except Exception as e:
            # 捕获其他异常并显示错误信息
            self.root.after(0, lambda: self.text_box.insert(tk.END, "\n---------------------\n"))
            error_message = f"出现未知错误: {str(e)}"
            self.root.after(0, lambda: self.text_box.insert(
                tk.END, error_message))

    def run(self):
        # 运行主循环
        self.root.mainloop()


if __name__ == "__main__":
    app = QuickAnswerApp(env)
    app.run()
