import os
import time
import fire
import subprocess
from pynput import keyboard
from base import print


class ClipboardHotkeyHandler:
    def __init__(self, env):
        self.last_question = None
        self.env = env

    def on_activate(self):
        print("检测到热键触发")

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

        question = clipboard_content
        time.sleep(0.5)
        if question == self.last_question:
            print("重复提问,等待一会")
            time.sleep(1)

        self.last_question = question
        # 执行 Python 脚本
        process = subprocess.Popen(
            [self.env["python_exe"], self.env["chat_path"], question, str(self.env)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # 获取脚本的输出和错误信息
        stdout, stderr = process.communicate()
        print("输出:", stdout.decode("utf-8"))
        print("错误:", stderr.decode("utf-8"))
        # 获取脚本的返回码
        returncode = process.returncode
        print("返回码:", returncode)

    def kjj_run(self):
        with keyboard.GlobalHotKeys({"<cmd>+<space>": self.on_activate}) as h:
            print("监听已启动 (按 esc 退出)")
            h.join()  # 保持监听


def main(env):
    print("启动环境:", env)
    handler = ClipboardHotkeyHandler(env)
    handler.kjj_run()


if __name__ == "__main__":
    fire.Fire(main)
