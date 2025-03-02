import subprocess
from pynput import keyboard
import time

# 初始化上一次触发时间为 0
last_trigger_time = 0


def on_activate():
    global last_trigger_time
    current_time = time.time()
    # 检查当前时间与上一次触发时间的间隔是否小于 0.5 秒
    if current_time - last_trigger_time < 3:
        return
    # 更新上一次触发时间
    last_trigger_time = current_time
    print("检测到热键触发")
    # 执行 Python 脚本
    process = subprocess.Popen(
        ["python", "/Users/zhangsong/workspace/OpenSource/cedar-mac/pomodoro/chat.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # 获取脚本的输出和错误信息
    stdout, stderr = process.communicate()
    # 打印输出和错误信息
    print("标准输出:", stdout.decode("utf-8"))
    print("标准错误:", stderr.decode("utf-8"))
    # 获取脚本的返回码
    returncode = process.returncode
    print("返回码:", returncode)


with keyboard.GlobalHotKeys({"<cmd>+<space>": on_activate}) as h:
    print("监听已启动 (按 esc 退出)")
    h.join()  # 保持监听
