"""学规数据分析看板"""
import streamlit as st
import os
from modules.theme import render_header, render_kpis

os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

st.set_page_config(page_title='学规数据分析', page_icon='📊', layout='wide')
render_header('学规数据分析系统', '每日数据监控平台')

# 功能入口卡片
st.markdown('''
<div class="kpi-row">
    <div class="kpi-card blue">
        <div class="kpi-icon">📤</div>
        <div class="kpi-label">数据上传</div>
        <div class="kpi-value" style="font-size:13px; font-weight:500;">上传底表，一键运行 Pipeline</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-icon">📋</div>
        <div class="kpi-label">数据透视表</div>
        <div class="kpi-value" style="font-size:13px; font-weight:500;">多维筛选，查看汇总与效率指标</div>
    </div>
    <div class="kpi-card purple">
        <div class="kpi-icon">📈</div>
        <div class="kpi-label">每日指标</div>
        <div class="kpi-value" style="font-size:13px; font-weight:500;">趋势图表，监控核心数据变化</div>
    </div>
</div>
''', unsafe_allow_html=True)

# 数据状态
output_file = 'output/data_年级_日更.xlsx'
if os.path.exists(output_file):
    import datetime
    mtime = os.path.getmtime(output_file)
    update_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f'''
    <div class="panel">
        <div class="panel-title">📡 数据状态</div>
        <p style="color:#10B981; font-size:13px; margin:0;">● 数据已就绪 &nbsp; 最近更新: {update_time}</p>
    </div>''', unsafe_allow_html=True)
else:
    st.markdown('''
    <div class="panel">
        <div class="panel-title">📡 数据状态</div>
        <p style="color:#F59E0B; font-size:13px; margin:0;">● 尚无数据，请先到「数据上传」页面上传底表</p>
    </div>''', unsafe_allow_html=True)

st.markdown('''
<div class="panel">
    <div class="panel-title">📖 使用指南</div>
    <p style="font-size:13px; color:#6B7A8D; line-height:2; margin:0;">
        1. 在左侧菜单选择 <b>数据上传</b>，上传 data1.xlsx 和 data2.xlsx<br>
        2. 点击运行 Pipeline，等待处理完成<br>
        3. 切换到 <b>数据透视表</b> 或 <b>每日指标</b> 查看分析结果
    </p>
</div>''', unsafe_allow_html=True)
