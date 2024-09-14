import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data

# 加载国家坐标的 CSV 文件
country_coords = pd.read_csv('data/countries.csv')

st.title("SecBee AI Security Analysis")

# 上传用户的数据
uploaded_file = st.file_uploader("上传分析文件：")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # 展示原始数据预览
    with st.expander("数据预览"):
        st.write(data)

    # 自动识别列名
    column_names = data.columns.tolist()

    # 查找与国家相关的列，寻找列名中包含 "country" 或 "国家"
    country_col = None
    for col in column_names:
        if "country" in col.lower() or "国家" in col.lower():
            country_col = col
            break

    # 如果找到了与国家相关的列
    if country_col:
        st.write(f"检测到国家列：{country_col}")

        # 假设记录数列是除国家列以外的另一列
        count_col = [col for col in column_names if col != country_col][0]
        
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

        # 只有在上传数据中包含有效国家时才显示地图
        if not filtered_data.empty:
            ### 显示世界地图 ###
            st.header(f"{country_col} 的威胁记录数世界地图")
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
                tooltip=[alt.Tooltip('name:N', title=country_col), alt.Tooltip(f'{count_col}:Q', title=f'{count_col}')]  # 确保只显示有效数据
            )

            # 将地图和气泡图结合
            final_chart = map_chart + points

            # 在 Streamlit 中首先显示地图
            st.altair_chart(final_chart, use_container_width=True)

        ### 显示柱状图 ###
        st.header(f"{country_col} 的柱状图")
        
        # 动态调整图表高度
        chart_height = max(400, 25 * len(filtered_data))  # 每个国家 25 像素
        
        bar_chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X(f'{count_col}:Q', title=f'{count_col}'),
            y=alt.Y('name:N', sort='-x', title=f'{country_col}')
        ).properties(
            width=700,
            height=chart_height  # 动态高度
        )
        st.altair_chart(bar_chart, use_container_width=True)

    else:
        st.write("未检测到与国家相关的列，只生成柱状图。")

        # 假设记录数列是第一列
        count_col = column_names[0]
        
        # 动态调整图表高度
        chart_height = max(400, 25 * len(data))  # 每个国家 25 像素
        
        # 动态生成柱状图
        bar_chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(f'{count_col}:Q', title=f'{count_col}'),
            y=alt.Y(f'{data.columns[1]}:N', sort='-x', title=f'{data.columns[1]}')
        ).properties(
            width=700,
            height=chart_height  # 动态高度
        )
        st.altair_chart(bar_chart, use_container_width=True)
