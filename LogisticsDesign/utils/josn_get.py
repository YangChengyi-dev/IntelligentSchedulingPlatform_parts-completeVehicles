import json
from flask import request


def josn_get():
    data = []
    upload_data = json.loads(request.get_data().decode('utf-8'))
    for key in upload_data:
        data.append(upload_data.get(key))
    return data
