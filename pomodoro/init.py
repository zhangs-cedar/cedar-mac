import subprocess
import os.path as osp
import json5 as json
from s_print import print


script_directory = osp.dirname(osp.abspath(__file__))
kjj_path = osp.join(script_directory, "kjj.py")
chat_path = osp.join(script_directory, "chat.py")
config_path = osp.join(script_directory, "config.json5")
print(kjj_path, chat_path, config_path)


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



