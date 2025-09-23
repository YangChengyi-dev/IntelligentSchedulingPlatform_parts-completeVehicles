import os
from flask import send_file
from utils.jsonify import fail_jsonify
from utils.config_utils import BASE_DIR


def downflie(path, filename):
    file = os.path.join(BASE_DIR, path, filename)
    if not os.path.exists(file):
        return fail_jsonify('file not exist')
    # 发送Excel文件给前端
    return send_file(file, as_attachment=True)
