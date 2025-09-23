import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.src.callbacks import ModelCheckpoint
from keras.src.saving import load_model
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, mean_absolute_error

import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']


# 数据预处理函数
def create_dataset(data, time_steps):
    X, Y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])  # 输入
        Y.append(data[i + time_steps])  # 输出
    return np.array(X), np.array(Y)


# 加载数据
data = pd.read_excel('sales_data.xlsx', engine='openpyxl')
dates = pd.to_datetime(data.iloc[:, 0])
sales = data.iloc[:, 3].values
data1 = sales.copy()  # 保留原始数据用于还原和评估

# 确保日期列不为空
if dates.empty:
    raise ValueError("日期数据为空，请检查数据文件。")

# 数据标准化
scaler = StandardScaler()
sales_scaled = scaler.fit_transform(sales.reshape(-1, 1)).flatten()

# 参数设置
time_steps = 2  # 时间步长度
train_size = 40  # 训练集大小
train_data = sales_scaled[:train_size]
test_data = sales_scaled[train_size:]

# 创建训练集和测试集
X_train, Y_train = create_dataset(train_data, time_steps)
X_test, Y_test = create_dataset(test_data, time_steps)

# 转换为 LSTM 需要的输入形状 (样本数, 时间步长, 特征数)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))


def train_model(epochs=300, model_path='sales_lstm_model'):
    # 构建LSTM模型
    model = Sequential([
        LSTM(50, return_sequences=False, input_shape=(time_steps, 1)),
        Dropout(0.2),
        Dense(1)
    ])

    model.compile(optimizer=Adam(learning_rate=0.005), loss='mean_squared_error')

    # 设置模型检查点，以保存验证损失最小的模型
    model_checkpoint = ModelCheckpoint(
        filepath=f'./model/{model_path}.keras',
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        mode='min'
    )

    # 训练模型
    model.fit(X_train, Y_train, epochs=epochs, batch_size=10, validation_data=(X_test, Y_test), verbose=1,
              callbacks=[model_checkpoint])
    #
    # # 保存模型
    # model.save(f'./model/{model_path}.keras')


def predict_model(model_path='sales_lstm_model'):
    # 加载模型
    model = load_model(f'./model/{model_path}.keras')
    # 预测训练集和测试集
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # 还原预测值和目标值到原始尺度
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    Y_train_actual = scaler.inverse_transform(Y_train.reshape(-1, 1))
    Y_test_actual = scaler.inverse_transform(Y_test.reshape(-1, 1))

    # 评估误差
    def calculate_metrics(y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        return rmse, mae, mape

    train_rmse, train_mae, train_mape = calculate_metrics(Y_train_actual, train_predict)
    test_rmse, test_mae, test_mape = calculate_metrics(Y_test_actual, test_predict)

    print(f"训练集 RMSE: {train_rmse}, MAE: {train_mae}, MAPE: {train_mape}%")
    print(f"测试集 RMSE: {test_rmse}, MAE: {test_mae}, MAPE: {test_mape}%")

    # 绘制训练集预测结果
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(dates[time_steps:train_size], train_predict, '-s', color='red', label='LSTM 拟合训练集')
    plt.plot(dates[time_steps:train_size], Y_train_actual, '-o', color='gray', label='实际训练集')
    plt.title('LSTM 训练集预测结果')
    plt.xlabel('时间')
    plt.ylabel('销量')
    plt.legend()

    plt.subplot(2, 1, 2)

    plt.bar(dates[time_steps:train_size],
            (train_predict - Y_train_actual).flatten() / Y_train_actual.flatten(),
            color='orange', label='相对误差', width=20)  # 调整 width 参数

    plt.title('LSTM 训练集相对误差')
    plt.xlabel('时间')
    plt.ylabel('误差')
    plt.legend()

    # 旋转横坐标的日期标签，以便显示更清晰
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # 绘制测试集预测结果
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(dates[train_size + time_steps:], test_predict, '-s', color='blue', label='LSTM 预测验证集')
    plt.plot(dates[train_size + time_steps:], Y_test_actual, '-o', color='black', label='实际验证集')
    plt.title('LSTM 测试集预测结果')
    plt.xlabel('时间')
    plt.ylabel('销量')
    plt.legend()

    plt.subplot(2, 1, 2)
    # 调整条形的宽度，设置较宽的宽度，避免条形太细
    plt.bar(dates[train_size + time_steps:],
            (test_predict - Y_test_actual).flatten() / Y_test_actual.flatten(),
            color='purple', label='相对误差', width=25)  # 调整 width 参数

    plt.title('LSTM 测试集相对误差')
    plt.xlabel('时间')
    plt.ylabel('误差')
    plt.legend()

    # 旋转横坐标的日期标签，以便显示更清晰
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # 预测未来数据
    def predict_future(model, data, time_steps, future_steps):
        future_predictions = []
        input_seq = data[-time_steps:]
        for _ in range(future_steps):
            input_seq_reshaped = input_seq.reshape((1, time_steps, 1))
            next_pred = model.predict(input_seq_reshaped)[0, 0]
            future_predictions.append(next_pred)
            input_seq = np.append(input_seq[1:], next_pred)
        return np.array(future_predictions)

    future_steps = 10  # 预测未来 10 个时间步
    future_predictions = predict_future(model, sales_scaled, time_steps, future_steps)
    future_predictions = scaler.inverse_transform(future_predictions.reshape(-1, 1))

    # 获取未来日期
    # 这里使用 pd.date_range 来确保从最后一个日期开始预测
    if len(dates) > 0:
        future_dates = pd.date_range(dates.iloc[-1], periods=future_steps + 1, freq='MS')[1:]  # 从最后日期开始的未来日期
    else:
        raise ValueError("日期数据为空，无法生成未来日期。")

    # 绘制未来预测结果
    plt.figure(figsize=(10, 6))
    plt.plot(dates, sales, '-s', color='blue', label='训练数据')
    plt.plot(future_dates, future_predictions, '-o', color='green', label='预测数据')
    plt.title('销量预测')
    plt.xlabel('时间')
    plt.ylabel('销量')
    plt.legend()
    plt.show()


# if __name__ == '__main__':
#     # train_model(epochs=300, model_path="sales_lstm1")
#     predict_model("sales_lstm1")
