import datetime
import pytesseract
import re

from enum import IntEnum
from PIL import Image, ImageEnhance, ImageFilter
from PIL.Image import Resampling


PENELCO_1_MARGIN = 40
PENELCO_1_WIDTH = 482
PENELCO_2_MARGIN = 28
PENELCO_2_WIDTH = 489

date_regex = re.compile(r"([a-zA-Z]+)\s+(\d+),\s+(\d+)")
time_regex = re.compile(r"([0123456789oOQ]+):([01345oOQ]+)(AM|PM)")
zero_like = re.compile(r"[oOQ]")

month_mapping = {
    "JANUARY": 1,
    "FEBRUARY": 2,
    "MARCH": 3,
    "APRIL": 4,
    "MAY": 5,
    "JUNE": 6,
    "JULY": 7,
    "AUGUST": 8,
    "SEPTEMBER": 9,
    "OCTOBER": 10,
    "NOVEMBER": 11,
    "DECEMBER": 12
}

def callback(r, g, b):
    if g > 50 or r > 50 or b > 50:
        return (255, 255, 255)
    else:
        return (r, g, b)
COLOR3DLUT = ImageFilter.Color3DLUT.generate(32, callback)

class NoticeType(IntEnum):
    NGCP = 0  # The green and yellow image
    PENELCO_1 = 1  # With the `Purpose` box
    PENELCO_2 = 2  # Without the `Purpose` box

    def image_resolution(self) -> tuple[int, int]:
        match self:
            case NoticeType.NGCP:
                return 1650, 1275
            case NoticeType.PENELCO_1 | NoticeType.PENELCO_2:
                return 1280, 720

    def discriminant_pixel_color(self) -> tuple[int, int, int]:
        match self:
            case NoticeType.NGCP:
                return (255, 255, 0)  # yellow
            case NoticeType.PENELCO_1:
                return (37, 37, 37)  # dark gray
            case NoticeType.PENELCO_2:
                return (255, 255, 255)  # white

    def date_box(self) -> tuple[int, int, int, int]:
        match self:
            case NoticeType.NGCP:
                LEFT = 111
                TOP = 258
                WIDTH = 685
                HEIGHT = 105
                return (LEFT, TOP, LEFT + WIDTH, TOP + HEIGHT)
            case NoticeType.PENELCO_1:
                TOP = 190
                HEIGHT = 55
                return (
                    PENELCO_1_MARGIN,
                    TOP,
                    PENELCO_1_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )
            case NoticeType.PENELCO_2:
                TOP = 213
                HEIGHT = 83
                return (
                    PENELCO_2_MARGIN,
                    TOP,
                    PENELCO_2_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )

    def time_box(self) -> tuple[int, int, int, int]:
        match self:
            case NoticeType.NGCP:
                LEFT = 111
                TOP = 380
                WIDTH = 685
                HEIGHT = 120
                return (LEFT, TOP, LEFT + WIDTH, TOP + HEIGHT)
            case NoticeType.PENELCO_1:
                TOP = 306
                HEIGHT = 40
                return (
                    PENELCO_1_MARGIN,
                    TOP,
                    PENELCO_1_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )
            case NoticeType.PENELCO_2:
                TOP = 360
                HEIGHT = 61
                return (
                    PENELCO_2_MARGIN,
                    TOP,
                    PENELCO_2_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )

    def activity_box(self) -> tuple[int, int, int, int]:
        match self:
            case NoticeType.NGCP:
                LEFT = 815
                TOP = 297
                WIDTH = 825
                HEIGHT = 240
                return (LEFT, TOP, LEFT + WIDTH, TOP + HEIGHT)
            case NoticeType.PENELCO_1:
                TOP = 411
                HEIGHT = 102
                return (
                    PENELCO_1_MARGIN,
                    TOP,
                    PENELCO_1_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )
            case NoticeType.PENELCO_2:
                TOP = 488
                HEIGHT = 139
                return (
                    PENELCO_2_MARGIN,
                    TOP,
                    PENELCO_2_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )

    def purpose_box(self) -> tuple[int, int, int, int] | None:
        match self:
            case NoticeType.NGCP:
                return None
            case NoticeType.PENELCO_1:
                TOP = 576
                HEIGHT = 73
                return (
                    PENELCO_1_MARGIN,
                    TOP,
                    PENELCO_1_MARGIN + PENELCO_1_WIDTH,
                    TOP + HEIGHT,
                )
            case NoticeType.PENELCO_2:
                return None

    def affected_areas_box(self) -> tuple[int, int, int, int]:
        match self:
            case NoticeType.NGCP:
                LEFT = 5
                TOP = 546
                WIDTH = 1645
                HEIGHT = 439
                return (LEFT, TOP, LEFT + WIDTH, TOP + HEIGHT)
            case NoticeType.PENELCO_1:
                LEFT = 558
                TOP = 221
                WIDTH = 677
                HEIGHT = 427
                return (LEFT, TOP, LEFT + WIDTH, TOP + HEIGHT)
            case NoticeType.PENELCO_2:
                LEFT = 548
                TOP = 214
                WIDTH = 678
                HEIGHT = 410
                return (LEFT, TOP, LEFT + WIDTH, TOP + HEIGHT)


