# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

学习规划师（学规）每日数据分析系统。对教育产品中不同规划师的用户漏斗数据进行清洗、聚合、可视化，支持手动导入底表后自动完成 pipeline 分析，通过 Streamlit 看板展示结果，并推送关键指标到飞书。

## Project Structure

```
Claude-ymx/
├── CLAUDE.md
├── requirements.txt
├── main.py                # Pipeline 入口脚本
├── app.py                 # Streamlit 看板入口
├── data/                  # 原始输入数据（只读）
│   ├── data1.xlsx
│   └── data2.xlsx
├── output/                # 最终输出
│   └── data_年级_日更.xlsx
├── modules/               # 业务逻辑模块
│   ├── __init__.py
│   ├── config.py          # 品类映射字典、规划师ID、筛选条件等常量
│   ├── mapping.py         # 品类映射 + 身份/年级标注
│   ├── pivot_table.py     # 数据透视表生成 + 计算字段
│   ├── daily_metrics.py   # 每日指标计算 + 图表生成
│   ├── significance.py    # A/B实验显著性检验
│   └── notify.py          # 飞书 Webhook 推送
└── pages/                 # Streamlit 多页面
    ├── 01_数据上传.py
    ├── 02_数据透视表.py
    └── 03_每日指标.py
```

## Environment

- Python 3
- 依赖管理: `pip install -r requirements.txt`
- 核心依赖: pandas, numpy, matplotlib, openpyxl, statsmodels, scipy
- 看板: streamlit
- 推送: requests (飞书 Webhook)
- 文件监听: watchdog (可选)

## Commands

```bash
# 运行完整 pipeline
python main.py

# 启动 Streamlit 看板
streamlit run app.py

# 安装依赖
pip install -r requirements.txt
```

## Data Pipeline

`main.py` 按顺序调用各模块，中间产物在内存中传递，最终只输出一个文件：

### 1. modules/mapping.py — 品类映射 + 身份/年级标注

- 输入: `data/data1.xlsx` + `data/data2.xlsx`
- 将"末级分类名"映射到大类（考研、公职、财经、雅思、心理、语言等）
- 按规划师id分别处理身份/年级（id=11按app一级品类判断职场/大学生；id=19,22按一级品类直接映射年级；其他id标记为"空"）

### 2. modules/pivot_table.py — 数据透视表

基于 mapping 处理后的原始数据生成数据透视表，样式参照 `数据透视表参考.xlsx`。

**筛选项（Filter）：**
- 规划师id
- 对应品类
- 月

**值（Values）— 求和项：**
- 学习规划师曝光uv
- 完成学习规划师数
- 课程领取页展示uv
- 学习规划师线索量
- 加好友数
- 首节到课数
- 正价课用户数
- 正价课订单数
- 学习规划师净gmv

**新增计算字段：**

| 字段名 | 公式 | 显示格式 |
|--------|------|----------|
| 完成率 | 完成学习规划师数 / 学习规划师曝光uv | 百分比，保留1位小数 |
| 线索生成率 | 学习规划师线索量 / 学习规划师曝光uv | 百分比，保留1位小数 |
| 加好友率 | 加好友数 / 学习规划师线索量 | 百分比，保留1位小数 |
| 单效 | 学习规划师净gmv / 学习规划师线索量 | 数值，保留1位小数 |
| ARPU | 学习规划师净gmv / 学习规划师曝光uv | 数值，保留1位小数 |

### 3. modules/daily_metrics.py — 每日指标计算 + 图表

- 计算每日曝光UV、线索量、线索生成率，排除规划师id=22
- 分CA品类（排除小学初中、高中）和6个重点品类（考研、考公、财经、雅思、心理、语言）

### 4. modules/significance.py — 显著性检验

- 对control/group组做Z检验（前转率、后转率、好友率、到课率）和GMV的Z检验

**最终输出**: `output/data_年级_日更.xlsx`，包含以下sheet：
- 原始数据（mapping处理后的完整数据）
- 数据透视表（含筛选项和计算字段）
- 每日指标(排除规划师22)
- 图表(排除规划师22)

## Streamlit 看板

- `app.py` 为入口，使用 Streamlit 多页面模式
- `pages/01_数据上传.py`: 上传 data1.xlsx + data2.xlsx，触发 pipeline 运行
- `pages/02_数据透视表.py`: 交互式筛选（规划师id、品类、月份），展示透视表和计算字段
- `pages/03_每日指标.py`: 展示每日趋势图表（曝光UV、线索量、线索生成率）

## 飞书推送

- `modules/notify.py` 通过飞书群机器人 Webhook 推送每日关键指标摘要
- Webhook URL 配置在 `modules/config.py` 中

## Key Metrics

漏斗指标链路: 曝光UV → 第一题完成 → 完成规划师 → 课程领取页展示 → 线索量 → 加好友 → 到课 → 正价课转化

效率指标: 首屏跳出率、运营配置完成率、规划师完成率、领课页曝光率、领课页转化率、线索生成率、加微率、线索转正率、单效、ARPU

## Conventions

- `data/` 目录为只读，脚本不修改原始输入文件
- `output/` 目录存放最终输出，中间产物不落盘
- 所有可配置常量（映射字典、规划师ID、筛选条件）集中在 `modules/config.py`
- 中文列名和变量名是正常的，保持一致即可
- matplotlib 中文显示需设置字体: `plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']`
