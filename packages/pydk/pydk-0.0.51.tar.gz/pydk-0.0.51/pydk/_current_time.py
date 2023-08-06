
from datetime import datetime, timezone
import pytz


def _current_time(time_zone="America/New_York", formatting="%d%b%Y_%-I.%m.%S.%f"):

    """
    Return current time formatted as a string.

    Parameters:
    -----------
    time_zone
        Input to pytz.timezone()
        default: "America/New_York"
        type: str

    formatting
        Format the string
        default: "%d%b%Y_%-I.%m.%S%f"
        type: str

    Returns:
    --------
    current time formatted as a string

    Notes:
    ------

    """

    current_time = datetime.now(tz=pytz.timezone(time_zone))
    return current_time.strftime(formatting).upper()[
        :-4
    ]  # cut off 6 of the extra decimals for the seconds