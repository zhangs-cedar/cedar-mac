import sys
import os.path as osp

if getattr(sys, "frozen", False):
    print("打包后的应用")
    # /Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Pomodoro.app/Contents/Resources
    base_path = osp.dirname(osp.dirname(sys.argv[0]))
    python_exe = osp.join(base_path, "MacOS", "python")
    kjj_path = osp.join(base_path, "Resources", "pomodoro", "kjj.py")
    chat_path = osp.join(base_path, "Resources", "pomodoro", "chat.py")
    config_path = osp.join(base_path, "Resources", "pomodoro", "config.json5")
else:
    print("开发环境")
    base_path = osp.dirname(osp.abspath(__file__))
    python_exe = "python"
    kjj_path = osp.join(base_path, "kjj.py")
    chat_path = osp.join(base_path, "chat.py")
    config_path = osp.join(base_path, "config.json5")
