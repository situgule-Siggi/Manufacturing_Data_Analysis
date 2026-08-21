from pathlib import Path
import sqlite3
import pandas as pd
# from numpy.ma.core import maximum, count
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "quality.db"


def load_defects() -> pd.DataFrame:
    """从 SQLite 数据库读取 defects 表。"""

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(f"找不到数据库：{DATABASE_FILE}")

    query = ("""
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
    """)

    with sqlite3.connect(DATABASE_FILE) as connection:
        df = pd.read_sql_query(
            query,
            connection,
            parse_dates=["defect_date"]
        )

    return df

def main():
    df = load_defects()
#哪种 Defect Type 带来的维修成本最高？
    result_defect = (
        df.groupby("defect_type", as_index=False).agg(
            total_count=('defect_id', 'count'),
            total_cost=('repair_cost', 'sum'),
            avg_cost=('repair_cost', 'mean')
        )
    )
    # print(result_defect)
# Severity 和 Repair Cost 有没有明显关系？
    result_severity = (
        df.groupby("severity", as_index=False).agg(
            total_count=('defect_id', 'count'),
            # total_cost=('repair_cost', 'sum'),
            avg_cost=('repair_cost', 'mean')
        ).round(2)
    )
# 哪种Inspection_Method,检出的,Critical / Moderate,缺陷最多?
    result_method = (
        df[df["severity"].isin(["Critical", "Moderate"])]
        .groupby("inspection_method", as_index=False)
        .agg(total_count=('defect_id', 'count'))
        .sort_values("total_count", ascending=False)
    )
    # print(result_method)

def pareto_by_product(df: pd.DataFrame):
    """按 product_id 做维修成本的帕累托分析"""

    result_product = (
        df.groupby("product_id", as_index=False).agg(
            total_count=('defect_id', 'count'),
            total_cost=('repair_cost', 'sum')
        )
    )

    pareto_df = result_product.sort_values("total_cost", ascending=False).reset_index(drop=True)
    pareto_df["cum_cost"] = pareto_df["total_cost"].cumsum()
    pareto_df["cum_pct"] = pareto_df["cum_cost"] / pareto_df["total_cost"].sum() * 100

    print(pareto_df)

    # 找出贡献前80%成本的"关键少数"产品
    vital_few = pareto_df[pareto_df["cum_pct"].shift(fill_value=0) < 80]
    print(f"\n关键少数产品数量：{len(vital_few)} / 共 {len(pareto_df)} 个产品")
    print(f"占比：{len(vital_few) / len(pareto_df) * 100:.1f}%")
    print("关键少数产品列表：")
    print(vital_few["product_id"].tolist())

    # ---------- 画图 ----------
    fig, ax1 = plt.subplots(figsize=(12, 6))

    bars = ax1.bar(pareto_df["product_id"].astype(str), pareto_df["total_cost"], color='steelblue')
    ax1.set_xlabel("Product ID")
    ax1.set_ylabel("Total Repair Cost", color='steelblue')
    ax1.tick_params(axis='x', rotation=90)

    ax2 = ax1.twinx()
    ax2.plot(pareto_df["product_id"].astype(str), pareto_df["cum_pct"],
              color='red', marker='o', linewidth=2, markersize=4)
    ax2.set_ylabel("Cumulative %", color='red')
    ax2.set_ylim(0, 110)

    ax2.axhline(80, color='gray', linestyle='--', linewidth=1)
    ax2.text(len(pareto_df) - 1, 82, '80%', color='gray', ha='right')

    plt.title("Pareto Analysis: Repair Cost by Product ID")
    plt.tight_layout()
    plt.show()

    return pareto_df


if __name__ == "__main__":
    df = load_defects()
    pareto_by_product(df)
# 创建 2行 x 2列 的画布，共4个子图，共享同一个figure
#     fig, axes = plt.subplots(2, 2, figsize=(12, 12))
#
#     # 子图1：缺陷数量
#     bar_1 = axes[0, 0].bar(result_defect["defect_type"], result_defect["total_count"], color='steelblue')
#     axes[0, 0].bar_label(bar_1, padding=3)
#     axes[0, 0].set_title("Count by Type")
#     axes[0, 0].set_xlabel("type")
#     axes[0, 0].set_ylabel("count")
#
#     # 子图2：总维修成本
#     bar_2 = axes[0, 1].bar(result_defect["defect_type"], result_defect["total_cost"], color='orange')
#     axes[0, 1].bar_label(bar_2, padding=3, fmt='%.0f')
#     axes[0, 1].set_title("Total Repair Cost by Type")
#     axes[0, 1].set_xlabel("type")
#     axes[0, 1].set_ylabel("total cost")
#
#     # 子图3：平均维修成本
#     bar_3 = axes[1, 0].bar(result_severity['severity'], result_severity['avg_cost'], color='steelblue' )
#     axes[1, 0].bar_label(bar_3, padding=3)
#     axes[1, 0].set_title("Severity by Type")
#     axes[1, 0].set_xlabel("type")
#     axes[1, 0].set_ylabel("cost")
#     # 子图4：空着，或者放别的统计
#     bar_4 = axes[1, 1].bar(result_method['inspection_method'], result_method['total_count'], color='steelblue')
#     axes[1, 1].bar_label(bar_4, padding=3, fmt='%.0f')
#     axes[1, 1].set_title("Inspection Method by Type")
#     axes[1, 1].set_xlabel("type")
#     axes[1, 1].set_ylabel("count")
#
#     # ---------- Pareto 分析：按 defect_type 的维修成本 ----------
#     pareto_df = result_defect.sort_values("total_cost", ascending=False).reset_index(drop=True)
#     pareto_df["cum_cost"] = pareto_df["total_cost"].cumsum()
#     pareto_df["cum_pct"] = pareto_df["cum_cost"] / pareto_df["total_cost"].sum() * 100
#
#     print(pareto_df[["defect_type", "total_cost", "cum_pct"]])
#
#     fig2, ax1 = plt.subplots(figsize=(9, 6))
#
#     # 柱状图：单项成本
#     bars = ax1.bar(pareto_df["defect_type"], pareto_df["total_cost"], color='steelblue')
#     ax1.bar_label(bars, padding=3, fmt='%.0f')
#     ax1.set_xlabel("Defect Type")
#     ax1.set_ylabel("Total Repair Cost", color='steelblue')
#     ax1.tick_params(axis='x', rotation=45)
#
#     # 折线图：累计百分比（右轴）
#     ax2 = ax1.twinx()
#     ax2.plot(pareto_df["defect_type"], pareto_df["cum_pct"],
#               color='red', marker='o', linewidth=2)
#     ax2.set_ylabel("Cumulative %", color='red')
#     ax2.set_ylim(0, 110)
#
#     # 80% 参考线
#     ax2.axhline(80, color='gray', linestyle='--', linewidth=1)
#     ax2.text(len(pareto_df) - 1, 82, '80%', color='gray')
#
#     plt.title("Pareto Analysis: Repair Cost by Defect Type")
#     plt.tight_layout()
#     plt.show()


# 不需要就隐藏
#
#     for ax in axes.flat:
#         ax.tick_params(axis='x', rotation=45)
#
#     plt.tight_layout()
#     plt.show()
# #
#
#     # print(df['severity'].unique())
#
#     print(result_severity)
# defect_id,product_id,defect_type,defect_date,
# defect_location,severity,inspection_method,repair_cost
#
# if __name__ == "__main__":
#     main()