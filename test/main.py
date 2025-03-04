import sys
import os
import subprocess
import signal

def get_resource_path(relative_path):
    """ 获取资源的绝对路径 """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    # 获取实际功能脚本路径
    worker_script = get_resource_path("worker.py")
    
    # 启动子进程
    process = subprocess.Popen(
        [sys.executable, worker_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 实时输出子进程日志
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            
    return process.poll()

if __name__ == "__main__":
    # 注册信号处理（用于macOS的优雅退出）
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)