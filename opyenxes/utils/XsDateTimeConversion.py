from datetime import datetime, timedelta, timezone


def parse_date_time(date_time):
    """Transform the date in string format to datetime format

        :param date_time: The date in string format
        :type date_time: str
        :return: The date in datetime format
        :rtype: datetime
        """
    try:
        value = date_time
        relative_zone = ""
        if "Z" in value:
            value = value.replace("Z", "")
            relative_zone = "Z"
        elif "+" in value:
            relative_zone = value[value.index("+"):]
            value = value[:value.index("+")]

        elif "-" in value[::-1][:7]:
            value = value[::-1]
            relative_zone = value[:value.index("-") + 1]
            value = value[value.index("-") + 1:]
            relative_zone = relative_zone[::-1]
            value = value[::-1]

        if relative_zone != "Z" and relative_zone != "":
            hours, minute = relative_zone.split(":")
            if "-" in hours:
                minute = int(minute) * -1
        else:
            hours = 0
            minute = 0

        if '.' in value:
            time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

        time = time.replace(tzinfo=timezone(timedelta(minutes=int(minute), hours=int(hours))))
        return time

    except ValueError:
        print("\"" + date_time + "\" is not a valid representation of a XES timestamp.")
        return None
