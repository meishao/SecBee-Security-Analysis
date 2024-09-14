'''
import streamlit as st
import pandas as pd

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    with st.expander("Data preview"):
        st.write(dataframe)

if st.button("Start"):
    st.write("Analyzing...")
    #st.write(dataframe)
'''

import streamlit as st
import plotly.express as px
import pandas as pd

# 设置页面布局为宽屏
st.set_page_config(layout="wide")

# 侧边栏菜单
st.sidebar.title("NetEyez")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/NetEyez_logo.svg/1200px-NetEyez_logo.svg.png", width=150)
st.sidebar.header("Menu")
menu_options = ["ダッシュボード", "アクションインサイトAI", "脅威の重要度", "ネットワーク", "アプリケーション", "設定"]
selected_option = st.sidebar.radio("Select Option", menu_options)

# 主体部分布局
st.title("NetEyez - ダッシュボード")

# 模拟时间线的图表
st.subheader("監視 - フィルターなし")
time_data = pd.DataFrame({
    'time': pd.date_range('2024-09-11 12:00', periods=100, freq='H'),
    'count': abs(pd.Series(range(100)) + pd.Series([x * 2 for x in range(100)]))
})
fig = px.line(time_data, x='time', y='count', title='Event Timeline')
st.plotly_chart(fig, use_container_width=True)

# 使用列布局模拟图表分布
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("アセット")
    asset_data = pd.DataFrame({
        'Category': ['クリティカル', 'メジャー', 'マイナー'],
        'Count': [2150, 1250, 720]
    })
    fig = px.pie(asset_data, values='Count', names='Category', title='アセット分布')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("脅威")
    threat_data = pd.DataFrame({
        'Category': ['クリティカル', 'メジャー', 'マイナー'],
        'Count': [33720, 25200, 18000]
    })
    fig = px.pie(threat_data, values='Count', names='Category', title='脅威分布')
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("アセットと脅威の関係")
    funnel_data = pd.DataFrame({
        'Step': ['Critical', 'Major', 'Minor'],
        'Value': [2150, 1250, 720]
    })
    fig = px.funnel(funnel_data, x='Step', y='Value')
    st.plotly_chart(fig, use_container_width=True)

# 显示 AI 评分的表格
st.subheader("AIアセット")
ai_data = pd.DataFrame({
    '重大度': ['クリティカル', 'クリティカル', 'メジャー', 'メジャー', 'マイナー'],
    'アセット': ['60.252.70.152', '60.252.70.151', '60.252.198', '10.104.201.199', '10.104.201.203'],
    '脅威': ['ウェブクローラ', 'ホストスキャン', 'DDoS攻撃準備', '黒書ファイル', 'ボットネットプロキシ'],
    'AIスコア': [82, 81, 71, 68, 68]
})
st.table(ai_data)

# 使用列布局模拟图表分布
col4, col5 = st.columns(2)

with col4:
    st.subheader("トップ脅威イベント分布")
    threat_event_data = pd.DataFrame({
        'Event': ['OSINT脅威サイト', 'リモートアクセス', 'ブルートフォースアタック', 'ボットネットプロキシ', '黒書ファイル'],
        'Count': [500, 450, 400, 300, 200]
    })
    fig = px.bar(threat_event_data, x='Event', y='Count', title='トップ脅威イベント分布')
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.subheader("イベントネットワーク")
    network_data = pd.DataFrame({
        'Node': ['60.252.70.152', '10.104.201.199', 'OSINT脅威サイト', 'リモートアクセス'],
        'Connections': [10, 12, 7, 9]
    })
    fig = px.scatter(network_data, x='Node', y='Connections', title='ネットワーク分析', size='Connections')
    st.plotly_chart(fig, use_container_width=True)

# 显示未处理事件的经过时间
st.subheader("未処理イベントの経過時間")
time_data = pd.DataFrame({
    'Period': ['>15日間', '7-15日間', '3-7日間', '<3日間'],
    'Count': [20000, 10000, 5000, 3000]
})
fig = px.bar(time_data, x='Period', y='Count', title='未処理イベントの経過時間')
st.plotly_chart(fig, use_container_width=True)

