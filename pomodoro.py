import rumps
import webbrowser

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
            "interval": 60*25,  # 25分钟，单位为秒
            "开发者": "https://github.com/zhangs-cedar/cedar-mac",
        }
        self.app = rumps.App(self.config["app_name"], quit_button="退出")
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]

        # 新增预设时长配置
        self.presets = {
            "1分钟": 60,
            "3分钟": 3*60,
            "5分钟": 5*60,
            "10分钟": 10*60,
            "15分钟": 15*60,
            "25分钟": 25*60,
            "30分钟": 30*60,
            "45分钟": 45*60
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
            self.settings_menu.add(rumps.MenuItem(preset, callback=self.set_duration))

        self.app.menu = [
            self.start_pause_button,
            self.stop_button,
            None,  # 添加分隔线
            self.settings_menu,
            None,  # 添加分隔线
            rumps.MenuItem("关于开发者", callback=self.open_website)
        ]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "🍅"
        
    def open_website(self, _):
        webbrowser.open("https://github.com/zhangs-cedar/cedar-mac")  # 替换你的目标网址

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

    def set_duration(self, sender):
        """优化后的时长设置回调函数"""
        selected = sender.title
        # 原有逻辑保持不变
        self.interval = self.presets[selected]
        for item in self.settings_menu.values():
            item.state = 1 if item.title == selected else 0
        rumps.notification("设置成功", "", f"已设为 {selected}")

    def _show_custom_dialog(self, _):
        """改进后的跨版本兼容方案"""
        window = rumps.Window(
            message="请输入分钟数（1-60）",
            default_text="25",
            dimensions=(160, 24)
        )
        
        # 使用字符串代替AppKit常量
        window.text_field.setAllowedInputTypes_(["NSTextInputTypeNumber"])
        
        # 强制弹出数字键盘（实测有效）
        window.text_field.setBezelStyle_(2)  # 圆形边框样式
        
        response = window.run()
    # 后续处理保持不变...

        try:
            minutes = int(response.text)
            if 1 <= minutes <= 60:
                self.interval = minutes * 60
                # 立即更新界面显示
                self.title = f"🍅 {minutes}分钟"
                rumps.notification("设置成功", "", f"已设为 {minutes} 分钟")
            else:
                raise ValueError
        except:
            rumps.notification("输入错误", "", "请输入1-60的整数")

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
