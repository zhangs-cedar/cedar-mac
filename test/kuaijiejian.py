import time
import subprocess
from pynput import keyboard
import threading

class CommandCHandler:
    def __init__(self):
        self.listener = None

    def block_system_shortcut(self):
        """通过创建临时监听器阻断系统默认响应"""
        def suppress(key):
            if key == keyboard.Key.cmd:
                return False  # 阻断信号
        with keyboard.Listener(on_press=suppress) as temp_listener:
            temp_listener.join()

    def handle_command_c(self):
        self.block_system_shortcut()
        print("⌘+C 已捕获 | 系统行为已屏蔽 | 执行自定义操作")

        # 获取剪切板内容
        try:
            clipboard_content = subprocess.check_output(['pbpaste'])
            print("剪贴板内容:", clipboard_content.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print("无法读取剪贴板内容:", e)

        # 执行 Python 脚本
        # process = subprocess.Popen(['python', '/Users/zhangsong/workspace/OpenSource/cedar-mac/pomodoro/chat.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # # 获取脚本的输出和错误信息
        # stdout, stderr = process.communicate()
        # # 打印输出和错误信息
        # print("标准输出:", stdout.decode('utf-8'))
        # print("标准错误:", stderr.decode('utf-8'))
        # # 获取脚本的返回码
        # returncode = process.returncode
        # print("返回码:", returncode)

    def on_command_c(self):
        # 使用线程异步处理耗时操作
        threading.Thread(target=self.handle_command_c).start()

    def start(self):
        self.listener = keyboard.GlobalHotKeys({'<cmd>+c': self.on_command_c})
        self.listener.start()
        print("监听器已启动 → 按 ⌘+C 测试")
        # 可以考虑使用更高效的方式保持主线程运行
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.listener.stop()

if __name__ == "__main__":
    CommandCHandler().start()