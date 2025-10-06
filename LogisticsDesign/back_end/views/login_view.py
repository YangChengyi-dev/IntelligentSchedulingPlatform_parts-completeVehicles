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
    try:
        # 记录请求信息
        print("收到登录请求")
        print(f"请求头: {request.headers}")
        
        # 获取请求数据
        upload_data = json.loads(request.get_data().decode('utf-8'))
        username = upload_data.get("username")
        password = upload_data.get("password")
        print(f"登录尝试 - 用户名: {username}, 密码: {'*' * len(password) if password else None}")
        
        # 验证参数
        if not all([username, password]):
            print("参数验证失败：用户名或密码为空")
            return {
                "code": 400,
                "message": "用户名和密码不能为空",
                "data": {"isSuccess": False}
            }
        
        # 添加硬编码的admin用户验证（用于开发环境或数据库未就绪时）
        if username == 'admin' and password == '123456':
            print("开发模式: 管理员登录成功")
            # 返回符合前端期望格式的响应，包含isSuccess字段
            return {
                "code": 200,
                "message": "登录成功",
                "data": {
                    "isSuccess": True,
                    "user": {
                        "userId": "1",
                        "loginName": "admin",
                        "userName": "管理员"
                    }
                }
            }
        
        # 尝试从数据库验证（正常模式）
        try:
            password_hash_list = user.query([user.password], filter=[user.username == username])
            print(f"数据库查询结果: {password_hash_list}")
            if not password_hash_list:
                print("用户不存在")
                return {
                    "code": 401,
                    "message": "登录失败",
                    "data": {"isSuccess": False}
                }
            
            if password == password_hash_list[0][0]:
                print("密码验证成功")
                return {
                    "code": 200,
                    "message": "登录成功",
                    "data": {
                        "isSuccess": True,
                        "user": {
                            "userId": "1",
                            "loginName": username,
                            "userName": "管理员"
                        }
                    }
                }
            else:
                print("密码错误")
                return {
                    "code": 401,
                    "message": "登录失败",
                    "data": {"isSuccess": False}
                }
        except Exception as e:
            print(f"数据库验证失败: {str(e)}")
            # 数据库连接失败时，返回硬编码验证结果
            if username == 'admin' and password == '123456':
                print("数据库错误时的管理员登录成功")
                return {
                    "code": 200,
                    "message": "登录成功",
                    "data": {
                        "isSuccess": True,
                        "user": {
                            "userId": "1",
                            "loginName": "admin",
                            "userName": "管理员"
                        }
                    }
                }
            else:
                return {
                    "code": 500,
                    "message": "数据库查询异常",
                    "data": {"isSuccess": False}
                }
    except Exception as e:
        print(f"登录处理异常: {str(e)}")
        # 返回明确的错误信息，包含isSuccess字段
        return {
            "code": 500,
            "message": f"登录处理异常: {str(e)}",
            "data": {"isSuccess": False}
        }

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
