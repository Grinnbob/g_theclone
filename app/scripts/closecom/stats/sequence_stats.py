from .data import *
from .utils import *

def calc_sequence_percents(DATA=STATS_SEQUENCE):
    for seq_name, seq_data in DATA.items():
        calc_percents(seq_data)

        templates = seq_data.get("templates", {})
        if templates:
            for tmpl_name, tmpl_data in templates.items():
                calc_percents(tmpl_data)

def inc_sequence(stat,
                 sequence_name,
                 template_name,
                 DATA=STATS_SEQUENCE):

    if not DATA.get(sequence_name):
        DATA[sequence_name] = {}

    SEQUENCE_DATA = DATA[sequence_name]

    if not SEQUENCE_DATA.get(stat):
        SEQUENCE_DATA[stat] = 1
    else:
        SEQUENCE_DATA[stat] += 1

    if not SEQUENCE_DATA.get('templates'):
        SEQUENCE_DATA['templates'] = {}

    TEMPLATES = SEQUENCE_DATA['templates']

    if not TEMPLATES.get(template_name):
        TEMPLATES[template_name] = {}

    TMPL = TEMPLATES[template_name]
    if not TMPL.get(stat):
        TMPL[stat] = 1
    else:
        TMPL[stat] += 1
