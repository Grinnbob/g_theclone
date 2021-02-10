import pandas as pd
import numpy as np
import email
import os

EMAILS_PATH_IN = '../data/emails.csv'
EMAILS_PATH_OUT = '../data/emails_modified.csv'
CHUNK_SIZE = 10000
HEADERS = ["Date", "Subject", "To", "From", "X-Folder", 'Body']
SKIPROWS = 0


def insert_value(dictionary, key, value):
    if key in dictionary:
        values = dictionary.get(key)
        values.append(value)
        dictionary[key] = values
    else:
        dictionary[key] = [value]
    return dictionary

def add_headers(df, header_list):
    for label in header_list:
        df_new = pd.DataFrame(headers[label], columns = [label])
        if label not in df.columns:
            df = pd.concat([df, df_new], axis = 1)
    return df

def process_folder(original):
    if not original:
        return ''
    original = original.split("\\")[-1]
    original = original.lower()
    return original

def get_headers(df, header_names):
    headers = {}
    messages = df["message"]
    for message in messages:
        e = email.message_from_string(message)
        for item in header_names:
            header = None
            if item == 'Body':
                message_body = e.get_payload()
                header = message_body.lower()
            else:
                header = e.get(item)
                if item == 'X-Folder':
                    header = process_folder(header)

            insert_value(dictionary = headers, key = item, value = header)

    print("Successfully retrieved header information!")
    return headers


def convert_data(df, headers):
    headers = get_headers(df, headers)
    
    df_new = pd.DataFrame(headers)
    df = pd.concat([df, df_new], axis = 1)

    return df

with open(EMAILS_PATH_IN, 'r') as src:
    print(f"Starting from SKIPROWS={SKIPROWS}")

    count = 0
    try:
        df = pd.read_csv(src, 
                        chunksize=CHUNK_SIZE,
                        skiprows=SKIPROWS,
                        low_memory=True)
        print(f"Successfully read chunk={count}")
        for chunk in df:
            chunk = convert_data(chunk, HEADERS)
            chunk.to_csv(EMAILS_PATH_OUT, mode='a')
            print(f"Successfully write chunk={count}")
            count = count + 1
    except:
        print(f"Has writed chunks={count} of size={CHUNK_SIZE} and SKIPROWS={SKIPROWS}")
        print(f"For the next launch set SKIPROWS to ={SKIPROWS + count*CHUNK_SIZE}")