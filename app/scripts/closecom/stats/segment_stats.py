from .data import *
from .utils import *

def calc_segment_percents(DATA=STATS_SEGMENT):
    for segment_name, segment_data in DATA.items():
        calc_percents(segment_data)

        sequences = segment_data.get("sequences", {})
        for seq_name, seq_data in sequences.items():
            calc_percents(seq_data)

            templates = seq_data.get("templates", {})
            for tmpl_name, tmpl_data in templates.items():
                calc_percents(tmpl_data)

def inc_segment(stat,
                segment_name,
                sequence_name,
                template_name,
                DATA=STATS_SEGMENT):

    # CHECK or create segment
    if not DATA.get(segment_name):
        DATA[segment_name] = {}

    SEGMENT_DATA = DATA[segment_name]
    if not SEGMENT_DATA.get(stat):
        SEGMENT_DATA[stat] = 1
    else:
        SEGMENT_DATA[stat] += 1

    if not SEGMENT_DATA.get('sequences'):
        SEGMENT_DATA['sequences'] = {}

    SEGMENT_SEQUENCES = SEGMENT_DATA['sequences']

    # CHECK or create sequence inside segment
    if not SEGMENT_SEQUENCES.get(sequence_name):
        SEGMENT_SEQUENCES[sequence_name] = {}

    SEQUENCE_DATA = SEGMENT_SEQUENCES[sequence_name]

    if not SEQUENCE_DATA.get(stat):
        SEQUENCE_DATA[stat] = 1
    else:
        SEQUENCE_DATA[stat] += 1

    # CHECK or create templates inside sequence
    if not SEQUENCE_DATA.get('templates'):
        SEQUENCE_DATA['templates'] = {}

    TEMPLATES = SEQUENCE_DATA['templates']

    # CHECK or create template_name inside sequence.templates
    if not TEMPLATES.get(template_name):
        TEMPLATES[template_name] = {}

    TMPL = TEMPLATES[template_name]
    if not TMPL.get(stat):
        TMPL[stat] = 1
    else:
        TMPL[stat] += 1

