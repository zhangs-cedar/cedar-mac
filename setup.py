from setuptools import setup

APP = ["pomodoro/kjj.py"]
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
        
    ),
    (
        "lib",["/opt/homebrew/opt/libffi/lib/libffi.8.dylib",
                "/opt/homebrew/opt/tcl-tk@8/lib/libtcl8.6.dylib",  #"libtk8.6.dylib"
                 "/opt/homebrew/opt/tcl-tk@8/lib/libtk8.6.dylib",
                 "/opt/homebrew/opt/openssl/lib/libssl.3.dylib",
                 "/opt/homebrew/opt/openssl/lib/libcrypto.3.dylib"
                 # /usr/local/lib/libssl.3.dylib   
                     # libcrypto.3.dylib   
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
    "frameworks": ["/opt/homebrew/opt/libffi/lib/libffi.8.dylib",
                   "/opt/homebrew/opt/tcl-tk@8/lib/libtcl8.6.dylib"
                   ],
}

        
setup(app=APP, name="Pomodoro", data_files=DATA_FILES, options={"py2app": OPTIONS}, setup_requires=["py2app"], install_requires=["rumps"])