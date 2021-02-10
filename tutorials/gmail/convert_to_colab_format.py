import pymongo
from .db import sync_db_connect
import re
import pickle
import pandas as pd
import os
import base64
from bs4 import BeautifulSoup
import email

mail_regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

RAW_DATA = 'raw_message'
FILENAME_CSV = "./colab_emails.csv"

ENRICHED = 2

label_column = 'X-Folder'
message_body = 'Message-Body'
message_subject = 'Subject'

data = {
    label_column : {},
    message_body : {},
    message_subject : {},
    'content-type' : {},
    '_id' : {}
}

DATA_KEYS = {
    'label' : True,
    'payload' : True,
    'subject' : True
}

skip = ['_id']

def remove_html(html):
    cleantext = BeautifulSoup(html, "lxml").text

    text = os.linesep.join([s for s in cleantext.splitlines() if s])

    return text


def clean_body(data, content_type):
    decoded = base64.urlsafe_b64decode(data)
    final = decoded.decode('utf-8')

    if 'html' in content_type:
        final = remove_html(final)

    return final


def get_content_type(headers):
    for header in headers:
        name = header.get('name')
        if name == 'Content-Type':
            return header.get('value')

    return 'unknown'

def extract_conent_type(part):
    headers = part.get('headers', None)
    content_type = 'unknown'
    if headers:
        content_type = get_content_type(headers)

    return content_type

def parse_parts(payloads, part):
    parts = part.get('parts', None)
    if not parts:
        data = part['body'].get('data', None)
        if data:
            content_type = extract_conent_type(part)
            payloads.append({'content-type' : content_type, 'data':data})
        else:
            pass
            #print(f"..seems an attachment part={part['body']}")
        return
    else:
        for p in parts:
            parse_parts(payloads, p)

    return

def decode_multipart(msg):
    payloads = []

    part = msg.get('payload')

    body = part.get('body', None)
    content_type = extract_conent_type(part)
    if body:
        data = body.get('data', None)
        if not data:
            parse_parts(payloads, part)
        else:
            payloads.append({'content-type': content_type, 'data':data})

    body = ''
    content_type = ''
    for data in payloads:
        if 'plain' in content_type:
            continue

        content_type =data['content-type']
        body = data['data']

    return clean_body(body, content_type), content_type



def get_enriched(db, limit=10):
    res = db[RAW_DATA].find({'status' : ENRICHED}, DATA_KEYS).limit(limit)
    return res

def get_labeled(db, limit=10):
    res = db[RAW_DATA].find({'label' : {'$ne' : None}}, DATA_KEYS).limit(limit)
    return res



def decode_message(message):
    data = message['payload']['body'].get('data', None)
    if not data:
        return decode_multipart(message)

    headers = message['payload']['headers']
    content_type = get_content_type(headers)

    return clean_body(data, content_type), content_type

def convert(messages):
    counter = 0
    for m in messages:
        for k,v in m.items():
            if k in skip:
                #print(v)
                continue

            if k == 'label':
                data[label_column][counter] = v
            elif k == 'subject':
                data[message_subject][counter] = v
            elif k == 'payload':
                body, content_type = decode_message(m)
                data[message_body][counter] = body
                data['content-type'][counter] = content_type
                data['_id'][counter] = m['_id']

            else:
                print(f"unknown key={k}")

        counter += 1

    print(f"...converted total: {counter}")

def main():
    db = sync_db_connect()

    print("..get_enriched started")
    res = get_labeled(db, limit=20000)

    print("...converting started")
    convert(res)

    data_df = pd.DataFrame(data)

    print("...creating csv")
    data_df.to_csv(FILENAME_CSV)

    print("Success")
if __name__ == '__main__':
    main()