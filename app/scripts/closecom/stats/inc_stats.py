from .total_stats import *
from .daily_stats import *
from .sequence_stats import *
from .segment_stats import *
from pprint import pprint
from .data import *

def inc_all_percents():
    calc_total_percents()
    calc_daily_percents()
    calc_sequence_percents()
    calc_segment_percents()

def inc_total_unique(DATA=STATS_TOTAL):
    DATA['unique leads'] = len(list(UNIQUE_LEADS))

def _unique_leads_sent(email_data):
    t_email = to_email(email_data)
    if t_email:
        UNIQUE_LEADS.add(t_email)

def _inc_all(stat,
             email_data,
             sequence_name,
             template_name,
             segment_name,
             calc_daily=True):

    inc_total(stat)

    #WE use it to tirn off cal stats daily for lead_stastus
    if calc_daily:
        inc_daily(stat, email_data)

    inc_sequence(stat,
                 sequence_name=sequence_name,
                 template_name=template_name)

    inc_segment(stat,
                segment_name=segment_name,
                sequence_name=sequence_name,
                template_name=template_name)


def inc_sent(email_data):
    _store_id_to_sequence(email_data)
    _unique_leads_sent(email_data)

    sequence_name = email_data.get("sequence_name")
    template_name = email_data.get("template_name", "Not a template")

    lead_id = email_data.get("lead_id")
    segment_name = LEAD_DATA[lead_id].get("custom").get("lead_segment", "Unknown segment")

    _inc_all('sent',
             email_data,
             sequence_name=sequence_name,
             template_name=template_name,
             segment_name=segment_name)


def inc_opened(email_data):
    sequence_name = email_data.get("sequence_name")
    template_name = email_data.get("template_name", "Not a template")

    lead_id = email_data.get("lead_id")
    segment_name = LEAD_DATA[lead_id].get("custom").get("lead_segment", "Unknown segment")

    _inc_all('opened',
             email_data,
             sequence_name=sequence_name,
             template_name=template_name,
             segment_name=segment_name)

def inc_lead_status(email_data):
    lead_id = email_data.get("lead_id")
    t_email = to_email(email_data)
    if lead_id in LEADS_STATUS_CALC:
        return

    try:
        lead = LEAD_DATA[lead_id]
        status = lead['status_label'].lower()
        lead_date_updated = lead.get('date_updated', None)

        if lead_date_updated is None:
            print(f"ERROR: unknown lead_date_updated for lead_id={lead_id}")

    except Exception as e:
        print(f"ERROR: status not found for lead_id={lead_id} error={str(e)}")
        return

    _inc_daily_lead_status(status,
                          lead_date_updated)

    sequence_name = email_data.get("sequence_name")
    template_name = email_data.get("template_name", "Not a template")

    lead_id = email_data.get("lead_id")
    segment_name = LEAD_DATA[lead_id].get("custom").get("lead_segment", "Unknown segment")

    _inc_all(status,
             email_data,
             sequence_name=sequence_name,
             template_name=template_name,
             segment_name=segment_name,
             calc_daily=False)

    LEADS_STATUS_CALC.append(lead_id)
    EMAILS_TO_STATUS[t_email] = status

def inc_bounced(message,
                reply_email_data):

#    f_email = from_email(reply_email_data)
#    if f_email in EMAILS_BOUNCED:
#        return

    sequence_name = list(message.keys())[0]
    template_name = message[sequence_name]

    lead_id = reply_email_data.get("lead_id")
    segment_name = LEAD_DATA[lead_id].get("custom").get("lead_segment", "Unknown segment")

    _inc_all("bounced",
             reply_email_data,
             sequence_name=sequence_name,
             template_name=template_name,
             segment_name=segment_name)

#   EMAILS_BOUNCED.append(f_email)


def inc_replied(message,
                reply_email_data):
    f_email = from_email(reply_email_data)
    if f_email in EMAILS_REPLIED:
        return

    sequence_name = list(message.keys())[0]
    template_name = message[sequence_name]

    lead_id = reply_email_data.get("lead_id")
    segment_name = LEAD_DATA[lead_id].get("custom").get("lead_segment", "Unknown segment")

    _inc_all("replied",
             reply_email_data,
             sequence_name=sequence_name,
             template_name=template_name,
             segment_name=segment_name)

    EMAILS_REPLIED.append(f_email)
    if not EMAILS_TO_STATUS.get(f_email):
        EMAILS_TO_STATUS[f_email] = 'replied'

def inc_auto_replied(message,
                     reply_email_data):
    f_email = from_email(reply_email_data)
    if f_email in EMAILS_AUTO_REPLIED:
        return

    sequence_name = list(message.keys())[0]
    template_name = message[sequence_name]

    lead_id = reply_email_data.get("lead_id")
    segment_name = LEAD_DATA[lead_id].get("custom").get("lead_segment", "Unknown segment")

    _inc_all("auto_replied",
             reply_email_data,
             sequence_name=sequence_name,
             template_name=template_name,
             segment_name=segment_name)

    EMAILS_AUTO_REPLIED.append(f_email)




def store_bounced(email_data):
    _calc_msgid_stats(email_data,
                      'bounced')


def store_replied(email_data):
    _calc_msgid_stats(email_data,
                      'replied')

def store_auto_replied(email_data):
    _calc_msgid_stats(email_data,
                      'auto_replied')


def _inc_daily_lead_status(status,
                          lead_date_updated):
    if not lead_date_updated:
        return

    day = to_day(lead_date_updated)

    inc_daily_lead_status(status,
                          day)

def _calc_msgid_stats(email_data,
                      stat,
                      DATA=MSG_ID_STATS):
    envelope = email_data.get("envelope")
    in_reply_to = envelope.get("in_reply_to")

    DATA[in_reply_to] = {
        'stat' : stat,
        'email_data' : email_data
    }


def _store_id_to_sequence(email_data):
    sequence_name = email_data.get("sequence_name", None)
    if not sequence_name:
        return

    template_name = email_data.get("template_name", "Not a template")

    envelope = email_data.get("envelope", None)
    if not envelope:
        return

    message_id = envelope.get("message_id")
    MSG_ID_TO_SEQUENCE[message_id] = {
        sequence_name : template_name
    }


