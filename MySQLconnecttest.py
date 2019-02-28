# # -*- coding: utf-8 -*-
# #!/usr/bin/env python
#
# import pymysql
# # https://blog.csdn.net/just_so_so_fnc/article/details/72995731
# # https://blog.csdn.net/dongweionly/article/details/80273095
#
#
#
# # 建立数据库连接的函数
# def connectdb():
#     print('连接到mysal服务器...')
#     db = pymysql.Connect(
#         host='localhost',#本地主机
#         port=3306,#端口
#         user='root',#当前用户名
#         passwd='123456',#数据库密码
#         db='firstdb',#数据库名称
#         charset='utf8',
#         cursorclass=pymysql.cursors.DictCursor)
#     print('连接上了！')
#     return db
# # connectdb()
#
#
# import pymysql
#
# # 建立数据库连接
# conn = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='firstdb',
#     charset='utf8'
# )
#
# # 获取游标
# cursor = conn.cursor()
# # print(conn)
# # print(cursor)
#
# # 1、从数据库中查询
# # sql="INSERT INTO login(user_name,pass_word)"
# #sql = "SELECT *FROM new_table"
# sql = "SELECT *FROM letters"
# # cursor执行sql语句
# cursor.execute(sql)
# # 打印执行结果的条数
# print(cursor.rowcount)
#
# # 使用fetch方法进行遍历结果  总共有三条数据
# #####注意：这三种方法不能同时进行，不然显示的条数会有所改变
# #rs=cursor.fetchone()#将第一条结果放入rs中
# #print(rs)
# #re=cursor.fetchmany(5)#将多个结果放入re中
# #print(re)
# rr = cursor.fetchall()  # 将所有的结果放入rr中
# print(rr)
# # 对结果进行处理
# for row in rr:
#     print("letter_id是：%s, letter_name：%s, content：=%s,name_id：%s" % row)
# # print(re)#输出两条数据，因为fetch()方法是建立在上一次fetch()方法基础上的
#
#
# # # 2数据库中插入数据(提交一次之后即可，多次提交会出错：pymysql.err.IntegrityError: (1062, "Duplicate entry '7' for key 'PRIMARY'"))
# # sql_insert = "INSERT INTO letters values(7,'hh','ss',2)"
# # # 执行语句
# # cursor.execute(sql_insert)
# # # 事务提交，否则数据库得不到更新
# # conn.commit()
# # print(cursor.rowcount)
#
# # # 修改数据库中的内容(提交一次之后即可)
# # sql_update = "UPDATE letters SET letter_name='hhh123' WHERE letter_id=7"
# # cursor.execute(sql_update)
# # conn.commit()
#
#
# # (提交一次之后即可)
# # # # 删除数据库中的内容，并利用try catch语句进行事务回滚
# # try:
# #     sql_delete = "DELETE FROM letters WHERE letter_id=7"
# #     cursor.execute(sql_delete)
# #     conn.commit()
# # except Exception as e:
# #     print(e)
# #     # 事务回滚，即出现错误后，不会继续执行，而是回到程序未执行的状态，原先执行的也不算了
# #     conn.rollback()
# #
# # 数据库连接和游标的关闭
# conn.close()
# cursor.close()
#
