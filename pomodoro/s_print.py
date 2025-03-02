import os
import datetime
from base import base_path

# 定义全局日志文件路径
LOG_FILE = os.path.join(base_path, "s_print.log")
# 备份原始的 print 函数
original_print = print


# 定义自定义的 print 函数
def print(*args, sep=" ", end="\n", file=None):
    # 在输出前添加一个前缀
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[Print] [{current_time}]   "  # 添加时间戳到日志内容
    output_with_type = []
    for arg in args:
        arg_type = type(arg).__name__
        output_with_type.append(f"({arg_type}) {arg}    ")
    output = sep.join(output_with_type)
    output = prefix + output
    original_print(output, end=end)
    # 将输出写入到日志文件
    if file is None:
        file = LOG_FILE
    with open(file, "a", encoding="utf-8") as log_file:  # 使用追加模式
        log_file.write(output + "\n")  # 写入内容并换行
    # try:
    #     _ = sep.join(str(arg) for arg in args)
    #     Notifier.notify(_)
    # except:
    #     pass
    return output
