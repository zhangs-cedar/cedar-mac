#!/bin/bash

cd dist
# 尝试打开应用程序，并将输出和错误信息重定向到 1.log 文件
open "./Pomodoro.app" 2>&1 | tee 1.log

# 这里的 2>&1 是将标准错误输出重定向到标准输出，然后 tee 命令会将输出内容同时打印到终端和 1.log 文件中