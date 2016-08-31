import os
import subprocess as sb
import logging
import time
import shlex


def robust_curl(curl_command, sleep_seconds=5):
    try:
        FNULL = open(os.devnull, 'w')
        res = sb.check_output(shlex.split(curl_command), stderr=FNULL)
        if res is not None and res.__contains__("The requested URL could not be retrieved"):
            logging.error("Access through proxy blocked")
            raise ValueError("Access through proxy blocked")
        time.sleep(sleep_seconds)
        return res
    except:
        logging.debug("failed try for curl_command : " + curl_command)
        raise


def get_attr(data, attr):
    if attr in data:
        return data[attr]
    return None
