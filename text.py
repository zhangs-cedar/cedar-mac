import subprocess

kjj_path = "/Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Pomodoro.app/Contents/Resources/pomodoro/kjj.py" # 替换为实际的 kjj.py 文件路径
python_path = "/Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Pomodoro.app/Contents/MacOS/python"

print(f"Python 解释器路径: {python_path}")
print(f"kjj.py 文件路径: {kjj_path}")

try:
    process = subprocess.Popen([python_path, kjj_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(f"标准输出: {stdout.decode('utf-8')}")
    print(f"错误输出: {stderr.decode('utf-8')}")
except FileNotFoundError:
    print("指定的文件或命令未找到，请检查路径。")