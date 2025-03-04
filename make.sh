rm -rf build dist
pip --version
python setup.py py2app
cp -r /Users/zhangsong/workspace/OpenSource/cedar-mac/lb/*  /Users/zhangsong/workspace/OpenSource/cedar-mac/dist/Sandwich.app/Contents/Frameworks/
# open dist/Sandwich.app 
# chmod -R 777 ./dist/Sandwich.app
# sudo -s
# xattr -r -d com.apple.quarantine dist/Sandwich.app
# codesign -f -s - --deep dist/Sandwich.app
sudo open dist/Sandwich.app 


# xattr -r -d com.apple.quarantine dist/Sandwich.app