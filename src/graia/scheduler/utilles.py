from datetime import datetime, time, timedelta
from typing import Optional, Union


class EnteredRecord:
    def __init__(self) -> None:
        self.entered = False

    def __enter__(self) -> None:
        self.entered = True

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.entered = False


def print_track_async(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            import traceback

            traceback.print_exc()

    return wrapper


TimeObject = Union[datetime, timedelta, time, str, float]


def to_datetime(
    base: TimeObject,
    start: Optional[TimeObject] = None,
) -> datetime:
    """将适宜的对象转化为 datetime 类型.

    Args:
        base (TimeObject): 要转化的对象, 字符串应为 ISO 时间 / 日期格式, 浮点数为时间戳.
        start (Optional[TimeObject], optional): 用于计算开始时间的对象. 默认为 datetime.now().

    Raises:
        ValueError: 字符串格式错误.

    Returns:
        datetime: 转化成的 datetime.
    """
    if not start:
        start = datetime.now()
    else:
        start = to_datetime(start)
    if isinstance(base, datetime):
        return base
    elif isinstance(base, time):
        return datetime.fromisoformat(f"{start.date()} {base.isoformat()}")
    elif isinstance(base, timedelta):
        return start + base
    elif isinstance(base, float):
        return datetime.fromtimestamp(base)
    else:
        if "-" in base:  # Base is from datetime.isoformat()
            return datetime.fromisoformat(base)
        elif ":" in base:  # Base is from time.isoformat()
            return datetime.fromisoformat(f"{start.date()} {base}")
        else:
            raise ValueError("Expected an ISO style time string!")
