import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from FinMind.data import DataLoader

api = DataLoader()
# 金鑰 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0xMC0yNiAxNToxNjoyOSIsInVzZXJfaWQiOiIxOTk5MTEiLCJpcCI6IjIyMC4xMzMuMTQ0LjIxMyJ9.bJTqCeF_lXe3LdU0Vj7th9ZBTC1itqJeiFaij-hs_1o
# user_id:199911 # password:19990101

st.write("查詢信息輸入")
token_p = st.text_input("輸入金鑰")
user_id_p = st.text_input("輸入用戶名")
password_p = st.text_input("輸入密碼")

genre = st.radio("是否選擇公司編號", ["尋找公司😎", "不需要了，我知道公司編號🚀"])
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
        # 可視化
        #
        # fig_line = px.line(data_company, x='date', y=['open', 'close', 'max', 'min'], title='股价走势图')
        # st.plotly_chart(fig_line)
    else:
        st.warning("請輸入查詢所需信息")

if genre == "不需要了，我知道公司編號🚀":
    if token_p and user_id_p and password_p is not None:
        api.login_by_token(api_token=token_p)
        api.login(user_id=user_id_p, password=password_p)
        stock_id_p = st.text_input
        df = api.taiwan_stock_daily(
            stock_id='2330',
            start_date='2020-04-02',
            end_date='2020-04-12'
        )
    else:
        st.warning("請輸入查詢所需信息")
