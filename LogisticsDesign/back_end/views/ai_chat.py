from zhipuai import ZhipuAI


def _init():  # 初始化
    global _global_client
    _global_client = {}


def set():
    global _global_client  # 声明_global_client为全局变量
    _global_client = ZhipuAI(api_key="88bf5b26454170a3013311f953c3234f.vOS7sO7IFfEwJuwF")


def get_value():
    # 获得全局变量，不存在则返回默认值
    return _global_client
