import datetime


def date2str(t: datetime.datetime, style: str) -> str:
    """
    eg:
        p.date2str(':') -> 2022:05:30
    :param t:
    :param style: [:,-,...]
    :return:
    """
    return t.strftime(f'%Y{style}%m{style}%d')


def str2date(t: str, style: str) -> datetime.datetime:
    """
    eg:
        str2date("2017:05:08", ":")
    :param t:
    :param style:
    :return:
    """
    return datetime.datetime.strptime(t, f'%Y{style}%m{style}%d')


def get_delta_time(t: datetime.datetime, delta_day) -> datetime:
    """
    eg:
        get_delta_time(now, -30),get_delta_time(now, 30)
    :param t:
    :param delta_day: +:未来，-：以前
    :return:
    """
    return t + datetime.timedelta(days=delta_day)


now = datetime.datetime.now

if __name__ == '__main__':
    t1 = get_delta_time(now, -30)
    print(t1)
