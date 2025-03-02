from pynput import keyboard
import time
from cedar.utils import run_subprocess


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

    def on_command_c(self):
        self.block_system_shortcut()
        print("⌘+C 已捕获 | 系统行为已屏蔽 | 执行自定义操作")
        

    def start(self):
        self.listener = keyboard.GlobalHotKeys({'<cmd>+c': self.on_command_c})
        self.listener.start()
        print("监听器已启动 → 按 ⌘+C 测试")
        while True:  # 防止主线程退出
            time.sleep(1)

if __name__ == "__main__":
    # CommandCHandler().start()
    run_subprocess("/Users/zhangsong/workspace/OpenSource/cedar-mac/pomodoro/chat.py")
