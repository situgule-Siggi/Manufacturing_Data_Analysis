from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "quality.db"


def load_defects() -> pd.DataFrame:
    """从 SQLite 数据库读取 defects 表。"""

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(f"找不到数据库：{DATABASE_FILE}")

    query = """
        SELECT
            defect_id,
            product_id,
            defect_type,
            defect_date,
            defect_location,
            severity,
            inspection_method,
            repair_cost
        FROM defects
    """

    with sqlite3.connect(DATABASE_FILE) as connection:
        df = pd.read_sql_query(
            query,
            connection,
            parse_dates=["defect_date"]
        )

    return df


def main() -> None:
    df = load_defects()

    # print(df.head())
    # print(df.info())
    print(df.describe(include="all"))


if __name__ == "__main__":
    main()