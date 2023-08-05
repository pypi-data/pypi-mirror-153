__author__ = "Shreejaa Talla"
__source__ = "https://bitbucket.org/gsudmlab/filament_dataacquisition/src/master/data_acquisition/fileexplorer.py"
__modified__ = "yes"

import bisect
from sortedcontainers import SortedDict
from datetime import datetime


def get_timestamp_dict(bbso_json: dict) -> dict:
    """
    Gets a sorted dictionary with all timestamp values in bbso json file as keys and
    image ids as values.
    :param bbso_json: BBSO json file as input
    :return: the timestamp and image ids dictonary
    """
    images = bbso_json["images"]
    timestamp_dict = SortedDict({})
    for image in images:
        dt = datetime.strptime(image["date_captured"], '%Y-%m-%d %H:%M:%S')
        timestamp_dict[image['id']] = dt
    return timestamp_dict


def find_closest(q_time: datetime, timestamp_dict: dict) -> int:
    """
    finds the closest timestamp value for given q-time and return the index of timestamp
    dict.
    :param timestamp_dict: the dictionary of timestamps as keys and image ids as values.
    :param q_time: datetime for which the image id should be queried.
    :return: index of the closest timestamp
    Note: this code is based on the suggestions here:
            - https://stackoverflow.com/questions/8162379/python-locating-the-closest-timestamp
            - https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    """
    q_index = bisect.bisect_left(timestamp_dict.values(), q_time)
    if q_index >= len(timestamp_dict):  # if q_time occurs after the last time stamp
        q_index = q_index - 1
    elif q_index == 0:
        pass
    else:
        before_q_time = timestamp_dict.items()[q_index - 1][1]
        after_q_time = timestamp_dict.items()[q_index][1]
        diff_from_before = q_time - before_q_time
        diff_from_after = after_q_time - q_time
        q_index = (q_index if diff_from_after < diff_from_before else q_index - 1)
    return q_index
