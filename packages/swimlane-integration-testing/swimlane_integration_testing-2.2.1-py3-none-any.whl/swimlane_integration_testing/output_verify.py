import validators
import phonenumbers
import json
import re
from datetime import datetime
from math import ceil, log
from dateutil import parser


def is_string(v):
    return isinstance(v, str)


def is_number(v):
    return isinstance(v, (int, float))


def is_list(v):
    return isinstance(v, list)


def is_json(v):
    try:
        json.loads(json.dumps(v))
        return True
    except Exception:
        return False


def is_bool(v):
    return isinstance(v, bool)


def is_epoch(v):
    try:
        return ceil(log(v, 10)) == 10
    except Exception:
        return False


def is_epoch_ms(v):
    try:
        return ceil(log(v, 10)) == 13
    except Exception:
        return False


def is_iso8601(v):
    try:
        parser.isoparse(v)
        return True
    except Exception:
        return False

def is_date(v):
    # todo: make this regex more exact, idk what platform is looking for currently
    if isinstance(v, str):
        found = re.findall(r"(\d){1,2}/(\d){1,2}/((\d){4}|(\d){2})", v)
        if found:
            return True
    return False


def is_email(v):
    return validators.email(v)


def is_url(v):
    return validators.url(v)


def is_telephone(v):
    # todo: test
    return phonenumbers.is_valid_number(phonenumbers.parse(v))


def is_ip(v):
    return validators.ipv4(v) or validators.ipv6(v)


def is_time(v):
    # todo: test
    time = False
    if isinstance(v, str):
        time = re.findall('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v)
    if time:
        return True
    else:
        return False


def is_attachment(v):
    if isinstance(v, list):
        for a in v:
            if not all(key in a for key in ['filename', 'base64']):
                return False
    else:
        return False
    return True


def is_numeric_list(v):
    return isinstance(v, list) and all(isinstance(x, (int, float)) for x in v)


def is_category(v):
    # todo - is this ever a thing?
    raise NotImplementedError()


OUTPUT_MAP = {
    1: is_string,  # string
    2: is_string,  # text area
    3: is_string,  # code
    4: is_string,  # password
    5: is_list,    # string list
    6: is_number,
    7: is_bool,
    8: is_iso8601,
    9: is_json,
    10: is_epoch,
    11: is_epoch_ms,
    12: is_date,
    13: is_email,
    14: is_url,
    15: is_telephone,
    16: is_ip,
    17: is_time,
    18: is_attachment,
    19: is_numeric_list,
    20: is_list
}

