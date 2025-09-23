from flask import jsonify


def success_jsonify(str, json_data=None):
    if json_data is None:
        return jsonify({
            "code": 200,
            "message": str,
        })
    else:
        return jsonify({
            "code": 200,
            "message": str,
            "data": json_data
        })


def fail_jsonify(str):
    return jsonify({
        'code': 500,
        'message': str
    })
