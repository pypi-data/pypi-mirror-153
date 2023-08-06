import datetime
import time

from datetime import timedelta, timezone


def time_in_sp():
    'returns the date and time of sao paulo, UTC - 3:00'
    dh_now = datetime.datetime.now()
    diff = -timedelta(hours=3)
    fuso_horario = timezone(diff)
    dh_sao_paulo = dh_now.astimezone(fuso_horario)
    return dh_sao_paulo


def sleep(secs: float):
    'sleep for the seconds informed on the call'
    time.sleep(secs)