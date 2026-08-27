from pathlib import Path
import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

BASE_DIR = Path(__file__).resolve().parent
Project_DIR = BASE_DIR.parent


# 1. 读取原始 CSV
CSV_FILE=Project_DIR/'data'/'raw'/'defects_data.csv'
df = pd.read_csv(CSV_FILE)

# 2. 连接新的 SQLite 数据库
conn = sqlite3.connect("quality_v2.db")
cursor = conn.cursor()

# 3. 开启外键支持
cursor.execute("PRAGMA foreign_keys = ON;")

# 4. 创建 products 表
# cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS products (
#                 product_id INTEGER PRIMARY KEY
#                 )
#         """)

# 5. 从原始数据中提取唯一 product_id
# products = (
#     df[["product_id"]]
#     .drop_duplicates()
#     .sort_values("product_id")
# )
#
# print(products.head())
# print("产品数量:", len(products))
#
# # 6. 写入数据库
# products.to_sql(
#     "products",
#     conn,
#     if_exists="append",
#     index=False
# )

#创建 defect_types 表格
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS defect_types (
#     defect_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     defect_type_name TEXT NOT NULL UNIQUE
# )
# """)

# defect_types = (
#     df[["defect_type"]]
#     .drop_duplicates()
#     .rename(columns={"defect_type": "defect_type_name"})
# )
#
# print(defect_types)
#
# defect_types.to_sql(
#     "defect_types",
#     conn,
#     if_exists="append",
#     index=False
# )

# 建立locations工作表
# cursor.execute("""
#         CREATE TABLE IF NOT EXISTS locations (
#             location_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             location_name TEXT NOT NULL UNIQUE
#         )
#     """)
#
# locations = (
#     df[["defect_location"]]
#     .drop_duplicates()
#     .rename(columns={"defect_location": "location_name"})
# )
#
# print(locations)
#
# locations.to_sql(
#     "locations",
#     conn,
#     if_exists="append",
#     index=False
# )

# 建立inspection_methods工作表
# curs

# 创建建核心表 defects
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS main_defects (
#         defect_id INTEGER PRIMARY KEY,
#         product_id INTEGER NOT NULL,
#         defect_type_id INTEGER NOT NULL,
#         defect_date TEXT NOT NULL,
#         location_id INTEGER NOT NULL,
#         severity TEXT NOT NULL,
#         method_id INTEGER NOT NULL,
#         repair_cost REAL,
#
#         FOREIGN KEY (product_id)
#             REFERENCES products(product_id),
#
#         FOREIGN KEY (defect_type_id)
#             REFERENCES defect_types(defect_type_id),
#
#         FOREIGN KEY (location_id)
#             REFERENCES locations(location_id),
#
#         FOREIGN KEY (method_id)
#             REFERENCES inspection_methods(method_id)
#     )
#     """)

# cursor.execute("""
#     DROP TABLE defects
# """)

# conn.commit()
# cursor.execute("""
#     ALTER TABLE defects
#     RENAME TO main_defects
# """)

#映射表格
type_map = pd.read_sql("""
SELECT
    defect_type_id,
    defect_type_name
FROM defect_types
""", conn)

location_map = pd.read_sql("""
SELECT
    location_id,
    location_name
FROM locations
""", conn)

method_map = pd.read_sql("""
SELECT
    method_id,
    method_name
FROM inspection_methods
""", conn)

print(type_map)
print(location_map)
print(method_map)

df = df.merge(
    type_map,
    left_on="defect_type",
    right_on="defect_type_name",
    how="left"
)

df = df.merge(
    location_map,
    left_on="defect_location",
    right_on="location_name",
    how="left"
)

df = df.merge(
    method_map,
    left_on="inspection_method",
    right_on="method_name",
    how="left"
)

# print(df.head())

#选出 main_defects 真正需要的字段
main_defects = df[[
    "defect_id",
    "product_id",
    "defect_type_id",
    "defect_date",
    "location_id",
    "severity",
    "method_id",
    "repair_cost"
]]
# print(main_defects.head())
# print(main_defects.dtypes)

# 写入 main_defects
# main_defects.to_sql(
#     "main_defects",
#     conn,
#     if_exists="append",
#     index=False
# )

result = pd.read_sql("""
        SELECT *
        FROM main_defects
        LIMIT 10;
    """, conn)

# print(result)

# 在写数据库之前，检查有没有映射失败
# print(main_defects.isnull().sum())

# 然后开始做 JOIN，便于阅读的结果表
read_join = pd.read_sql("""
    SELECT
    m.defect_id,
    m.product_id,
    dt.defect_type_name,
    l.location_name,
    im.method_name,
    m.severity,
    m.repair_cost
FROM main_defects m
JOIN defect_types dt
    ON m.defect_type_id = dt.defect_type_id
JOIN locations l
    ON m.location_id = l.location_id
JOIN inspection_methods im
    ON m.method_id = im.method_id
LIMIT 20;
    """, conn)

print(read_join)
# 7. 保存并关闭
conn.commit()
conn.close()