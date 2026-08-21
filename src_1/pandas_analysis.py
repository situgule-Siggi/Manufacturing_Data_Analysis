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


def main():
    df = load_defects()

    # print(df.head().T )
    # print(df.info(S))
    # print(df.describe(include="all"))
    # print(df.isna().sum())
    # print(df.shape)
    # print(df.duplicated().sum())
    # print(df['defect_id'].unique())
    # print(df['severity'].unique())
    # print(df['inspection_method'].unique())
    # high_cost=df[df['repair_cost']>100]
    # print(high_cost.head())
    # top20 = df.sort_values('repair_cost', ascending=False).head(20)
    # print(top20)
    # critical_defects=df[
    #     (df['severity']=='Critical')
    #     & (df['repair_cost']>900)
    # ]
    # print(critical_defects)
    # result=df[df['severity'].isin(['Minor','Critical'])]
    # print(result)
    # print(df['defect_type'].unique())
#['Minor', 'Criti cal', 'Moderate']
    # result_asc=df.sort_values(by="repair_cost",ascending=True)

    # result_asc=df.sort_values(by=["repair_cost",'severity'],ascending=[True,True])
    # print(result_asc.head(10))
    # print(df["repair_cost"].count())
    # print(df["repair_cost"].sum())
    # print(df["repair_cost"].mean())
    # print(df["repair_cost"].min())
    # print(df["repair_cost"].max())
    # print(df["repair_cost"].median())
    # print(df.describe())
    # defect_counts = (
    #     df.groupby("defect_type")
    #     .size()
    #     .reset_index(name="h")
    #     .sort_values("h", ascending=False)
    # )
    # quality_summary=(
    #     df.groupby('defect_type ',as_index=False).agg(
    #         defect_count=('defect_id', 'count'),
    #         defect_cost=('repair_cost', 'mean'),
    #         total_cost=('repair_cost', 'sum'),
    #         maximum_cost=('repair_cost', 'max'),
    #     ).sort_values('total_cost', ascending=False)
    # )
    # print(quality_summary)
    # print(df['defect_date'].dtype)
    df["defect_month"] = df["defect_date"].dt.to_period("M").astype(str)
    # print(df['defect_month'].dtype)
    # print(df['defect_date'])
    # df["is_high_risk"] = df["severity"].isin(["High", "Critical"])
    monthly_cost=(
        df.groupby("defect_month", as_index=False)
          .agg(
            cocunt_defect=("defect_date", "count"),
            total_cost_defect=("repair_cost", "sum")
        ).sort_values("defect_month", ascending=False)
    )
    # print(df['is_high_risk'].unique())
    # count_risk=(
    #     df.groupby("defect_month", as_index=False)
    #     .agg(
    #         count_risk=("is_high_risk", "count"),
    #     ).sort_values("count_risk", ascending=False)
    # )
    # print(count_risk)
    # print(monthly_cose)
    print(df['product_id'].nunique())
    df['cost_category']=pd.cut(
        df['repair_cost'],
        bins=[0,100,300,float("inf")],
        labels=['Low cost','Medium Cost','High Cost']
    )
    # print(df)

    def create_quality_summary(df):
        summary = (
            df.groupby("defect_type", as_index=False)
              .agg(
                  defect_count=("defect_id", "count"),
                  affected_products=("product_id", "nunique"),
                  average_cost=("repair_cost", "mean"),
                  total_cost=("repair_cost", "sum"),
                  maximum_cost=("repair_cost", "max")
              )
              .sort_values("total_cost", ascending=False)
        )

        summary["average_cost"] = summary["average_cost"].round(2)
        summary["total_cost"] = summary["total_cost"].round(2)
        summary["maximum_cost"] = summary["maximum_cost"].round(2)

        return summary

    # summary = create_quality_summary(df)
    # output_file = BASE_DIR / "quality_report.xlsx"
    # with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    #     df.to_excel(
    #         writer,
    #         sheet_name="Raw Data",
    #         index=False
    #     )
    #
    #     summary.to_excel(
    #         writer,
    #         sheet_name="Defect Summary",
    #         index=False
    #     )
    #
    #     monthly_cost.to_excel(
    #         writer,
    #         sheet_name="Monthly Analysis",
    #         index=False
    #     )


    plt.figure(figsize=(10, 5))

    plt.plot(
        monthly_cost["defect_month"],
        monthly_cost["total_cost_defect"],
        marker="o"
    )

    plt.title("Monthly Repair Cost")
    plt.xlabel("Month")
    plt.ylabel("Repair Cost")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# defect_id,product_id,defect_type,defect_date,
# defect_location,severity,inspection_method,repair_cost

if __name__ == "__main__":
    main()