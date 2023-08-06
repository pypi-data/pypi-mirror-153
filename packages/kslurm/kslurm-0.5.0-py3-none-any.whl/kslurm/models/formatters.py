from __future__ import absolute_import

import re

from kslurm.exceptions import ValidationError


def time(time: str):
    if ":" in time:
        if "-" in time:
            days, hhmm = time.split("-")
            hours, min = hhmm.split(":")
        else:
            days = "0"
            hours, min = time.split(":")
    else:
        raise TypeError(
            f'Invalid format for time: "{time}"\n'
            f"Must be as [xx-]xx:xx or x where x is a number"
        )
    return int(min) + int(hours) * 60 + int(days) * 60 * 24


def mem(mem: str):
    match = re.match(r"^([0-9]+)[GMgm][bB]?$", mem)
    if match:
        num = int(match.group(1))
    else:
        raise ValidationError(
            "Memory is not formatted correctly. Must be xxx(G|M)[B], e.g. 32G, 4000MB, "
            "etc"
        )
    if "G" in mem or "g" in mem:
        return num * 1000
    else:
        return num
