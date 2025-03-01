from setuptools import setup

APP = ["pomodoro/pomodoro.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "pomodoro/icon.png",  # 可选：添加应用图标
    "plist": {
        "CFBundleShortVersionString": "0.2.0",
        "LSUIElement": True,
    },
    "packages": ["rumps"],
    "frameworks": ["/opt/homebrew/opt/libffi/lib/libffi.8.dylib"],
}

setup(app=APP, name="Pomodoro", data_files=DATA_FILES, options={"py2app": OPTIONS}, setup_requires=["py2app"], install_requires=["rumps"])
