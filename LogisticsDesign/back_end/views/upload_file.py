import json
import os

from utils.log_utils import Logging
from flask import Blueprint, request, jsonify, send_file
from database.base_model import t

log = Logging().get_logger()


def update_upload():
    f = request.files['file']
    upload_path = os.path.join('data/part', f.filename)
    f.save(upload_path)


def insert_upload():
    f = request.files['file']
    upload_path = os.path.join('data/part', f.filename)
    f.save(upload_path)