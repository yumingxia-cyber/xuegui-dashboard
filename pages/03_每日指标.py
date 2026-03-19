"""每日指标页面"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from modules import config
from modules.theme import render_header

st.set_page_config(page_title='每日指标', page_icon='📈', layout='wide')
render_header('每日指标', '已排除规划师id=22', '📈')

OUTPUT_FILE = 'output/data_年级_日更.xlsx'
if not os.path.exists(OUTPUT_FILE):
    st.warning('尚无数据，请先到「数据上传」页面运行 pipeline')
    st.stop()

@st.cache_data
def load_metrics(file_mtime):
    return pd.read_excel(OUTPUT_FILE, sheet_name='每日指标(排除规划师22)')

metrics_df = load_metrics(os.path.getmtime(OUTPUT_FILE))
metrics_df['日期'] = pd.to_datetime(metrics_df['日期'])

# === 控制区 ===
col1, col2, col3 = st.columns([1, 3, 2])
with col1:
    metric_type = st.selectbox('选择指标', ['曝光uv', '线索量', '线索生成率'])
with col2:
    all_series = ['CA品类'] + config.FOCUS_CATEGORIES + ['重点品类合计']
    selected_series = st.multiselect('选择品类', all_series, default=['CA品类', '重点品类合计'])
with col3:
    date_min = metrics_df['日期'].min().date()
    date_max = metrics_df['日期'].max().date()
    date_range = st.date_input('日期范围', value=(date_min, date_max),
                                min_value=date_min, max_value=date_max)

if not selected_series:
    st.info('请至少选择一个品类')
    st.stop()

# 应用日期筛选
d_start, d_end = (date_range if len(date_range) == 2 else (date_min, date_max))
metrics_df = metrics_df[(metrics_df['日期'].dt.date >= d_start) & (metrics_df['日期'].dt.date <= d_end)]

# === 图表 ===
chart_colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#14B8A6', '#6366F1', '#EC4899']

fig = go.Figure()
for i, series in enumerate(selected_series):
    col_name = f'{series}_{metric_type}'
    if col_name in metrics_df.columns:
        fig.add_trace(go.Scatter(
            x=metrics_df['日期'], y=metrics_df[col_name],
            name=series, mode='lines+markers',
            line=dict(width=2.5, color=chart_colors[i % len(chart_colors)]),
            marker=dict(size=5),
        ))

y_title = '线索生成率 (%)' if metric_type == '线索生成率' else metric_type

fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(family='Inter, sans-serif', size=12, color='#1E3456'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0, font=dict(size=11)),
    margin=dict(l=40, r=20, t=20, b=40),
    xaxis=dict(gridcolor='#F0ECF5', tickformat='%m-%d'),
    yaxis=dict(gridcolor='#F0ECF5', title=y_title),
    hovermode='x unified',
    height=400,
)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# === 数据表格 ===
with st.expander('查看原始数据'):
    display_cols = ['日期'] + [f'{s}_{metric_type}' for s in selected_series if f'{s}_{metric_type}' in metrics_df.columns]
    display_df = metrics_df[display_cols].copy()
    display_df['日期'] = display_df['日期'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df, use_container_width=True, hide_index=True)
