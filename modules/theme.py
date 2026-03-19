"""分析看板 UI 主题"""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ===== 全局 ===== */
.stApp {
    background-color: #EEEAF4;
    font-family: 'Inter', sans-serif;
}

/* ===== 隐藏默认元素 ===== */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

/* ===== 深蓝侧边栏 ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3456 0%, #2B4A78 100%);
}
section[data-testid="stSidebar"] * {
    color: #C8D6E5 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stDateInput label {
    color: #FFFFFF !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
section[data-testid="stSidebar"] .stMarkdown p {
    font-size: 11px;
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"],
section[data-testid="stSidebar"] div[data-baseweb="input"] {
    background-color: rgba(255,255,255,0.08);
    border-radius: 6px;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* ===== 页面标题栏 ===== */
.page-header {
    background: linear-gradient(135deg, #1E3456 0%, #34608D 100%);
    padding: 20px 28px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.page-header h1 {
    color: #FFFFFF !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
.page-header .subtitle {
    color: #8FB8DE;
    font-size: 13px;
}

/* ===== KPI 卡片 ===== */
.kpi-row { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.kpi-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 16px 18px;
    flex: 1;
    min-width: 150px;
    box-shadow: 0 2px 8px rgba(30,52,86,0.06);
    transition: transform 0.15s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(30,52,86,0.1); }
.kpi-card .kpi-label {
    font-size: 11px;
    color: #7A8BA4;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
}
.kpi-card .kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #1E3456;
}
.kpi-card .kpi-icon {
    font-size: 16px;
    margin-bottom: 4px;
}

/* 卡片顶部彩色指示条 */
.kpi-card.blue    { border-top: 3px solid #3B82F6; }
.kpi-card.green   { border-top: 3px solid #10B981; }
.kpi-card.orange  { border-top: 3px solid #F59E0B; }
.kpi-card.purple  { border-top: 3px solid #8B5CF6; }
.kpi-card.red     { border-top: 3px solid #EF4444; }
.kpi-card.teal    { border-top: 3px solid #14B8A6; }
.kpi-card.indigo  { border-top: 3px solid #6366F1; }

/* ===== 白色面板 ===== */
.panel {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 22px 24px;
    box-shadow: 0 2px 8px rgba(30,52,86,0.06);
    margin-bottom: 16px;
}
.panel-title {
    font-size: 14px;
    font-weight: 600;
    color: #1E3456;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ===== st.metric 覆写 ===== */
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 2px 8px rgba(30,52,86,0.06);
    border-top: 3px solid #3B82F6;
}
div[data-testid="stMetricValue"] {
    font-size: 20px !important;
    color: #1E3456 !important;
    font-weight: 700 !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: #7A8BA4 !important;
}

/* ===== 全局标题 ===== */
h1 { font-size: 20px !important; color: #1E3456 !important; font-weight: 600 !important; }
h2 { font-size: 16px !important; color: #1E3456 !important; font-weight: 600 !important; }
h3 { font-size: 14px !important; color: #1E3456 !important; font-weight: 600 !important; }

/* ===== 表格 ===== */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(30,52,86,0.06);
}

/* ===== 按钮 ===== */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 24px;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
}

/* ===== 文件上传 ===== */
section[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(30,52,86,0.06);
}

/* ===== 分割线 ===== */
hr { border-color: #E0DCE8 !important; }

/* ===== Expander ===== */
.streamlit-expanderHeader {
    background: #FFFFFF;
    border-radius: 8px;
}

/* ===== Multiselect 选中标签 ===== */
span[data-baseweb="tag"] {
    background-color: #E8EDF4 !important;
    color: #1E3456 !important;
    border: 1px solid #B0C4DE !important;
    border-radius: 4px !important;
    font-size: 12px !important;
}
span[data-baseweb="tag"] span {
    color: #1E3456 !important;
}
span[data-baseweb="tag"] svg {
    fill: #4A6B8A !important;
}
/* 侧边栏中的标签 */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #FFFFFF !important;
    color: #1E3456 !important;
    border: 1px solid #B0C4DE !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
    color: #1E3456 !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
    fill: #1E3456 !important;
}
</style>
"""


def render_header(title, subtitle='', icon='📊'):
    """渲染页面顶部标题栏"""
    import streamlit as st
    st.markdown(THEME_CSS, unsafe_allow_html=True)
    sub = f'<div class="subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f'''
    <div class="page-header">
        <span style="font-size:24px">{icon}</span>
        <div><h1>{title}</h1>{sub}</div>
    </div>''', unsafe_allow_html=True)


def render_kpis(items, cols_per_row=5):
    """渲染 KPI 卡片
    items: list of (label, value) or (label, value, color_class) or (label, value, color_class, icon)
    color_class: 'blue','green','orange','purple','red','teal','indigo'
    """
    import streamlit as st
    rows = [items[i:i+cols_per_row] for i in range(0, len(items), cols_per_row)]
    for row in rows:
        html = '<div class="kpi-row">'
        for item in row:
            label = item[0]
            value = item[1]
            color = item[2] if len(item) > 2 else 'blue'
            icon = item[3] if len(item) > 3 else ''
            icon_html = f'<div class="kpi-icon">{icon}</div>' if icon else ''
            html += f'''
            <div class="kpi-card {color}">
                {icon_html}
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>'''
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
