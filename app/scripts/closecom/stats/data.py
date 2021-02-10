SHOW_COLUMNS = [
    'sent',
    'bounced',
    'delivered',
    'opened',
    'replied',
    'auto_replied',
    'interested',
    'meeting booked',
    'bounce rate',
    'open rate',
    'reply rate',
    'appointment rate',
]

SHOW_TOTAL_COLUMNS = [
    'unique leads',
    'sent',
    'bounced',
    'delivered',
    'opened',
    'replied',
    'auto_replied',
    'interested',
    'meeting booked',
    'bounce rate',
    'open rate',
    'reply rate',
    'appointment rate',
]


EMAILS_TO_STATUS_COLUMNS = [
    'status'
]

UNIQUE_LEADS = set()

LEAD_DATA = {}

EMAILS_REPLIED = []
EMAILS_BOUNCED = []
EMAILS_AUTO_REPLIED = []
LEADS_STATUS_CALC = []

EMAILS_TO_STATUS = {}

STATS_TOTAL = {}
STATS_DAILY = {}
STATS_SEQUENCE = {}
STATS_SEGMENT = {}

FROM_TO_DATE = {
    'earliest' : '',
    'latest' : ''
}

MSG_ID_STATS = {
#    'in_reply_to' : {
#        'thread_id' : 'thread_id',
#        'stat' : 'sent'
#        'email_data' : ''
#    }
}

#STORE all IDS of sequence emails
MSG_ID_TO_SEQUENCE = {
#    'reply_to_id' : {
#        'seq-name' : 'tmpl-name',
#    }
}

