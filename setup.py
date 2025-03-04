from setuptools import setup

APP = ['pomodoro/test.py']
APP_NAME = 'Sandwich'
DATA_FILES = [
    (
        "pomodoro",
        [
            "pomodoro/icon.png",
            "pomodoro/config.json5",
            "pomodoro/base.py",
            "pomodoro/chat.py",
        ],

    ), 

]
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "pomodoro/icon.png", 
    'plist': {
        'CFBundleName': APP_NAME,     # 应用名
        'CFBundleDisplayName': APP_NAME,  # 应用显示名
        'CFBundleVersion': '1.0.0',      # 应用版本号
        'CFBundleIdentifier': APP_NAME,  # 应用包名、唯一标识
        'NSHumanReadableCopyright': 'Copyright © 2021 SW Felix.Zhao. All rights reserved.',  # 可读版权
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
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
