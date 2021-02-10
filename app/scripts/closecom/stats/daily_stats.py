from .data import *
from .utils import *

def calc_daily_percents(DATA=STATS_DAILY):
    for day, data in DATA.items():
        calc_percents(data)

def inc_daily_lead_status(stat,
                          day,
                          DATA=STATS_DAILY):
    if not DATA.get(day):
        DATA[day] = {}

    DAILY = DATA[day]
    if not DAILY.get(stat):
        DAILY[stat] = 1
    else:
        DAILY[stat] += 1

def inc_daily(stat, email_data, DATA=STATS_DAILY):
    date_created = to_day(email_data.get('date_created'))

    if not DATA.get(date_created):
        DATA[date_created] = {}

    DAILY = DATA[date_created]
    if not DAILY.get(stat):
        DAILY[stat] = 1
    else:
        DAILY[stat] += 1

    return
