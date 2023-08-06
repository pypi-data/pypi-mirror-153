import time

import pyautogui
import platform


class PcDriver(object):
    """windows和macos的驱动"""

    def __init__(self):
        self.driver = pyautogui

    @staticmethod
    def _adapt_point(x, y):
        """转换坐标"""
        plat = platform.platform()
        if plat.startswith('macOS'):
            x = x // 2
            y = y // 2
        return x, y

    def get_real_time_position(self):
        """实时获取当前鼠标坐标"""
        while True:
            print(self.driver.position())
            time.sleep(1)

    def click(self, x=None, y=None):
        """点击坐标点"""
        if x is not None and y is not None:
            x, y = self._adapt_point(x, y)
            self.driver.click(x, y)
        else:
            self.driver.click()

    def right_click(self, x, y):
        """右键坐标点"""
        x, y = self._adapt_point(x, y)
        self.driver.rightClick(x, y)

    def click_image(self, image_path):
        """点击图片"""
        x, y = self.driver.locateCenterOnScreen(image_path)
        self.click(x, y)

    def right_click_image(self, image_path):
        """右键图片"""
        x, y = self.driver.locateCenterOnScreen(image_path)
        self.right_click(x, y)

    def press(self, key_name):
        """键盘点击"""
        self.driver.press(key_name)

    def drag_to(self, x, y, duration=None):
        """按住并拖动"""
        x, y = self._adapt_point(x, y)
        if duration is not None:
            self.driver.dragTo(x, y, duration, button='left')
        else:
            self.driver.dragTo(x, y, button='left')

    def scroll(self, amount_to_scroll, x=None, y=None):
        """鼠标滚轮滚动"""
        x, y = self._adapt_point(x, y)
        if x is not None and y is not None:
            self.driver.scroll(amount_to_scroll, x=x, y=y)
        else:
            self.driver.scroll(amount_to_scroll)

    def move_to(self, x, y, duration=None):
        """移动光标位置"""
        x, y = self._adapt_point(x, y)
        if duration is not None:
            self.driver.moveTo(x, y, duration=duration)
        else:
            self.driver.moveTo(x, y)

    def set_text(self, text):
        """输入"""
        self.driver.typewrite(text)

    def set_hot_key(self, *args):
        """组合键"""
        self.driver.hotkey(*args)

    def screenshot(self, file_path):
        """截屏"""
        self.driver.screenshot(file_path)


if __name__ == '__main__':
    pass


