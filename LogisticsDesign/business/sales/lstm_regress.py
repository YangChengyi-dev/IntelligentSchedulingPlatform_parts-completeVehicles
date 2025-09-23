import os.path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.src.saving import load_model
from business.sales.base_regress import get_date_list, month_factor

from utils.config_utils import BASE_DIR


class LSTMRegressionPredict:
    def __init__(self, model_path="sales_lstm1"):
        model_path = os.path.join(BASE_DIR, 'business', 'sales', 'model', model_path)
        self.model = load_model(f'{model_path}.keras')  # 加载模型
        file_path = os.path.join(BASE_DIR, 'business', 'sales', 'sales_data.xlsx')
        df = pd.read_excel(file_path, engine='openpyxl')  # 加载数据
        sales = df.iloc[:, 4].values  # 获取销售额列
        self.scaler = StandardScaler()  # 数据标准化
        self.sales = self.scaler.fit_transform(sales.reshape(-1, 1)).flatten()
        self.future_steps = 0  # 预测未来几个时间步

    def predict(self, start_time: str, end_time: str):
        """
        :param start_time: 预测的开始时间
        :param end_time: 预测的结束时间
        :return: 预测结果包含时间，时间编号，预测结果
        """
        time_steps = 2  # 时间步长
        predictions, start_id, end_id = self.predict_core(start_time, end_time, time_steps)
        data_list = get_date_list(start_time, end_time)
        time_list = np.array([i for i in range(int(start_id), int(end_id) + 1)])

        data = []
        final_regress = []
        for i in range(len(data_list)):
            final_regress.append(month_factor[int(data_list[i].split('/')[1]) - 1] * predictions[i])
        # 将预测数据四舍五入转换为整数
        for i in range(len(predictions)):
            predictions[i] = round(predictions[i])
            final_regress[i] = round(final_regress[i])

        for i in range(len(data_list)):
            data.append({
                "时间": data_list[i],
                "时间编号": int(time_list[i]),
                "预测结果": predictions[i],
                "最终结果": final_regress[i]
            })
        res_dict = {"time": data_list, "result": final_regress}
        return data, res_dict

    # 预测未来数据
    def predict_future(self, time_steps, input_seq):
        """
        :param time_steps: 表示时间步长
        :param input_seq: 表示初始的第一个数据
        :return:
        """
        future_predictions = []
        for _ in range(self.future_steps):
            input_seq_reshaped = input_seq.reshape((1, time_steps, 1))
            next_predict = self.model.predict(input_seq_reshaped)[0, 0]
            future_predictions.append(next_predict)
            input_seq = np.append(input_seq[1:], next_predict)
        return np.array(future_predictions)

    def predict_core(self, start: str, end: str, time_steps):
        """
        # 这边是进行预测的实现，名字想不到更好的，暂时就用这个吧
        :param start: 预测的开始时间
        :param end: 预测的结束时间
        :param time_steps: 表示时间步长
        :return:
        """
        # 处理日期
        input_seq = None
        is_future = False  # 这边是用来区分start是否完全超过2024/10,超过的话要进行对应的处理
        start_date = start.split("/")  # 获取开始时间的相关信息
        start_year = int(start_date[0])
        start_month = int(start_date[1])
        end_date = end.split("/")  # 获取结束时间的相关信息
        end_year = int(end_date[0])
        end_month = int(end_date[1])
        start_time_id = 1 + (start_year - 2020) * 12 + start_month - 3
        end_time_id = 1 + (end_year - 2020) * 12 + end_month - 3
        # 此处是判断输入的起始时间是否在训练数据范围内
        # if start_month < 5 and start_year == 2020: # 考虑到应该不会有人预测2020/5之前的数据，所以注释掉，如果预测的话要进行处理
        #     input_seq = self.sales[:time_steps]
        if start_month <= 10 and start_year <= 2024:
            input_seq = self.sales[start_time_id - time_steps:start_time_id]
        elif start_month > 10 and start_year >= 2024:
            input_seq = self.sales[-time_steps:]
            is_future = True
        self.future_steps = end_time_id - start_time_id + 1
        if is_future:
            extra_step = start_time_id - len(self.sales) - 1
            self.future_steps += extra_step
            predictions = self.predict_future(time_steps, input_seq)
            predictions = predictions[extra_step:]
        else:
            predictions = self.predict_future(time_steps, input_seq)
        predictions = self.scaler.inverse_transform(predictions.reshape(-1, 1))
        predictions = predictions.flatten()
        return predictions, start_time_id, end_time_id


# if __name__ == '__main__':
#     # 测试
#     lstm = LSTMRegressionPredict()
#     lstm.predict("2024/4", "2024/10")
