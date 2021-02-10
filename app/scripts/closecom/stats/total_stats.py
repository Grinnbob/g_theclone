from .data import *
from .utils import *

def calc_total_percents(DATA=STATS_TOTAL):
    calc_percents(DATA)

def inc_total(stat, DATA=STATS_TOTAL):
    if not DATA.get(stat):
        DATA[stat] = 1
    else:
        DATA[stat] += 1

    return