def is_same_color(color_a: tuple[int, int, int], color_b: tuple[int, int, int]) -> bool:
    """Fuzzy match if the given colors are the same"""

    COLOR_THRESHOLD = 10

    return sum(map(lambda x: abs(x[0] - x[1]), zip(color_a, color_b))) < COLOR_THRESHOLD


class Notice:
    PIXEL_COORD = (0, 40)
    COLOR_THRESHOLD = 10

    def __init__(self, image: Image):
        self.notice_type = Notice.check_notice_type(image)
        self.image = image

    @staticmethod
    def check_notice_type(image: Image) -> NoticeType:
        resolution = image.width, image.height
        pixel_color = image.getpixel(Notice.PIXEL_COORD)

        notice_types = [NoticeType.NGCP, NoticeType.PENELCO_1, NoticeType.PENELCO_2]
        for notice_type in notice_types:
            if notice_type.image_resolution() == resolution and is_same_color(
                pixel_color, notice_type.discriminant_pixel_color()
            ):
                return notice_type

        raise Exception("Unknown notice type")

    def get_date(self) -> datetime.date | None:
        cropped = self.image.crop(self.notice_type.date_box())
        text = pytesseract.image_to_string(cropped)
        m = date_regex.match(text)
        if m:
            #TODO: Handle possible typo
            month = month_mapping[m.group(1).upper()]

            day = int(m.group(2))
            year = int(m.group(3))
            return datetime.date(year, month, day)
        return None
    
    def get_time(self) -> list[tuple[datetime.time, datetime.time]]:

        image = self.image.crop(self.notice_type.time_box())

        def preprocessing(image):
            WIDTH_SCALE = 8
            HEIGHT_SCALE = 8

            image = image.resize((WIDTH_SCALE * image.width, HEIGHT_SCALE * image.height), Resampling.LANCZOS)

            # image = image.point(NGCP_TIME_BOX_LUT)
            image = image.filter(COLOR3DLUT)
            image = image.filter(filter=ImageFilter.GaussianBlur(radius=2))

            enhance = ImageEnhance.Contrast(image)
            image = enhance.enhance(5.0)
            
            return image

        def parse_time(m):
            hour = int(zero_like.sub("0", m[0]))
            match m[2]:
                case "AM":
                    if hour == 12:
                        hour = 0
                case "PM":
                    if hour < 12:
                        hour += 12
            minute = int(zero_like.sub("0", m[1]))
            return datetime.time(hour, minute)
        
        def parse_time_range(text):
            time = []
            matches = time_regex.findall(text)
            # print('>>>', text)
            assert len(matches) > 0 and len(matches) % 2 == 0

            for i in range(0, len(matches), 2):
                start = parse_time(matches[i])
                end = parse_time(matches[i + 1])
                time.append((start, end))
            return time

        image = preprocessing(image)
        config = "--oem 1 --psm 7"
        try:
            text = pytesseract.image_to_string(image, config=config)
            return parse_time_range(text)
        except AssertionError:
            image = image.resize((image.width, image.height // 4), Resampling.LANCZOS)
            text = pytesseract.image_to_string(image, config=config)
            try:
                return parse_time_range(text)
            except AssertionError:
                return []



# from selenium import webdriver
# from selenium.webdriver.common.by import By

# driver = webdriver.Firefox()

# driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# title = driver.title

# driver.implicitly_wait(0.5)

# text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# text_box.send_keys("Selenium")
# submit_button.click()

# message = driver.find_element(by=By.ID, value="message")
# text = message.text

# driver.quit()
