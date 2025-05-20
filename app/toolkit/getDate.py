from datetime import datetime


#截止到微秒
def get_current_time():
    """
    获取当前的日期和时间，包括年、月、日、时、分、秒、微秒
    :return: 当前的日期和时间对象
    """
    current_time = datetime.now()
    return current_time

#截止到日
def get_current_date():
    """
    获取当前的日期，包括年、月、日
    :return: 当前的日期对象
    """
    current_date = datetime.now().date()
    return current_date

#截止到秒
def get_current_time_str():
    """
    获取当前时间的字符串表示，格式为 'YYYY-MM-DD HH:MM:SS'
    :return: 当前时间的字符串表示
    """
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time_str


#到日截止
def get_current_date_str():
    """
    获取当前日期的字符串表示，格式为 'YYYY-MM-DD'
    :return: 当前日期的字符串表示
    """
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    return current_date_str


# 示例使用
# print(get_current_time())
# print(get_current_date())
# print(get_current_time_str())
# print(get_current_date_str())