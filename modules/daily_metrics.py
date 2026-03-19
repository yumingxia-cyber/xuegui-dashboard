import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
import tempfile
import os
from . import config


def compute_daily(df):
    """计算每日指标（排除规划师id=22）"""
    filtered = df[df['规划师id'] != config.PLANNER_ID_22].copy()
    filtered[config.DATE_COLUMN] = pd.to_datetime(filtered[config.DATE_COLUMN])

    dates = sorted(filtered[config.DATE_COLUMN].unique())
    rows = []

    for date in dates:
        day_data = filtered[filtered[config.DATE_COLUMN] == date]
        row = {'日期': date}

        # CA品类（排除小学初中、高中）
        ca_data = day_data[~day_data['对应品类'].isin(config.EXCLUDE_CATEGORIES)]
        ca_uv = ca_data['学习规划师曝光uv'].sum()
        ca_leads = ca_data['学习规划师线索量'].sum()
        row['CA品类_曝光uv'] = ca_uv
        row['CA品类_线索量'] = ca_leads
        row['CA品类_线索生成率'] = (ca_leads / ca_uv * 100) if ca_uv > 0 else 0

        # 各重点品类
        focus_uv_total = 0
        focus_leads_total = 0
        for cat in config.FOCUS_CATEGORIES:
            cat_data = day_data[day_data['对应品类'] == cat]
            uv = cat_data['学习规划师曝光uv'].sum()
            leads = cat_data['学习规划师线索量'].sum()
            row[f'{cat}_曝光uv'] = uv
            row[f'{cat}_线索量'] = leads
            row[f'{cat}_线索生成率'] = (leads / uv * 100) if uv > 0 else 0
            focus_uv_total += uv
            focus_leads_total += leads

        # 重点品类合计
        row['重点品类合计_曝光uv'] = focus_uv_total
        row['重点品类合计_线索量'] = focus_leads_total
        row['重点品类合计_线索生成率'] = (focus_leads_total / focus_uv_total * 100) if focus_uv_total > 0 else 0

        rows.append(row)

    return pd.DataFrame(rows)


def _create_chart(result_df, metric_suffix, y_label, title):
    """创建折线图，返回临时文件路径"""
    plt.rcParams['font.sans-serif'] = config.FONT_CONFIG
    plt.rcParams['axes.unicode_minus'] = False

    dates = [d.strftime('%m-%d') for d in result_df['日期']]
    colors = ['red', 'green', 'orange', 'purple', 'brown', 'pink']

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(dates, result_df[f'CA品类_{metric_suffix}'], marker='o', label=f'CA品类', linewidth=2.5, markersize=8, color='blue')

    for j, cat in enumerate(config.FOCUS_CATEGORIES):
        ax.plot(dates, result_df[f'{cat}_{metric_suffix}'], marker='s', label=cat,
                linewidth=2, markersize=6, color=colors[j], linestyle='--')

    ax.plot(dates, result_df[f'重点品类合计_{metric_suffix}'], marker='*', label='重点品类合计',
            linewidth=2.5, markersize=10, color='black')

    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(f'{title} [已排除规划师22]', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(tmp.name, dpi=100, bbox_inches='tight')
    plt.close()
    return tmp.name


def write_sheets(writer, df):
    """写入每日指标 sheet 和图表 sheet"""
    result_df = compute_daily(df)
    result_df.to_excel(writer, sheet_name='每日指标(排除规划师22)', index=False)

    # 生成图表
    charts = [
        ('曝光uv', '曝光UV', '分日曝光UV趋势图'),
        ('线索量', '线索量', '分日线索量趋势图'),
        ('线索生成率', '线索生成率(%)', '分日线索生成率趋势图'),
    ]

    workbook = writer.book
    chart_sheet = workbook.create_sheet(title='图表(排除规划师22)')

    chart_sheet['E1'] = '图表说明:'
    chart_sheet['E2'] = "CA品类: 排除['小学初中', '高中']后的所有品类"
    chart_sheet['E3'] = '重点品类: 考研、考公、财经、雅思、心理、语言'
    chart_sheet['E4'] = '数据说明: 图表数据已排除规划师id为22，原始数据sheet包含所有数据'

    # 使用项目内的临时目录，避免文件在 openpyxl 保存前被清理
    chart_dir = os.path.join('output', '.charts')
    os.makedirs(chart_dir, exist_ok=True)

    tmp_files = []
    positions = ['A1', 'A28', 'A55']

    for i, ((suffix, ylabel, title), pos) in enumerate(zip(charts, positions)):
        tmp_path = _create_chart(result_df, suffix, ylabel, title)
        stable_path = os.path.join(chart_dir, f'chart_{i}.png')
        os.replace(tmp_path, stable_path)
        tmp_files.append(stable_path)
        img = Image(stable_path)
        img.width = 1000
        img.height = 500
        chart_sheet.add_image(img, pos)

    # 记录待清理文件，由 pipeline 在保存后清理
    writer._chart_tmp_files = tmp_files

    print(f"daily_metrics 完成: {len(result_df)} 天的指标已计算")


def run(df, writer):
    """执行每日指标模块"""
    write_sheets(writer, df)
