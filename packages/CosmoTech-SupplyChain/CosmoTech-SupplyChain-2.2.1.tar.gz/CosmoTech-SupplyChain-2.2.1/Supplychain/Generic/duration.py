def seconds_to_iso_8061_duration(total_time_in_seconds: int) -> str:
    """
    Convert a duration in seconds to an iso 8061 formated string
    :param total_time_in_seconds: duration to convert
    :return: iso 8061 representation of the duration
    """
    time_left = total_time_in_seconds

    minute_duration = 60
    hour_duration = minute_duration * 60
    day_duration = hour_duration * 24

    days = time_left // day_duration
    time_left -= days * day_duration
    hours = time_left // hour_duration
    time_left -= hours * hour_duration
    minutes = time_left // minute_duration
    time_left -= minutes * minute_duration

    return f'P{days}DT{hours}H{minutes}M{time_left}S'
