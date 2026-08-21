import sqlite3 as sql
# import matplotlib.pyplot as plt

#defect_id,product_id,defect_type,defect_date,defect_location,severity,inspection_method,repair_cost

with sql.connect("quality.db") as conn:
    cursor = conn.cursor()
    #cursor.execute("select * from defects order by defect_date desc limit 10")
    cursor.execute("""
        SELECT 
            defect_type,
            count(*) AS defect_count
        from defects
        group by defect_type
        order by defect_count desc            
    """)
    all_products = cursor.fetchall()

    for product in all_products:
        print(product)
    # cursor.execute("select avg(repair_cost) from defects  ")
    # all_products = cursor.fetchall()
    # id_list = []
    # count_list = []
    # for product in all_products:
    #     print(product)




    #     id_list.append(str(product[0]))
    #     count_list.append(product[1])
    # plt.figure(figsize = (30,10))
    # plt.bar (id_list,count_list)
    # plt.show()




