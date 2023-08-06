import time
from baseImage import Image, Rect
from qrunner.core.image.matching import SIFT
from qrunner.utils.log import logger


class ImageRecognition:
    def __init__(self, im_source_path, im_search_path):
        self.im_source_path = im_source_path
        self.im_search_path = im_search_path
        self.im_source = Image(im_source_path)
        self.im_search = Image(im_search_path)

    @staticmethod
    def mark(source_path, rect):
        """画框"""
        img = Image(source_path)
        img.rectangle(Rect(*rect), color=(0, 0, 255), thickness=3)
        img.imwrite(source_path)

    def match(self):
        """图片匹配，只获取最佳匹配"""
        logger.debug(f'开始匹配: 从 {self.im_source_path} 中 查找 {self.im_search_path}')
        match = SIFT()
        start = time.time()
        result = match.find_all_results(self.im_source, self.im_search)
        logger.debug(f'匹配耗时: {time.time() - start}')
        try:
            rect_tuple = result[0]['rect'].totuple()
        except:
            logger.debug(f'匹配失败, 结果如下: \n{result}')
            match_data = None
        else:
            top_left_x, top_left_y, width, height = rect_tuple
            logger.debug(f'匹配成功, 结果如下: \n{result}')
            match_data = {
                "rect": rect_tuple,
                "center": (top_left_x + width // 2, top_left_y + height // 2)
            }
        return match_data


class ImageElement:
    def __init__(self, driver, target_path=None):
        if target_path is None:
            raise AssertionError('请输入图片路径')
        self.target_path = target_path
        self.driver = driver

    def find_element(self, retry=3, timeout=3):
        center = None
        for _ in range(retry):
            logger.debug(f'开始查找元素: {self.target_path}')
            shot_path = self.driver.screenshot('screenshot.png')
            img_reg = ImageRecognition(shot_path, self.target_path)
            match_data = img_reg.match()
            if match_data is not None:
                logger.debug(f'元素: {self.target_path} 查找成功，结果如下: {match_data}')
                rect = match_data.get('rect')
                ImageRecognition.mark(shot_path, rect)
                center = match_data.get('center')
                break
            else:
                logger.debug(f'元素: {self.target_path} 查找失败，重试！！！')
                for i in range(timeout):
                    logger.debug(f'{i+1}s后重试')
                    time.sleep(1)
        return center

    def get_element(self, retry=3, timeout=3):
        center = self.find_element(retry=retry, timeout=timeout)
        if center is None:
            self.driver.screenshot(f'[控件 {self.target_path} 定位失败]')
            raise AssertionError(f'[控件 {self.target_path} 定位失败]')
        else:
            return center

    def click(self):
        """暂时只支持安卓和ios"""
        logger.debug(f'点击: {self.target_path}')
        x, y = self.get_element()
        self.driver.click(x, y)
        logger.debug('点击成功')



