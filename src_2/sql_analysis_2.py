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

#Q1 找出缺陷数量大于 10 的产品。
# sql_q1='''
# select
#     product_id,
#     count(product_id) as defect_count,
#     sum(repair_cost) as repair_cost
# from main_defects as m
# group by product_id
# having count(product_id) > 10
# order by defect_count
# '''
#
# results = pd.read_sql(sql_q1, conn).round(2)
# print(results)

# 人为建立维修成本等级
# sql_q2='''
# select
#     product_id,
#     sum(repair_cost)as total_cost,
#     case
#         when sum(repair_cost) < 3000 then 'low'
#         when sum(repair_cost) < 10000 then 'medium'
#         else 'high'
#     end as Cost_level
# from main_defects
# group by product_id
# order by total_cost desc
# '''
# results2=pd.read_sql(sql_q2,conn)
# print(results2 )

# CTE比如先计算每个产品总维修成本：

sql_q2='''
with products_cost as (
    select
        product_id,
        --severity,
        --method_id,
        --repair_cost,
        sum(repair_cost) as id_repair_cost
    from main_defects 
    group by product_id
    order by 'Percentage%'
)
select 
    *,
    rank () over ( order by id_repair_cost desc ) as cost_rank,
    sum(id_repair_cost) over (),
    --sum(id_repair_cost) over (partition by product_id ) as total_repair_cost
    round(id_repair_cost/sum(id_repair_cost) over () *100,2 ) as 'Percentage%'
from products_cost
--- order by total_repair_cost desc
'''
results = pd.read_sql(sql_q2, conn)
print(results)

