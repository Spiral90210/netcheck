import humanfriendly
from netcheck import checks
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
# Need to so a strange import here to work around IDE bug
# from kivy.properties import StringProperty
import kivy.properties as props
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from netcheck import checks
import signal
import sys


# Set to True for much faster testing of layouts
NETCHECK_FAKE = False
# test_result = checks.execute_test()
# print(f"{test_result['name']} :: down: {humanfriendly.format_size(test_result['down_speed'])}, up: {humanfriendly.format_size(test_result['up_speed'])}")


def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


class MainLayout(BoxLayout):
    def run_update(self, dt):
        Logger.info("Main View: Updating")
        # Not like windows - GUI updates are blocked until control returned
        # self.ids['btn_refresh'].text="refreshing..."
        check = checks.execute_test() if NETCHECK_FAKE else checks.execute()
        self.ids['cur_result'].update_check(check)
        self.ids['btn_refresh'].disabled = False
        Logger.info("Main View: Update finished")

    def before_update(self):
        self.ids['btn_refresh'].text = "refreshing..."
        self.ids['btn_refresh'].disabled = True


class CurrentResult(BoxLayout):
    name = props.StringProperty("-")
    down_speed = props.StringProperty("Loading...")
    up_speed = props.StringProperty("-")

    def update_check(self, new_check):
        self.name = new_check['name']
        self.down_speed = humanfriendly.format_size(
            new_check["down_speed"]) + "/s"
        self.up_speed = humanfriendly.format_size(new_check['up_speed']) + "/s"


class NetcheckApp(App):
    def build(self):
        """ Overriding the build method to return a new root widget"""
        self.main_layout = MainLayout()
        return self.main_layout

    def on_start(self):
        # Run an initial check, then schedule more every 5 mins
        self.main_layout.before_update()
        Clock.schedule_once(self.do_update_check, 5)
        Clock.schedule_interval(self.do_update_check, 300)
        super().on_start()

    def do_update_check(self, dt):
        self.main_layout.run_update(dt)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda x, y:  sys.exit(128 + signal.SIGINT))
    Window.size = (800, 480)
    NetcheckApp().run()
