from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

BASE_DIR = Path(__file__).resolve().parent
Project_DIR = BASE_DIR.parent


# 1. 读取原始 CSV
CSV_FILE=Project_DIR/'data'/'raw'/'defects_data.csv'
df = pd.read_csv(CSV_FILE)

DB_FILE = Project_DIR / "database_2" / "quality_v2.db"
# 2. 连接新的 SQLite 数据库
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Q1: 不同缺陷类型的数量、总维修成本、平均维修成本
# sql_q1='''
# select
#     dt.defect_type_name,
#     COUNT(*) AS defect_count,
#     SUM(m.repair_cost) AS total_cost,
#     AVG(m.repair_cost) AS avg_cost
# from main_defects as m
# join defect_types as dt
#     on m.defect_type_id = dt.defect_type_id
# group by dt.defect_type_name
# order by total_cost desc;
# '''
#
# result_q1=pd.read_sql(sql_q1,conn)
# print(result_q1)

# Q2：不同 defect_location 的缺陷数量和维修成本
# sql_q2='''
# select
#     lo.location_id,
#     lo.location_name,
#     COUNT(*) AS locations_count,
#     SUM(m.repair_cost) AS total_cost,
#     AVG(m.repair_cost) AS avg_cost
# from main_defects as m
# join locations as lo
#     on m.location_id = lo.location_id
# group by lo.location_id
# order by avg_cost desc;
# '''
# result_q2=pd.read_sql(sql_q2,conn).round(2)
# print(result_q2)

# Q3：不同 inspection_method 的缺陷数量和维修成本
# sql_q3='''
# select
#     im.method_id,
#     im.method_name,
#     COUNT(*) AS inspect_mothod_count,
#     SUM(m.repair_cost) AS total_cost,
#     avg(m.repair_cost) AS avg_cost
# from main_defects as m
# join inspection_methods as  im
#      on m.method_id=im.method_id
# group by im.method_id
# order by avg_cost desc
# '''
# result_q3= pd.read_sql_query(sql_q3,conn).round(2)
# print(result_q3)


# 不同 severity 的数量和平均维修成本
# sql_q4='''
# select
#     severity,
#     count(*) as severity_count,
#     sum(repair_cost)as total_repair_cost,
#     avg(repair_cost) as avg_repair_cost
# from main_defects
# group by severity
# '''
# result_q4=pd.read_sql_query(sql_q4,conn).round(2)
# print(result_q4)

# 缺陷最多的 Top 10 产品
# sql_q5='''
# select
#     product_id,
#     count(product_id) as id_number
# from main_defects
# group by product_id
# order by id_number desc
# limit 10;
# '''
# result_q5=pd.read_sql(sql_q5,conn)
# print(result_q5)

# 维修成本最高的 Top 10 产品
# sql_q6='''
# select
#     product_id,
#     sum(repair_cost) as repair_cost
# from main_defects
# group by product_id
# order by repair_cost desc
#
# '''
# result_q6=pd.read_sql(sql_q6,conn)
# result_q6["cum_cost"] = result_q6["repair_cost"].cumsum()
# result_q6["cum_pct"] = result_q6["cum_cost"] / result_q6["repair_cost"].sum() * 100
# print(result_q6.head(10))
# # 3. 只取 Top 10 用来画图（累计占比仍然是基于全体数据算出来的，准确）
# top10 = result_q6.head(10).copy()
# # 4. 画帕累托图
# fig, ax1 = plt.subplots(figsize=(10, 6))
# bars = ax1.bar(top10["product_id"].astype(str), top10["repair_cost"], color='steelblue')
# ax1.bar_label(bars, padding=3, fmt='%.0f')
# ax1.set_xlabel("Product ID")
# ax1.set_ylabel("Repair Cost", color='steelblue')
# ax1.tick_params(axis='x', rotation=45)
# ax2 = ax1.twinx()
# ax2.plot(top10["product_id"].astype(str), top10["cum_pct"],
#           color='red', marker='o', linewidth=2)
# ax2.set_ylabel("Cumulative %", color='red')
# ax2.set_ylim(0, 110)
#
# ax2.axhline(80, color='gray', linestyle='--', linewidth=1)
# ax2.text(len(top10) - 1, 82, '80%', color='gray', ha='right')
#
# plt.title("Pareto Analysis: Top 10 Products by Repair Cost")
# plt.tight_layout()
# plt.show()
#
# # 5. 关键少数产品（贡献前80%总成本的产品，基于全体数据）
# vital_few = result_q6[result_q6["cum_pct"].shift(fill_value=0) < 80]
# print(f"\n关键少数产品数量：{len(vital_few)} / 共 {len(result_q6)} 个产品")
# print(vital_few[["product_id", "repair_cost", "cum_pct"]])

# defect_type + location 组合分析
# sql_q7='''
# SELECT
#     dt.defect_type_name,
#     lo.location_name,
#     COUNT(*) AS defect_count,
#     SUM(m.repair_cost) AS total_cost,
#     AVG(m.repair_cost) AS avg_cost
# FROM main_defects m
# JOIN defect_types dt ON m.defect_type_id = dt.defect_type_id
# JOIN locations lo ON m.location_id = lo.location_id
# GROUP BY dt.defect_type_name, lo.location_name
# ORDER BY total_cost DESC;
# '''
# result_q7 = pd.read_sql(sql_q7,conn).round(2)
# print(result_q7)

# 月度缺陷数量和成本趋势
df = pd.read_sql("SELECT defect_date, repair_cost FROM main_defects", conn)

# 明确告诉 pandas 这是"月/日/年"格式
df["defect_date"] = pd.to_datetime(df["defect_date"], format="%m/%d/%Y")

df["de_month"] = df["defect_date"].dt.to_period("M").astype(str)

result_monthly = df.groupby("de_month", as_index=False).agg(
    defect_count=("repair_cost", "count"),
    total_cost=("repair_cost", "sum"),
    avg_cost=("repair_cost", "mean")
).round(2)

print(result_monthly)

conn.close()