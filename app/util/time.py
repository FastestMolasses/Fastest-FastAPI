from datetime import datetime, timezone


def iso8601ToTimestamp(iso8601: str) -> int:
    """
        Converts an ISO8601 string to a timestamp.
    """
    if iso8601.count('.') == 1:
        dt = datetime.strptime(iso8601, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        dt = datetime.strptime(iso8601, '%Y-%m-%dT%H:%M:%S')

    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())
