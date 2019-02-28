# -*- encoding=UTF-8 -*-
from nowins import app,db
# from nowins import db
from flask_script import Manager
from nowins.models import User, Image, Comment
import random
manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'

#数据库交互
@manager.command
def init_database():
    db.drop_all()# 删掉所有的表
    db.create_all()# 创建所有的表
    # 使用terminal命令行：python manager.py init_database
    for i in range(0, 100):
        db.session.add(User('牛客' +str(i+1), 'a'+str(i+1)))

        for j in range(0, 10): #每人发是10张图
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('这是一条评论'+str(k), 1+10*i+j, i+1))
    db.session.commit() # 提交事务

#----------------------------查询语句-------------------

    # print(db.session.query(User).all())
    # print(repr(User.query.all()))
    # print(1,User.query.all())
    # print(2,User.query.get(2)) #查询id为2的用户
    # print(3, User.query.filter_by(id=2).first())#查询id为2的用户
    # print(4, User.query.order_by(User.id.desc()).offset(1).limit(2).all()) # desc为降序 offset从第几条开始读取默认为零,limit是读取几条
    # print(5,User.query.filter(User.username.endswith('0')).limit(3).all())# LIKE 查询结尾是零的username的3个数据
    # # 5 [<User10 : 牛客10>, <User20 : 牛客20>, <User30 : 牛客30>]
    # #组合查询 80or99
    # from sqlalchemy import or_,and_
    # print(6,User.query.filter(or_(User.id ==88,User.id == 99)).all())
    # # 6[ < User88: 牛客88 >, < User99: 牛客99 >]
    # #将all()去掉，就是sql语句
    # print(7,User.query.filter(or_(User.id ==88,User.id == 99)))
    # #组合查询大于88小于93
    # print(8,User.query.filter(and_(User.id > 88,User.id < 93)).all())
    # print(9,User.query.filter(and_(User.id > 100,User.id < 105)).first_or_404())# 有数据就打印出来第一条，没有就打印404 abort404
    # #分页显示
    # print(10,User.query.paginate(page=1,per_page=10).items)# 分页显示，第一页，一页十个
    # print(11, User.query.order_by(User.id.desc()).paginate(page=1,per_page=10).items) # 先逆序再分页显示，第一页，一页十个

    # user = User.query.get(1)
    # print(11, user)
    # #11 < User1: 牛客1 >
    # print(22, user.images)
    # # 查询语句
    # print(22, user.images.all())
    # # 22 [<Image1 http://images.nowcoder.com/head/700m.png>, <Image2 http://images.n
    # # owcoder.com/head/408m.png>, <Image3 http://images.nowcoder.com/head/553m.png>]
    # print(33, Image.query.get(1).user)
    # # 33 <User1 : 牛客1>
    # image = Image.query.get(1)
    # print(44,image.user)
    # #44 <User1 : 牛客1>
    # #对应上句image.user如果不添加backref,那么会报错,相当于添加了user属性。images = db.relationship('Image', backref='user', lazy='dynamic')# 关系型数据库添加的
    # print(55,image,image.user)# 含义是第一张图片，对应的是第一个用户
    # #55 <Image1 http://images.nowcoder.com/head/509m.png> <User1 : 牛客1>
    # #https://www.cnblogs.com/RomanticLife/p/8372624.html

#--------------------------------END-----------------------------------

#-------------------Update更新--------------------------------
# # #更新1
#
#     for i in range(50, 100, 2):
#         # 通过设置属性
#         u = User.query.get(i)
#         print(u)
#         u.username = '[NEW1]' + u.username
#         print(u)
#     db.session.commit()
#
#     # 更新其中一条
#     User.query.filter_by(id=51).update({'username': '牛客新' + str(51)})
#     print(51,User.query.get(51))
#     # 51 <User51 : 牛客新51>
#     db.session.commit()
#
# #更新2
#     for i in range(0, 100, 10):
#         # 通过update函数
#         User.query.filter_by(id=i + 1).update({'username': '牛客新' + str(i+1)})
#     db.session.commit()
#
#
#     #print(98,User.query.get(98))
#     # <User98 : [NEW]牛客98>
#-------------------------------END-------------------------------


#---------------------------删除------------------
# # 删除
# for i in range(50, 100, 2):
#     Comment.query.filter_by(id = i + 1).delete()
# for i in range(51, 100, 2):
#     comment = Comment.query.get(i + 1)
#     db.session.delete(comment)
# db.session.commit()
#---------------------------------END----------------------




if __name__ == '__main__':
    manager.run()



