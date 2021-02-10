import pandas as pd
import numpy as np
import email
import os

EMAILS_DATA_PATH = '../data/emails_modified.csv'
HEADERS = ["X-Folder", 'Body']
LABELS = ['']
CHUNK_SIZE = 10000

def read_labels(filepath, headers=HEADERS):
    if len(headers) != 2:
        raise Exception(f"need to pass headers in format = ['label', 'data']")
    
    labels_count = {}
    with open(filepath, 'r') as src:
        df = pd.read_csv(src, 
                        chunksize=CHUNK_SIZE,
                        low_memory=True)

        for chunk in df:
            chunk.to_csv(EMAILS_PATH_OUT, mode='a')
            print(f"Successfully write chunk={count}")
            count = count + 1


def read_dataset(filepath, headers=HEADERS):
    texts = []
    labels = []
    
    if len(headers) != 2:
        raise Exception(f"need to pass headers in format = ['label', 'data']")

    with open(filepath, 'r') as src:
        df = pd.read_csv(src, low_memory=True, names=headers, header=0)
        
        labels = df[headers[0]]
        texts = df[headers[1]]

    return texts, labels

texts, labels = read_dataset(EMAILS_DATA_PATH)