import pandas as pd
import numpy as np
from . import config


def load_and_merge(data1_path='data/data1.xlsx', data2_path='data/data2.xlsx'):
    """读取并合并数据源，支持只有其中一个文件"""
    import os
    dfs = []
    for path in [data1_path, data2_path]:
        if path and os.path.exists(path):
            dfs.append(pd.read_excel(path))
    if not dfs:
        raise FileNotFoundError('data1.xlsx 和 data2.xlsx 至少需要上传一个')
    return pd.concat(dfs, ignore_index=True)


def map_category(df):
    """将末级分类名映射到大类，添加'对应品类'列"""
    df['对应品类'] = df['末级分类名'].map(config.CATEGORY_MAPPING).fillna('未知')
    return df


def _process_id11(df):
    """处理规划师id=11的身份和年级"""
    mask = df['规划师id'] == config.PLANNER_ID_11
    for idx, row in df[mask].iterrows():
        app1 = str(row['app一级品类']) if pd.notna(row['app一级品类']) else ''
        app2 = str(row['app二级品类']) if pd.notna(row['app二级品类']) else ''

        identity = config.ID11_IDENTITY_MAP.get(app1)
        if identity == '职场':
            df.at[idx, '身份'] = '职场'
            df.at[idx, '年级'] = '职场'
        elif identity == '大学生':
            df.at[idx, '身份'] = '大学生'
            df.at[idx, '年级'] = config.ID11_GRADE_MAP.get(app2, '')


def _process_id19_22(df):
    """处理规划师id=19,22的身份和年级"""
    mask = df['规划师id'].isin([config.PLANNER_ID_19, config.PLANNER_ID_22])
    for idx, row in df[mask].iterrows():
        app1 = str(row['app一级品类']) if pd.notna(row['app一级品类']) else ''
        app2 = str(row['app二级品类']) if pd.notna(row['app二级品类']) else ''

        mapped = config.ID19_22_MAP.get(app1)
        if mapped:
            df.at[idx, '身份'] = mapped[0]
            df.at[idx, '年级'] = mapped[1]
        elif app1 == '我是学生':
            df.at[idx, '身份'] = '大学生'
            df.at[idx, '年级'] = config.ID19_22_STUDENT_GRADE_MAP.get(app2, '')


def tag_identity_grade(df):
    """添加身份和年级列"""
    df['身份'] = ''
    df['年级'] = ''

    _process_id11(df)
    _process_id19_22(df)

    # 未匹配的行标记为'空'
    empty_mask = df['身份'] == ''
    df.loc[empty_mask, '身份'] = '空'
    df.loc[empty_mask, '年级'] = '空'
    return df


def run(data1_path='data/data1.xlsx', data2_path='data/data2.xlsx'):
    """执行完整的映射流程，返回处理后的 DataFrame"""
    df = load_and_merge(data1_path, data2_path)
    df = map_category(df)
    df = tag_identity_grade(df)

    # 添加月份列（供透视表筛选用）
    df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])
    df['月'] = df[config.DATE_COLUMN].dt.to_period('M').astype(str)

    print(f"mapping 完成: {len(df)} 行, 品类分布:")
    print(df['对应品类'].value_counts().to_string())
    return df
