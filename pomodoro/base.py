import sys
import datetime
import os.path as osp
import subprocess
import json5 as json

if getattr(sys, "frozen", False):
    print("打包后的应用")
    # /Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Pomodoro.app/Contents/Resources
    base_path = osp.dirname(osp.dirname(sys.argv[0]))
    python_exe = osp.join(base_path, "MacOS", "python")
    kjj_path = osp.join(base_path, "Resources", "pomodoro", "kjj.py")
    chat_path = osp.join(base_path, "Resources", "pomodoro", "chat.py")
    config_path = osp.join(base_path, "Resources", "pomodoro", "config.json5")
    log_path = osp.join(base_path, "Resources", "pomodoro", "pomodoro.log")

else:
    print("开发环境")
    base_path = osp.dirname(osp.abspath(__file__))
    python_exe = "python"
    kjj_path = osp.join(base_path, "kjj.py")
    chat_path = osp.join(base_path, "chat.py")
    config_path = osp.join(base_path, "config.json5")
    log_path = osp.join(base_path, "pomodoro.log")


def kill_process_by_pid(pid):
    try:
        # 调用 kill 命令发送 SIGTERM 信号给指定 PID 的进程
        subprocess.run(["kill", "-15", str(pid)], check=True)
        print(f"进程 {pid} 已成功关闭。")
    except subprocess.CalledProcessError as e:
        print(f"关闭进程 {pid} 时出错: {e}")


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data



# 定义全局日志文件路径
LOG_FILE = log_path
# 备份原始的 print 函数
original_print = print
# 定义自定义的 print 函数
def print(*args, sep=" ", end="\n", file=None):
    # 在输出前添加一个前缀
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[Print] [{current_time}]   "  # 添加时间戳到日志内容
    output_with_type = []
    for arg in args:
        arg_type = type(arg).__name__
        output_with_type.append(f"({arg_type}) {arg}    ")
    output = sep.join(output_with_type)
    output = prefix + output
    original_print(output, end=end)
    # 将输出写入到日志文件
    if file is None:
        file = LOG_FILE
    with open(file, "a", encoding="utf-8") as log_file:  # 使用追加模式
        log_file.write(output + "\n")  # 写入内容并换行
    return output


