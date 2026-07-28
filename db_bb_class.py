import sqlite3 as sql

#1）链接数据库
# conn=sql.connect("defects.db")
# #2）创建游标
# cursor=conn.cursor()
# #3）通过游标对象，执行sql
# # cursor.execute(
# #                 """
# #                 CREATE TABLE defects
# #                 """)
#
# #4)通过连接对象，来提交事务
# conn.commit()
# #5）关闭连接
# cursor.close()
# conn.close()
#
# #2 增删改查（最好使用？/占位符，不要使用字符串拼接）
# with sql.connect("quality.db") as conn:
#     cursor = conn.cursor()
# #数据插入：
#     #1）通过？占位符的形式插入单条数据，类型是元组tuple
#     #cursor.execute("insert into prople ( name,age) values (?,?)",("jon",18))
#     #2）通过命名参数的形式插入数据，类型是字典.
#     #cursor.execute("insert into prople ( name,age) values (:key_1,key_2)",{"key_1":"jon","key_2":25}
#     #3）批量插入数据
#     # users=[("jon",25),("ferf",15),("rere",52)]
#     # cursor.executemany("insert into prople ( name,age) values (?,?)",users)
#     res=cursor.execute("select * from defects")
#     print(res)
#数据查找：
with sql.connect("quality.db") as conn:
    cursor = conn.cursor()
    # cursor.execute("select * from defects limit 5")
    # all_defects=cursor.fetchall()
    # for i in all_defects:
    #     print(i)
    cursor.execute("SELECT * FROM defects where  defect_id=? ",(1,))
    defects = cursor.fetchall()
    print(f"id=1:{defects}")
#数据更新
with sql.connect("quality.db") as conn:
    cursor = conn.cursor()
    cursor.execute("update defects set defect_type =? where defect_id=? ",( "上次你说",1))
    cursor.execute("select * from defects where defect_id=? ",(1,))
    print(cursor.fetchall())
#数据的删除
with sql.connect("quality.db") as conn:
    cursor = conn.cursor()

