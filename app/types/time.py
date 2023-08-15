from enum import Enum


class TimeBucketInterval(str, Enum):
    FIVE_MIN = '5 min'
    FIFTEEN_MIN = '15 min'
    ONE_HOUR = '1 hour'
    ONE_DAY = '1 day'
    ONE_WEEK = '1 week'
    ONE_MONTH = '1 month'
    ONE_YEAR = '1 year'
