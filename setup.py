from setuptools import setup

APP = ["pomodoro/pomodoro.py"]
DATA_FILES = [
    (
        "pomodoro",
        [
            "pomodoro/base.py",
            "pomodoro/s_print.py",
            "pomodoro/icon.png",
            "pomodoro/config.json5",
            "pomodoro/chat.py",
            "pomodoro/init.py",
            "pomodoro/kjj.py",
        ],
    )
]
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "pomodoro/icon.png",  # 可选：添加应用图标
    "plist": {
        "CFBundleShortVersionString": "0.2.0",
        "LSUIElement": True,
    },
    "packages": [
        "fire",
        "tkinter",
        "openai",
        "pynput",
        "rumps",
        "webbrowser",
        "json5",
    ],
    "excludes": [],
    "frameworks": ["/opt/homebrew/opt/libffi/lib/libffi.8.dylib"],
}

setup(app=APP, name="Pomodoro", data_files=DATA_FILES, options={"py2app": OPTIONS}, setup_requires=["py2app"], install_requires=["rumps"])
