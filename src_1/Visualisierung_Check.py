from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或者用 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

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


def plot_repair_cost(df: pd.DataFrame) -> None:
    # 取出 repair_cost 列(Series)
    repair_cost = df['repair_cost']

    plt.figure(figsize=(10, 5))
    plt.plot(repair_cost.values, marker='o', linestyle='-')
    plt.title('Repair Cost 折线图')
    plt.xlabel('索引 (记录序号)')
    plt.ylabel('Repair Cost')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main() -> None:
    df = load_defects()

    high_cost=df[df['repair_cost']>100]
    print(high_cost.head())






