from .inc_stats import *
from .utils import *
from .data import *

def _is_sequence(email_data):
    sequence_name = email_data.get('sequence_name')
    if not sequence_name:
        return False

    return True

def calc_sent(email_data):
    direction = email_data.get("direction")
    if direction != "outgoing":
        return

    if not _is_sequence(email_data):
        return

    inc_sent(email_data)

def calc_bounced(email_data):
    f_email = from_email(email_data)

    direction = email_data.get('direction')
    if direction != 'incoming':
        return

    if not is_postmaster(f_email):
        return


    store_bounced(email_data)

def calc_replies(email_data):
    f_email = from_email(email_data)

    direction = email_data.get('direction')
    if direction != 'incoming':
        return

    is_autoreply = get_autoreply(email_data)
    if is_autoreply:
        return

    if is_postmaster(f_email):
        return

    store_replied(email_data)

def calc_autoreplies(email_data):
    f_email = from_email(email_data)

    direction = email_data.get('direction')
    if direction != 'incoming':
        return

    if is_postmaster(f_email):
        return

    is_autoreply = get_autoreply(email_data)
    if not is_autoreply:
        return

    store_auto_replied(email_data)


def calc_opens(email_data):
    t_email = to_email(email_data)

    if not _is_sequence(email_data):
        return

    opens = email_data.get("opens", None)
    if not opens:
        return

    is_opened = is_opened_by(opens, t_email)
    if not is_opened:
        return

    inc_opened(email_data)


def calc_leads_status(email_data):
    # WE calculate lead status only for outgoing emails from sequence
    # WE need this to attach the LEAD to the sequence and template
    direction = email_data.get("direction")
    if direction != "outgoing":
        return

    if not _is_sequence(email_data):
        return

    inc_lead_status(email_data)



def post_calc(REPLIES=MSG_ID_STATS,
              MESSAGES=MSG_ID_TO_SEQUENCE):

    for reply_to_id, reply_data in REPLIES.items():
        message = _get_message(reply_to_id=reply_to_id,
                               reply_data=reply_data,
                               MESSAGES=MESSAGES)
        if not message:
            continue

        stat = reply_data.get('stat')
        reply_email_data = reply_data.get('email_data')

        if stat == 'bounced':
            inc_bounced(message=message,
                        reply_email_data=reply_email_data)
        elif stat == 'replied':
            inc_replied(message=message,
                        reply_email_data=reply_email_data)
        elif stat == 'auto_replied':
            inc_auto_replied(message=message,
                             reply_email_data=reply_email_data)
        else:
            print(f"Unknown stat for reply_data={reply_data}")


    inc_all_percents()
    inc_total_unique()

def _get_message(reply_to_id,
                 reply_data,
                 MESSAGES=MSG_ID_TO_SEQUENCE):

    #CHECK if reply_to_id correct and already is a reply to sequence
    message = MESSAGES.get(reply_to_id, None)
    if message:
        return message

    email_data = reply_data.get('email_data', None)
    if not email_data:
        return None

    #GET references (the list of MSG_IDS that this message is reply to)
    references = email_data.get('references', [])
    if not references:
        return None

    #THE last reference is always the ID of the reply
    last_reference = references[-1]

    #CHECK if this MSG_ID is a sequence
    message = MESSAGES.get(last_reference, None)
    if message:
        return message

    return None