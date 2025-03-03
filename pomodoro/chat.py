import fire
import os.path as osp
import tkinter as tk
from openai import OpenAI
from threading import Thread
from base import print, read_json


class QuickAnswerApp:
    def __init__(self, env):
        # 初始化主窗口
        self.env = env
        config = read_json(self.env["config_path"])
        self.root = tk.Tk()
        self.config = config["chat_plugin"]
        self.question = "讲一个故事，500字"
        self.setup_window()
        self.create_text_box()
        self.start_stream_response()

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
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    self.root.after(0, lambda c=chunk: self.text_box.insert(
                        tk.END, c.choices[0].delta.content))
                    self.root.after(0, self.text_box.see, tk.END)
        except Exception as e:
            # 捕获其他异常并显示错误信息
            error_message = f"出现未知错误: {str(e)}"
            self.root.after(0, lambda: self.text_box.insert(
                tk.END, error_message))

    def start_stream_response(self):
        # 在新线程中启动流式请求
        Thread(target=self.stream_response, daemon=True).start()

    def run(self, question):
        # 运行主循环
        self.question = question
        self.root.mainloop()


def main(question="解释一下什么是人工智能", env=None):
    """
    Args:
        question: 问题
    """
    # 创建并运行应用程序
    print(question)
    print(env)
    app = QuickAnswerApp(env)
    app.run(question)


if __name__ == "__main__":
    fire.Fire(main)
