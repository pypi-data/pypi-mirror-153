from datetime import timedelta


def format_duration(value: timedelta) -> str:
    """Format a timedelta to a duration string as HH:MM:SS or MM:SS."""
    if not value:
        return '--:--'
    result = []
    seconds = value.total_seconds()
    if seconds >= 3600:
        hours, seconds = divmod(seconds, 3600)
        result.append('{:02n}'.format(hours))
    minutes, seconds = divmod(seconds, 60)
    result.append('{:02n}'.format(minutes))
    result.append('{:02n}'.format(seconds))
    return ':'.join(result)
