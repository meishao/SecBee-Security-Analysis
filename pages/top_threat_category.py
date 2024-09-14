import streamlit as st
import pandas as pd
import altair as alt

st.title("SecBee AI Security Analysis")

# 上传分析文件
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # 展示原始数据
    with st.expander("Data preview"):
        st.write(data)

    # 自动识别列名
    column_names = data.columns.tolist()
    category_col = column_names[0]  # 假设第一列是分类列
    count_col = column_names[1]  # 假设第二列是记录数列

    # 清理记录数列，去除逗号并转换为整数
    data[count_col] = data[count_col].str.replace(',', '').astype(int)

    # 按照记录数列降序排列数据
    data = data.sort_values(by=count_col, ascending=False)

    # 创建左右列布局
    col1, col2 = st.columns([1, 3])  # 左侧为1，右侧为3的比例

    # 左侧列：选择过滤器
    with col1:
        with st.container():
            selected_categories = st.multiselect(
                "Select categories to include:",
                options=data[category_col].unique(),
                default=data[category_col].unique()
            )

    # 根据选中的类别过滤数据
    filtered_data = data[data[category_col].isin(selected_categories)]

    # 右侧列：创建水平柱状图
    with col2:
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X(f'{count_col}:Q', title='Count of Records'),
            y=alt.Y(f'{category_col}:N', sort='-x', 
                    title='Threat Category', 
                    axis=alt.Axis(
                        titleAnchor="start",  # 将Y轴标题移动到最左侧
                        titleAngle=0,  # 标题水平显示
                        labelLimit=600,  # 限制标签长度
                    ))
        ).properties(
            title=alt.TitleParams(
                text="Top Threat Categories by Count",  # 图表标题
                offset=20,  # 调整标题偏移量
                fontSize=16  # 设置标题字体大小
            ),
            padding={"left": 100, "top": 30}  # 添加左侧和顶部的填充空间
        )

        # 在 Streamlit 中显示图表
        st.altair_chart(chart, use_container_width=True)
