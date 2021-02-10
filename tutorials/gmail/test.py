import pandas as pd

emails = {
    'from' : {},
    'to' : {},
    'cc' : {},
    'bcc' : {},
    'subject': {}
}

test = [
    {
    'from' : 'ks.shilov@gmail.com',
    'internalDate' : '3424234',
    'id' : 'adfasdfasdf000000',
    'to' : 'kaka@mail.com',
    },
    {
        'from': ['kaka@mail.com'],
        'internalDate': '342423433',
        'id': 'adfasdfasdf980890980',
        'to': ['ks.shilov@gmail.com', 'ivan@gmail.com'],
        'cc' : ['cuper@gmail.com']
    },
    {
        'from': ['ks.shilov@gmail.com'],
        'internalDate': '34242341',
        'id': 'adfasdfasdf56767',
        'to': ['kaka@mail.com', 'crypto@gmail.com']
    },
    {
        'from': ['super@mail.com'],
        'internalDate': '342423444',
        'id': 'adfasdfasdf34343',
        'to': ['ks.shilov@gmail.com', 'kol1@gmail.com']
    },
]

tt = ['ks.shilov@gmail.com', 'ks.shilov@gmail.com', 'ks.shilov@gmail.com', 'kaka@mail.com']

n = dict(map(lambda i: (i[0], True),emails.items()))
print(n)