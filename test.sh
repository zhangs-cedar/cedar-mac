rm -rf build dist
pip --version
python setup.py py2app
cp -r /Users/zhangsong/workspace/OpenSource/cedar-mac/lb/*  /Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Sandwich.app/Contents/Frameworks/
cd  dist/Sandwich.app/Contents/MacOS
./Sandwich
