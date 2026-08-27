from pathlib import Path
import sqlite3
import pandas as pd


# === 数据库里的表 ===
#            table_name
# 0            products
# 1        defect_types
# 2     sqlite_sequence
# 3           locations
# 4  inspection_methods
# 5        main_defects


BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "quality_v2.db"

conn = sqlite3.connect(DB_FILE)

# 查看所有表
tables = pd.read_sql("""
        SELECT name AS table_name
        FROM sqlite_master
        WHERE type = 'table'
--        ORDER BY name;
    """, conn)

print("=== 数据库里的表 ===")
print(tables)

# 查看 products
# print("\n=== products ===")
# products = pd.read_sql("""
#         SELECT *
#         FROM products
#         ORDER BY product_id;
#     """, conn)

# print(products)

# 查看main_defects
print("\n=== main_defects ===")
main_defects = pd.read_sql("""
        SELECT *
        FROM main_defects
    """, conn)

print(main_defects.columns)

# # 查看 table 内容
name_table= 'inspection_methods'
print(f'\n=== {name_table} ===')

result = pd.read_sql(f"""
        SELECT *
        FROM {name_table}
    """, conn)

print(result)

conn.close()