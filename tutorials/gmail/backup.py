import pymongo
from db import sync_db_connect
import re
import pickle
import pandas as pd
import os

mail_regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

RAW_DATA = 'raw_message'
READY = 1
ENRICHED = 2
FAILED = -1
EXTRACTED = 3
FILENAME = "./emails.pkl"

DATA_KEYS = {
    'from' : True,
    'to' : True,
    'cc' : True,
    'bcc' : True,
    'reply-to' : True
}

emails = dict()

def get_enriched(db, limit):
    res = db[RAW_DATA].find({'status' : ENRICHED}, DATA_KEYS).limit(limit)
    return res

def categorize(messages):
    for m in messages:
        for k,v in m.items():
            if k in DATA_KEYS.keys():
                if not emails.get(k):
                    emails[k] = set()
                if isinstance(v, list):
                    emails[k].update(v)
                else:
                    emails[k].add(v)

#def to_dataframe(dct):
#    emails_df = pd.DataFrame(dict([(k, pd.Series(list(v))) for k, v in dct.items()]))
#    return emails_df

def main():
    db = sync_db_connect()


    print("..get_enriched started")
    res = get_enriched(db, limit=10)

    print("...categorize started")
    categorize(res)

    from_count = len(emails.get('from', []))
    to_count = len(emails.get('to', []))
    copy_count = len(emails.get('cc', [])) + len(emails.get('bcc', []))
    replyto_count = len(emails.get('reply-to', []))
    print(f"found: from:{from_count}, to:{to_count}, copy:{copy_count} reply-to:{replyto_count}")


    print("...saving data")
    fd = open(FILENAME, 'wb')
    pickle.dump(emails, fd)

    print("Success")
if __name__ == '__main__':
    main()