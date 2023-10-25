import enum

PENELCO_1_MARGIN = 40
PENELCO_1_WIDTH = 482
PENELCO_2_MARGIN = 28
PENELCO_2_WIDTH = 489


class NoticeType(enum.IntEnum):
    NGCP = enum.auto()      # The green and yellow image
    PENELCO_1 = enum.auto() # With the `Purpose` box
    PENELCO_2 = enum.auto() # Without the `Purpose` box

    def image_resolution(self) -> tuple[int, int]:
        match self:
            case NoticeType.NGCP:
                return 1650, 1275
            case NoticeType.PENELCO_1 | NoticeType.PENELCO_2:
                return 1280, 720

    def discriminant_pixel_color(self) -> tuple[int, int, int]:
        """Pixel color around the upper-left of the image"""
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
