import os
import shutil
import pandas as pd
from . import config
from . import mapping
from . import pivot_table
from . import daily_metrics


def run(data1_path='data/data1.xlsx', data2_path='data/data2.xlsx',
        output_path='output/data_年级_日更.xlsx'):
    """执行完整 pipeline"""
    # 1. 品类映射 + 身份/年级标注
    df = mapping.run(data1_path, data2_path)

    # 2. 写入 Excel（多 sheet）
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # 原始数据 sheet
        df.to_excel(writer, sheet_name='原始数据', index=False)
        print(f"原始数据已写入: {len(df)} 行")

        # 数据透视表 sheet
        pivot_table.run(df, writer)

        # 每日指标 + 图表 sheet
        daily_metrics.run(df, writer)

    # 清理图表临时文件
    chart_dir = os.path.join('output', '.charts')
    if os.path.exists(chart_dir):
        shutil.rmtree(chart_dir)

    print(f"\npipeline 完成！输出文件: {output_path}")
