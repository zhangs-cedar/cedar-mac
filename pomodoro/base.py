import sys
import os.path as osp
import subprocess

if getattr(sys, "frozen", False):
    print("打包后的应用")
    # /Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Pomodoro.app/Contents/Resources
    base_path = osp.dirname(osp.dirname(sys.argv[0]))
    python_exe = osp.join(base_path, "MacOS", "python")
    kjj_path = osp.join(base_path, "Resources", "pomodoro", "kjj.py")
    chat_path = osp.join(base_path, "Resources", "pomodoro", "chat.py")
    config_path = osp.join(base_path, "Resources", "pomodoro", "config.json5")

    # 定义 _ctypes.so 和 libffi.8.dylib 的路径
    ctypes_so_path = osp.join(base_path, "Resources", "lib", "python3.10", "lib-dynload", "_ctypes.so")
    libffi_path = osp.join(base_path, "Frameworks", "libffi.8.dylib")

    # 修改 _ctypes.so 引用的 libffi.8.dylib 路径
    try:
        subprocess.run(["install_name_tool", "-change", "@rpath/libffi.8.dylib", libffi_path, ctypes_so_path], check=True)
        print("路径修改成功！")
    except subprocess.CalledProcessError as e:
        print(f"路径修改失败: {e}")

    # 验证修改结果
    try:
        result = subprocess.run(["otool", "-L", ctypes_so_path], capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"验证失败: {e}")
        
else:
    print("开发环境")
    base_path = osp.dirname(osp.abspath(__file__))
    python_exe = "python"
    kjj_path = osp.join(base_path, "kjj.py")
    chat_path = osp.join(base_path, "chat.py")
    config_path = osp.join(base_path, "config.json5")
