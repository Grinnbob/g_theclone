from dateutil import parser
from .data import *

def to_day(text_date):
    f = parser.parse(text_date)

    return f.strftime("%Y-%m-%d")

def from_email(email_data):
    envelope = email_data.get("envelope")

    from_email = envelope.get("from")[0].get("email")

    return from_email

def to_email(email_data):
    envelope = email_data.get("envelope")

    to_email = envelope.get("to")[0].get("email")

    return to_email

def get_autoreply(email_data):
    envelope = email_data.get("envelope")

    is_autoreply = envelope.get("is_autoreply")

    return is_autoreply

def is_opened_by(opens, to_email):
    if not opens or not to_email:
        return False

    for open in opens:
        opened_by = open.get("opened_by")
        if to_email not in opened_by:
            continue

        user_agent = open.get("user_agent")
        if user_agent is None:
            return True

        if 'Windows NT' in user_agent and \
            'Chrome' in user_agent and \
            'Safari' in user_agent and \
            'Edge' in user_agent and \
            'Mozilla' in user_agent:
            continue
        else:
            return True

    return False


def is_postmaster(email):
    if 'mailer-daemon' in email:
        return True

    if 'googlemail' in email:
        return True

    if 'postmaster' in email:
        return True

    return False

def update_dates(email_data,
                 data=FROM_TO_DATE):
    date_created = email_data.get('date_created')

    dc = parser.parse(date_created)

    if not data['earliest']:
        data['earliest'] = dc

    if not data['latest']:
        data['latest'] = dc

    if data['earliest'] > dc:
        data['earliest'] = dc

    if data['latest'] < dc:
        data['latest'] = dc

def calc_percents(data):
    bounced = data.get('bounced', 0)
    sent = data.get('sent', 0)

    data['delivered'] = sent - bounced
    if data['delivered'] < 0:
        data['delivered'] = 0

    delivered = data.get('delivered', 0)
    replied = data.get('replied', 0)
    opened = data.get('opened', 0)
    meetings = data.get('meeting booked', 0)

    data['bounce rate'] = 0
    data['open rate'] = 0
    data['reply rate'] = 0
    data['appointment rate'] = 0

    if sent:
        data['bounce rate'] = round((bounced / sent) * 100, 2)

    if delivered:
        data['open rate'] = round((opened / delivered) * 100, 2)
        data['reply rate'] = round((replied / delivered) * 100, 2)
        data['appointment rate'] = round((meetings / delivered) * 100, 2)
