from setuptools import setup

APP = ['main.py']
DATA_FILES = ['worker.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'MyApp',
        'CFBundleDisplayName': 'My Application',
        'CFBundleVersion': '1.0.0',
    },
    'packages': [],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)