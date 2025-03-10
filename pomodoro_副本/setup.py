from setuptools import setup

APP = ["pomodoro/chat.py"]
APP_NAME = "pomodoro"
DATA_FILES = [
    (
        "pomodoro",
        [
            "pomodoro/icon.png",
            "pomodoro/config.json5",
            "pomodoro/base.py",
            "pomodoro/chat.py",
            "pomodoro/kjj.py",
            "pomodoro/pomodoro.py"
        ],

    ),  # /Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Pomodoro.app/Contents/Resources/lib/libssl.3.dylib
    # Pomodoro.app/Contents/Resources/lib/python3.10/lib-dynload/_ssl.so
    (
        "lib", ["/opt/homebrew/opt/libffi/lib/libffi.8.dylib",
                "/opt/homebrew/opt/tcl-tk@8/lib/libtcl8.6.dylib",
                "/opt/homebrew/opt/tcl-tk@8/lib/libtk8.6.dylib",
                "/opt/homebrew/opt/openssl/lib/libssl.3.dylib",
                "/opt/homebrew/opt/openssl/lib/libcrypto.3.dylib"
                ],
    )
]
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "pomodoro/icon.png",  # 可选：添加应用图标
    "plist": {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Making Sandwiches",
        'CFBundleIdentifier': "com.metachris.osx.sandwich",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2015, Chris Hager, All Rights Reserved",
        
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
    "frameworks": ["/opt/homebrew/opt/libffi/lib/libffi.8.dylib",
                   "/opt/homebrew/opt/tcl-tk@8/lib/libtcl8.6.dylib",
                   "/opt/homebrew/opt/tcl-tk@8/lib/libtk8.6.dylib",
                   "/opt/homebrew/opt/openssl/lib/libssl.3.dylib",
                   "/opt/homebrew/opt/openssl/lib/libcrypto.3.dylib"
                   ],

}


setup(app=APP, name="Pomodoro", data_files=DATA_FILES, options={
      "py2app": OPTIONS}, setup_requires=["py2app"], install_requires=["rumps"])
