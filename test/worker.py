import time
import sys

def main():
    print("实际功能脚本已启动")
    counter = 0
    while True:
        print(f"工作中... {counter}")
        sys.stdout.flush()  # 确保输出立即显示
        time.sleep(1)
        counter += 1

if __name__ == "__main__":
    main()