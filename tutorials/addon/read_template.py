from pymongo import MongoClient
import base64

db_obj_sync = {
    'client' : None,
    'database' : ''
}

def sync_db_connect():
    db_obj_sync['client'] = MongoClient()
    db_obj_sync['database'] = db_obj_sync['client']['TC-dev']

    return db_obj_sync['database']


def main():
    db = sync_db_connect()

    template = db['template']

    res = template.find_one({'template_id' : "r-818747056620100651"})
    msg = res['data']['template']

    message_bytes = base64.b64decode(msg)
    message = message_bytes.decode('ascii')

    print(message)


if __name__ == '__main__':
    main()