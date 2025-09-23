import json
from flask import Blueprint, request
from utils.jsonify import success_jsonify, fail_jsonify
from database.models import user
from database.schemas import RegressPredictSchema
from utils.log_utils import Logging
from sqlalchemy import desc

log = Logging().get_logger()
login_view = Blueprint("login_view", __name__)


@login_view.route('/user/login', methods=['POST'], endpoint='login')
def login():
    upload_data = json.loads(request.get_data().decode('utf-8'))
    username = upload_data.get("username")
    password_hash_list = user.query([user.password], filter=[user.username == username])
    if not password_hash_list:
        return success_jsonify("Regress Predict successfully", {
            "isSuccess": False
        })
    password = upload_data.get("password")
    identity = upload_data.get("identity")
    if password == password_hash_list[0][0]:
        return success_jsonify("Regress Predict successfully", {
            "isSuccess": True
        })
    else:
        return success_jsonify("Regress Predict successfully", {
            "isSuccess": False
        })

# @login_view.route('/user/t1', methods=['GET'], endpoint='t1')
# def init():


# @login_view.route('/user/register', methods=['POST'], endpoint='register')
# def register():
#     return True
    # upload_data = json.loads(request.get_data().decode('utf-8'))
    # username = upload_data.get("username")
    # password_hash_list = user.query([user.password], filter=[user.username == username])
    # if not password_hash_list:
    #     return success_jsonify("Regress Predict successfully", {
    #         "isSuccess": False
    #     })
    # password = upload_data.get("password")
    # if password == password_hash_list[0][0]:
    #     return success_jsonify("Regress Predict successfully", {
    #         "isSuccess": True
    #     })
    # else:
    #     return success_jsonify("Regress Predict successfully", {
    #         "isSuccess": False
    #     })
