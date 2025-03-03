import rumps
import os
import sys
import os.path as osp
import webbrowser
import subprocess
from base import  kill_process_by_pid, print, env


class PomodoroApp(object):
    def __init__(self):
        # 配置项中文化修改
        self.config = {
            "app_name": "番茄钟",
            "start": "开始计时",
            "pause": "暂停",
            "continue": "继续",
            "stop": "停止",
            "break_message": "时间到！该休息一下了 :)",
            "interval": 60 * 25,  # 25分钟，单位为秒
            "开发者": "https://github.com/zhangs-cedar/cedar-mac",
        }

        # self.app = rumps.App(self.config["app_name"], quit_button="退出")

        self.app = rumps.App(self.config["app_name"], quit_button=None)

        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]

        # 新增预设时长配置
        self.presets = {
            "1分钟": 60,
            "3分钟": 3 * 60,
            "5分钟": 5 * 60,
            "10分钟": 10 * 60,
            "15分钟": 15 * 60,
            "25分钟": 25 * 60,
            "30分钟": 30 * 60,
            "45分钟": 45 * 60,
        }

        self.set_up_menu()

        # 构建菜单项
        self.start_pause_button = rumps.MenuItem(
            title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(
            title=self.config["stop"], callback=None)

        # 新增设置菜单（带子菜单）
        self.settings_menu = rumps.MenuItem("设置时长")
        for preset in self.presets:
            self.settings_menu.add(rumps.MenuItem(
                preset, callback=self.set_duration))

        self.quit_button = rumps.MenuItem(
            "退出", callback=self.custom_quit)  # 添加退出按钮
        self.app.menu = [
            self.start_pause_button,
            self.stop_button,
            None,
            self.settings_menu,
            None,
            rumps.MenuItem("关于开发者", callback=self.open_website),
            self.quit_button,
        ]  # 添加分隔线  # 添加分隔线

        self.set_plugin_chat()

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "🍅"

    def open_website(self, _):
        webbrowser.open(
            "https://github.com/zhangs-cedar/cedar-mac")  # 替换你的目标网址

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            rumps.notification(
                title=self.config["app_name"], subtitle=self.config["break_message"], message="")  # 中文提示
            self.stop_timer()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = "{:2d}:{:02d}".format(mins, secs)
        sender.count += 1

    def set_duration(self, sender):
        """优化后的时长设置回调函数"""
        selected = sender.title
        # 原有逻辑保持不变
        self.interval = self.presets[selected]
        for item in self.settings_menu.values():
            item.state = 1 if item.title == selected else 0
        rumps.notification("设置成功", "", f"已设为 {selected}")

    def start_timer(self, sender):
        # 修改判断逻辑适配中文
        if sender.title in [self.config["start"], self.config["continue"]]:
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]  # 显示"暂停"
            self.timer.start()
        else:
            sender.title = self.config["continue"]  # 显示"继续"
            self.timer.stop()

    def stop_timer(self, _=None):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]  # 重置为"开始计时"

    def set_plugin_chat(self):
        """ """
        # 启动子进程

        print("Python 解释器路径: {}".format(env["python_exe"]))
        print("kjj.py 文件路径: {}".format(env["kjj_path"]))
        self.process = subprocess.Popen([env["python_exe"], env["kjj_path"],str(env)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout, stderr = self.process.communicate()
        # print(f"标准输出: {stdout.decode('utf-8')}")
        # print(f"错误输出: {stderr.decode('utf-8')}")

        print("子进程已启动，PID:", self.process.pid)
        # 主线程继续执行其他任务
        print("主线程继续执行...")

    def custom_quit(self, _):
        # 这里可以添加自定义逻辑，例如保存数据、关闭连接等
        print("执行自定义退出逻辑...")
        print("正在关闭子进程... {}".format(self.process.pid))
        kill_process_by_pid(self.process.pid)
        # 最后调用 rumps.quit_application() 退出应用
        rumps.quit_application()

    def run(self):
        print("App is running...")
        self.app.run()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
