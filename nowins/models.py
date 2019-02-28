# -*- encoding=UTF-8 -*-
#  参考： https://www.jianshu.com/p/dbeec464c3ad

from nowins import db, login_manager
from datetime import datetime
import random
# login_manager 需要从nowins中导入

class Comment(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))# image表中的id和comment中的id相关联
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user表中的id和comment中的id相关联
    status = db.Column(db.Integer, default=0) # 0 正常 1删除 商用网站会用，防止误删
    user = db.relationship('User')
    # 表示user是从哪个表来的，是从user

     # 构造函数 user从外界来的，status默认为0
    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):
        return ('<Comment%d %s>' % (self.id, self.content))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))# 关系型数据库添加的，user.id表示user表中的id和image中的id相关联
    created_date = db.Column(db.DateTime)
    comments = db.relationship('Comment') # 关系型数据库添加的
    # 表示评论是从哪个表来的，是从Comment

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):
        return '<Image%d %s>' % (self.id, self.url)

class User(db.Model):
    #__tablename__ = 'myuser' 指定表名字
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image', backref='user', lazy='dynamic')# 关系型数据库添加的
    # 1.db.Relationship()第一个参数表明这个关系的另一端是哪个模型（类）。如果模型类尚未定义，可使用字符串形式指定。
    # 2.db.Relationship()第二个参数backref，将向User类中添加一个role属性，从而定义反向关系。这一属性可替代role_id访问Role模型，此时获取的是模型对象，而不是外键的值。
    # 链接：https://www.jianshu.com/p/dbeec464c3ad

    #images = db.relationship('Image')

    def __init__(self, username, password,salt=''):
        self.username = username
        self.password = password #暂时明文，下节课讲解加
        # self.datatime = datetime.now()
        self.salt = salt
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 't.png'

    def __repr__(self):
        # return ('<User %d %s>' % (self.id, self.username)).encode('gbk')
        return ('<User%d : %s>'% (self.id, self.username))
        # return ('<User id:%d name:%s>'% (self.id, self.username))

    # Flask Login接口
    def is_authenticated(self):
        print ('is_authenticated')
        return True

    def is_active(self):
        print ('is_active')
        return True

    def is_anonymous(self):
        print ('is_anonymous')
        return False

    def get_id(self):
        print('get_id')
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)