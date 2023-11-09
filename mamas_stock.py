import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from FinMind.data import DataLoader
import numpy as np
# 匯入決策樹分類器
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import graphviz
import pandas as pd

api = DataLoader()
# 金鑰 # user_id:199911 # password:19990101

st.write("查詢信息輸入")
token_p = st.text_input("輸入金鑰")
user_id_p = st.text_input("輸入用戶名")
password_p = st.text_input("輸入密碼")

genre = st.radio("是否選擇公司編號", ["尋找公司😎", "不需要了，我知道公司名稱🚀"])
if genre == "尋找公司😎":
    if token_p and user_id_p and password_p is not None:
        api.login_by_token(api_token=token_p)
        api.login(user_id=user_id_p, password=password_p)

        df = api.taiwan_stock_info()
        df_cate = df['industry_category'].unique()
        cate = st.selectbox("產業名稱", df_cate)
        cate_data = df[df['industry_category'] == cate]
        st.write(cate_data)
        df_company = cate_data['stock_name'].unique()
        company = st.selectbox("公司名稱", df_company)
        company_data = cate_data[cate_data['stock_name'] == company]
        # 得到公司編號
        company_id = company_data['stock_id']
        # 篩選時間
        selected_date_start = st.date_input("選擇起始日期", key="start")
        selected_date_end = st.date_input("選擇結束日期", key="end")
        # 根據篩選時間得到股票數據
        data_company = api.taiwan_stock_daily(
            stock_id=company_id,
            start_date=selected_date_start,
            end_date=selected_date_end
        )
        st.write(data_company)

        fig = go.Figure(data=[go.Candlestick(x=data_company['date'],
                                             open=data_company['open'],
                                             high=data_company['max'],
                                             low=data_company['min'],
                                             close=data_company['close'],
                                             increasing_line_color = 'red',
                                             decreasing_line_color = 'green')])

        fig.update_layout(
            title=f'{company}-{selected_date_start}-{selected_date_end}股票价格走势',
            xaxis_title='日期',
            yaxis_title='股价',
        )

        st.plotly_chart(fig)

        # 決策樹
        data_company['week_trend'] = np.where(data_company.close.shift(-5) > data_company.close, 1, 0)

        data_company['date'] = pd.to_datetime(data_company['date'])

        # 預處理時間序列
        data_company['date'] = (data_company['date'] - data_company['date'].min()).dt.days
        # 處理stock_id

        # 切割訓練集和測試集，切割比例為 70%:30%
        split_point = int(len(data_company) * 0.7)
        # 切割成學習樣本以及測試樣本
        train = data_company.iloc[:split_point, :].copy()
        test = data_company.iloc[split_point:-5, :].copy()
        st.write('训练数据总')
        st.write(train)
        # 訓練樣本再分成目標序列 y 以及因子矩陣 X
        train_X = train.drop('week_trend', axis=1)
        train_y = train.week_trend
        # 測試樣本再分成目標序列 y 以及因子矩陣 X
        test_X = test.drop('week_trend', axis=1)
        test_y = test.week_trend
        st.write("训练数据x")
        st.write(train_X)
        # 叫出一棵決策樹
        model = DecisionTreeClassifier(max_depth=7)
        # 學習
        model.fit(train_X, train_y)
        # 測驗，prediction, 根據測試集做出的預測
        prediction = model.predict(test_X)

        # 決策樹可視化
        dot_data = export_graphviz(model, out_file=None,
                                   feature_names=train_X.columns,
                                   filled=True, rounded=True,
                                   class_names=True,
                                   special_characters=True)
        graph = graphviz.Source(dot_data)
        st.graphviz_chart(dot_data)
        graph.render('output', format='png')
        st.image('output.png')
    else:
        st.warning("請輸入查詢所需信息")

if genre == "不需要了，我知道公司編號🚀":
    if token_p and user_id_p and password_p is not None:
        api.login_by_token(api_token=token_p)
        api.login(user_id=user_id_p, password=password_p)

        df = api.taiwan_stock_info()
        df_cate = df['stock_name'].unique()
        cate = st.selectbox("產業名稱", df_cate)
        company_data = df[df['stock_name'] == cate]
        st.write(company_data)

        # 得到公司編號
        company_id = company_data['stock_id']
        # 篩選時間
        selected_date_start = st.date_input("選擇起始日期", key="start")
        selected_date_end = st.date_input("選擇結束日期", key="end")
        # 根據篩選時間得到股票數據
        data_company = api.taiwan_stock_daily(
            stock_id=company_id,
            start_date=selected_date_start,
            end_date=selected_date_end
        )
        st.write(data_company)

        fig = go.Figure(data=[go.Candlestick(x=data_company['date'],
                                             open=data_company['open'],
                                             high=data_company['max'],
                                             low=data_company['min'],
                                             close=data_company['close'],
                                             increasing_line_color='red',
                                             decreasing_line_color='green')])

        fig.update_layout(
            title=f'{company}-{selected_date_start}-{selected_date_end}股票价格走势',
            xaxis_title='日期',
            yaxis_title='股价',
        )

        st.plotly_chart(fig)
    else:
        st.warning("請輸入查詢所需信息")
