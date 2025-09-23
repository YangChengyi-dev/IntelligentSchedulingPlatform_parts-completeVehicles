import json

from zhipuai import ZhipuAI

from utils.jsonify import success_jsonify, fail_jsonify
from utils.downfalie import downflie
from flask import Blueprint, request
# # from flask_login import login_required, current_user
# from database.base_model import t
from database.schemas import PartSchema, PartOptimizeSchema
from utils.log_utils import Logging
from database.models import Part, PartOptimize

#
part_view = Blueprint("part_view", __name__)
log = Logging().get_logger()
part_field_list = [Part.id, Part.supplier_name, Part.supplier_addr, Part.prov, Part.city, Part.dest,
                   Part.distance, Part.quantity]

part_optimize = [PartOptimize.id, PartOptimize.prov, PartOptimize.city, PartOptimize.cc, PartOptimize.cd,
                 PartOptimize.fs, PartOptimize.qd, PartOptimize.tj, PartOptimize.dl, PartOptimize.cost]


@part_view.route("/part/index", methods=["GET"], endpoint="init")
def init():
    result = Part.query(part_field_list)
    part_schema = PartSchema()
    json_data = part_schema.dump(result, many=True)  # 转换后的 JSON 数据
    # job_num = Part.query(func.count(Part.id))[0][0]  # 用来统计所有的岗位数据
    log.info("part init successfully")
    return success_jsonify("part init successfully", json_data)


@part_view.route('/part/search', methods=["POST"], endpoint='explore')
def explore():
    # 从前端获取对应的查询条件
    upload_data = json.loads(request.get_data().decode('utf-8'))
    prov = upload_data.get("prov")
    city = upload_data.get('city')
    dest = upload_data.get("dest")
    print(prov)
    # 通过if进行判断，如果查询条件为None就不添加该查询条件
    condition_filter = []
    if prov != "":  # 判断prov是否为None，如果不是就添加该查找条件
        condition_filter.append(Part.prov == prov)
    if city != "":
        condition_filter.append(Part.city.like(f'%{city}%'))
    if dest != "":
        condition_filter.append(Part.dest == dest)
    part_query_result = Part.query(part_field_list, filter=condition_filter)
    part_schema = PartSchema()
    json_data = part_schema.dump(part_query_result, many=True)
    log.info("part search successfully")
    return success_jsonify("part search successfully", json_data)


@part_view.route('/part/optimize', methods=["POST"], endpoint='optimize')
def optimize():
    # 从前端获取对应的查询条件
    upload_data = json.loads(request.get_data().decode('utf-8'))
    programme = upload_data.get("programme")
    method = upload_data.get("method")
    # 通过if进行判断，如果查询条件为None就不添加该查询条件
    query_result = PartOptimize.query(part_optimize,
                                      filter=[PartOptimize.programme == programme, PartOptimize.method == method])
    part_optimize_schema = PartOptimizeSchema()
    json_data = part_optimize_schema.dump(query_result, many=True)
    log.info("part optimize successfully")
    return success_jsonify("optimize successfully", json_data)


# 返回ai图片
@part_view.route('/part/ai_chat', methods=['POST'])
def ai_chat():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    chat = upload_data.get("chat")
    client = ZhipuAI(api_key="88bf5b26454170a3013311f953c3234f.vOS7sO7IFfEwJuwF")  # 填写您自己的APIKey
    # if "图" in chat:
    #     # 如果包含 "图" 字符，返回不调用模型的自定义响应
    #     response = client.images.generations(
    #         model="cogview-3",  # 填写需要调用的模型名称
    #         prompt=chat,
    #     )
    #     answer = response.data[0].url
    #     return success_jsonify("optimize successfully", answer)
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": chat}
        ],
    )
    answer = response.choices[0].message.content
    return success_jsonify("optimize successfully", answer)


# 返回ai图片
@part_view.route('/part/ai_photo', methods=['POST'])
def ai_photo():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    chat = upload_data.get("chat")
    client = ZhipuAI(api_key="88bf5b26454170a3013311f953c3234f.vOS7sO7IFfEwJuwF")  # 填写您自己的APIKey
    response = client.images.generations(
        model="cogview-3",  # 填写需要调用的模型名称
        prompt=chat,
    )
    answer = response.data[0].url
    return success_jsonify("optimize successfully", answer)


@part_view.route('/part/download', methods=['POST'])
def download_excel():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    programme = upload_data.get("programme")
    method = upload_data.get("method")
    # 生成Excel文件的路径
    filename = f"{programme}+{method}优化结果.xlsx" if programme != "综合优化概览" else "各方案优化结果统计表.xlsx"
    return downflie('data/part', filename)
