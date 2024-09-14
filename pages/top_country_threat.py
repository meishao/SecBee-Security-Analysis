import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data

# 检查用户是否已登录
if not st.session_state.get("logged_in"):
    st.warning("请先登录以访问此页面。")
    # 重定向到登录页面
    st.experimental_set_query_params()
    st.experimental_rerun()
else:
    # 您的页面内容
    st.title("全球威胁趋势")
    # 其他代码...

    # 加载国家坐标的 CSV 文件
    country_coords = pd.read_csv('./data/countries.csv')
    
    st.title("SecBee AI Security Analysis")
    
    # 上传用户的数据（包含国家和记录数的列）
    uploaded_file = st.file_uploader("上传分析文件：")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    
        # 展示原始数据预览
        with st.expander("数据预览"):
            st.write(data)
    
        # 自动识别列名
        column_names = data.columns.tolist()
        country_col = column_names[0]  # 假设第一列是国家名称
        count_col = column_names[1]  # 假设第二列是记录数
    
        # 清理记录数列，去除逗号并转换为整数
        data[count_col] = data[count_col].str.replace(',', '').astype(int)
    
        # 将用户数据与国家坐标数据合并
        merged_data = pd.merge(data, country_coords, left_on=country_col, right_on='name', how='inner')
    
        # 根据记录数列降序排列数据
        merged_data = merged_data.sort_values(by=count_col, ascending=False)
    
        # 确保数据框中不含布尔值和 NaN
        merged_data = merged_data.dropna(subset=['name', count_col])  # 删除有空值的行
        merged_data = merged_data[~merged_data['name'].apply(lambda x: isinstance(x, bool))]  # 过滤掉布尔类型的值
    
        # 选择要显示的国家
        selected_countries = st.multiselect(
            "选择要包含的国家：",
            options=merged_data['name'].unique(),
            default=merged_data['name'].unique()
        )
    
        # 根据选定的国家过滤数据
        filtered_data = merged_data[merged_data['name'].isin(selected_countries)]
    
        ### 显示世界地图 ###
        st.header("国家威胁记录数的世界地图")
        # 加载 Altair 的世界地图数据
        countries = alt.topo_feature(vega_data.world_110m.url, 'countries')
    
        # 创建不带工具提示的地图图层
        map_chart = alt.Chart(countries).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).properties(
            width=1000,
            height=600
        ).project('equirectangular')  # 使用等矩形投影显示整个世界
    
        # 创建气泡图，直接应用工具提示
        points = alt.Chart(filtered_data).mark_circle().encode(
            longitude='longitude:Q',
            latitude='latitude:Q',
            size=alt.Size(f'{count_col}:Q', title='记录数', scale=alt.Scale(range=[10, 1000])),
            color=alt.Color(f'{count_col}:Q', scale=alt.Scale(scheme='reds'), title='记录数'),
            tooltip=[alt.Tooltip('name:N', title='国家'), alt.Tooltip(f'{count_col}:Q', title='记录数')]  # 确保只显示有效数据
        )
    
        # 将地图和气泡图结合
        final_chart = map_chart + points
    
        # 在 Streamlit 中首先显示地图
        st.altair_chart(final_chart, use_container_width=True)
    
        ### 显示柱状图 ###
        st.header("国家威胁记录数的柱状图")
        
        # 动态调整图表高度
        chart_height = max(400, 25 * len(filtered_data))  # 每个国家 25 像素
        
        bar_chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X(f'{count_col}:Q', title='记录数'),
            y=alt.Y('name:N', sort='-x', title='国家')
        ).properties(
            width=700,
            height=chart_height  # 动态高度
        )
        st.altair_chart(bar_chart, use_container_width=True)
