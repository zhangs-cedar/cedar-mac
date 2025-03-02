import subprocess
from pynput import keyboard
from init import print, chat_path, python_exe


def on_activate():
    print("检测到热键触发")
    # 获取用户输入,执行 command + c
    process = subprocess.Popen(
        ["osascript", "-e", 'tell application "System Events" to keystroke "c" using {command down}'],
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
    question = clipboard_content
    # 执行 Python 脚本
    process = subprocess.Popen(
        [python_exe, chat_path, question],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # 获取脚本的输出和错误信息
    stdout, stderr = process.communicate()
    # 打印输出和错误信息
    print("标准输出:", stdout.decode("utf-8"))
    print("标准错误:", stderr.decode("utf-8"))
    # 获取脚本的返回码
    returncode = process.returncode
    print("返回码:", returncode)


def kjj_run():
    with keyboard.GlobalHotKeys({"<cmd>+<space>": on_activate}) as h:
        print("监听已启动 (按 esc 退出)")
        h.join()  # 保持监听


if __name__ == "__main__":
    kjj_run()
