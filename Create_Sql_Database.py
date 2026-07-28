from pathlib import Path
import sqlite3
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "defects_data.csv"
DATABASE_FILE = BASE_DIR / "quality.db"


def create_database() -> None:
    """读取 CSV，清洗数据，并导入 SQLite 数据库。"""

    if not CSV_FILE.exists():
        raise FileNotFoundError(f"找不到 CSV 文件：{CSV_FILE}")

    # 1. 读取 CSV
    df = pd.read_csv(CSV_FILE)

    # 2. 删除可能由 Pandas 导出产生的无意义索引列
    if "index" in df.columns:
        df = df.drop(columns=["index"])

    # 3. 转换数据类型
    df["defect_id"] = pd.to_numeric(df["defect_id"], errors="raise")
    df["product_id"] = pd.to_numeric(df["product_id"], errors="raise")
    df["repair_cost"] = pd.to_numeric(df["repair_cost"], errors="coerce")

    # 把类似 6/25/2024 的日期统一转换为 2024-06-25
    df["defect_date"] = pd.to_datetime(
        df["defect_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # 4. 检查关键字段是否存在空值
    required_columns = [
        "defect_id",
        "product_id",
        "defect_type",
        "defect_date",
        "severity"
    ]

    if df[required_columns].isnull().any().any():
        print("警告：部分关键字段存在空值，请检查原始数据。")

    # 5. 连接 SQLite 数据库
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()

        # 6. 创建数据表
        cursor.execute("DROP TABLE IF EXISTS defects")

        cursor.execute("""
            CREATE TABLE defects (
                defect_id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                defect_type TEXT NOT NULL,
                defect_date TEXT NOT NULL,
                defect_location TEXT,
                severity TEXT NOT NULL,
                inspection_method TEXT,
                repair_cost REAL CHECK (repair_cost >= 0)
            )
        """)

        # 7. 将 DataFrame 导入数据库
        df.to_sql(
            name="defects",
            con=connection,
            if_exists="append",
            index=False
        )

        # 8. 创建索引，提高常用查询速度
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_defects_product
            ON defects(product_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_defects_date
            ON defects(defect_date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_defects_severity
            ON defects(severity)
        """)

        connection.commit()

    print(f"数据库创建成功：{DATABASE_FILE}")
    print(f"已导入 {len(df)} 条缺陷记录。")


if __name__ == "__main__":
    create_database()