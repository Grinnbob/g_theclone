from .data import *
from tabulate import tabulate
import pandas as pd

pdtabulate=lambda df:tabulate(df,headers='keys',tablefmt='psql')

def _print_segment_stats(DATA=STATS_SEGMENT,
                         show=True):

    segment_stats = []
    best_dict = {}
    for segment_name, segment_data in DATA.items():
        segment_name_title = segment_name + '- total'
        if show:
            segment_name_title = segment_name[9:26] + '- total'

        from_dict = {
            segment_name_title : segment_data
        }
        best_dict[segment_name_title] = segment_data

        segment_stat = pd.DataFrame.from_dict(from_dict, orient='index', columns=SHOW_COLUMNS).fillna(0)

        if show:
            print(pdtabulate(segment_stat))

        segment_stats.append(segment_stat)

        sequences = segment_data.get("sequences", None)
        if sequences:
            res, best = _print_sequence_stats(DATA=sequences,
                                        show=show)
            if res:
                segment_stats.extend(res)

    best_segments_stat = pd.DataFrame.from_dict(best_dict, orient='index', columns=SHOW_COLUMNS).fillna(0)
    return segment_stats, best_segments_stat

def _print_daily_stats(DATA=STATS_DAILY,
                       show=True):
    from_dict = {}
    for day, day_data in DATA.items():
        from_dict[day] = day_data

    daily_stat = pd.DataFrame.from_dict(from_dict, orient='index', columns=SHOW_COLUMNS).fillna(0)
    if show:
        print(pdtabulate(daily_stat))

    return daily_stat

def _print_sequence_stats(DATA=STATS_SEQUENCE,
                          show=True):
    seq_stats = []
    best_dict = {}
    for seq_name, seq_data in DATA.items():
        seq_name_title = seq_name + '- total'
        if show:
            seq_name_title = seq_name[9:26] + '- total'

        from_dict = {
            seq_name_title : seq_data
        }
        best_dict[seq_name_title] = seq_data

        templates = seq_data.get('templates', None)
        if templates:
            for tmpl_name, tmpl_data in templates.items():
                tmpl_name_title = tmpl_name
                if show:
                    tmpl_name_title = tmpl_name[9:26]
                from_dict[tmpl_name_title] = tmpl_data

        sequence_stat = pd.DataFrame.from_dict(from_dict, orient='index', columns=SHOW_COLUMNS).fillna(0)
        seq_stats.append(sequence_stat)


        if show:
            print(pdtabulate(sequence_stat))

    best_sequences_stat = pd.DataFrame.from_dict(best_dict, orient='index', columns=SHOW_COLUMNS).fillna(0)
    return seq_stats, best_sequences_stat

def _print_total_stats(DATA=STATS_TOTAL,
                       show=True):
    stats_total = pd.DataFrame.from_records([DATA], columns=SHOW_TOTAL_COLUMNS).fillna(0)

    if show:
        print(pdtabulate(stats_total))

    return stats_total

def _print_email_to_status(DATA=EMAILS_TO_STATUS,
                           show=True):
    emails_stats = pd.DataFrame.from_dict(DATA, orient='index', columns=EMAILS_TO_STATUS_COLUMNS)

    if show:
        print(pdtabulate(emails_stats))

    return emails_stats


def print_all(customer):
    print(f"STATS FOR: customer={customer} date_from={FROM_TO_DATE['earliest']} date_to={FROM_TO_DATE['latest']}")

    _print_email_to_status()
    _print_total_stats()
    _print_daily_stats()
    _print_sequence_stats()
    _print_segment_stats()


def get_total_stats_df():
    return _print_total_stats(show=False)

def get_sequence_stats_df():
    return _print_sequence_stats(show=False)

def get_daily_stats_df():
    return _print_daily_stats(show=False)

def get_segment_stats_df():
    return _print_segment_stats(show=False)

def get_email_to_status_df():
    return _print_email_to_status(show=False)