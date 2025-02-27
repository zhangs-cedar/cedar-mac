import rumps


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
            "interval": 30  # 25分钟，单位为秒
        }
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.set_up_menu()
        # 菜单项使用中文配置
        self.start_pause_button = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title=self.config["stop"], callback=None)
        self.app.menu = [self.start_pause_button, self.stop_button]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "🍅"

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            rumps.notification(
                title=self.config["app_name"],
                subtitle=self.config["break_message"],  # 中文提示
                message='')
            self.stop_timer()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)
        sender.count += 1

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

    def run(self):
        self.app.run()

if __name__ == '__main__':
    app = PomodoroApp()
    app.run()
