"""数据上传页面"""
import streamlit as st
import os
import time
from modules.theme import render_header

st.set_page_config(page_title='数据上传', page_icon='📤', layout='wide')
render_header('数据上传', '上传底表并运行 Pipeline', '📤')

# 上传区
st.markdown('<div class="panel"><div class="panel-title">📁 上传数据文件</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader('data1.xlsx', type=['xlsx'], key='data1', label_visibility='collapsed')
    st.caption('data1.xlsx')
with col2:
    file2 = st.file_uploader('data2.xlsx', type=['xlsx'], key='data2', label_visibility='collapsed')
    st.caption('data2.xlsx')
st.markdown('</div>', unsafe_allow_html=True)

# 当前文件状态
st.markdown('<div class="panel"><div class="panel-title">📋 当前数据文件</div>', unsafe_allow_html=True)
for fname in ['data1.xlsx', 'data2.xlsx']:
    fpath = os.path.join('data', fname)
    if os.path.exists(fpath):
        import datetime
        mtime = os.path.getmtime(fpath)
        t = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        size_kb = os.path.getsize(fpath) / 1024
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f'<p style="font-size:13px; color:#10B981; margin:4px 0;">● {fname} — {size_kb:.0f} KB — {t}</p>', unsafe_allow_html=True)
        with c2:
            if st.button('删除', key=f'del_{fname}', type='secondary'):
                os.remove(fpath)
                # 同时清理 output
                output_path = 'output/data_年级_日更.xlsx'
                if os.path.exists(output_path):
                    os.remove(output_path)
                st.rerun()
    else:
        st.markdown(f'<p style="font-size:13px; color:#7A8BA4; margin:4px 0;">○ {fname} — 未上传（可选）</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 运行按钮
has_any_data = (os.path.exists('data/data1.xlsx') or file1 is not None
                or os.path.exists('data/data2.xlsx') or file2 is not None)
if st.button('运行 Pipeline', type='primary', disabled=not has_any_data):
    if file1:
        with open('data/data1.xlsx', 'wb') as f:
            f.write(file1.getvalue())
    if file2:
        with open('data/data2.xlsx', 'wb') as f:
            f.write(file2.getvalue())

    if not os.path.exists('data/data1.xlsx') and not os.path.exists('data/data2.xlsx'):
        st.error('请至少上传 data1.xlsx 或 data2.xlsx 中的一个')
    else:
        with st.spinner('正在运行 pipeline...'):
            try:
                from modules.pipeline import run
                start = time.time()
                run()
                elapsed = time.time() - start
                st.cache_data.clear()
                st.success(f'Pipeline 运行完成！耗时 {elapsed:.1f} 秒')
            except Exception as e:
                st.error(f'运行出错: {e}')
                import traceback
                st.code(traceback.format_exc())
