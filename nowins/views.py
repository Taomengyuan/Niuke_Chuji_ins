# -*- encoding=UTF-8 -*-
from nowins import app,db
from nowins.models import Image,User
from flask import render_template, redirect,request,flash,get_flashed_messages
import random,hashlib,json
from flask_login import login_user, logout_user,login_required


@app.route('/')
def index():
    # return 'hello~~~~~'
    images = Image.query.order_by(Image.id.desc()).limit(10).all()
    return render_template('index.html',images=images)
# import pymysql

@app.route('/image/<int:image_id>/')
@login_required # 表示只有登陆之后才可使用

def image(image_id):

    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    else:
        return render_template('pageDetail.html',image=image)
import pymysql


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    # 分页显示，注意不要丢掉filterby，不然profile页面就只是前两张图片
    # per_page = 3 改成 每页显示3个
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3)
    # 传输的数据在这里显示
    return render_template('profile.html', user = user,has_next=paginate.has_next,images=paginate.items)

# 跳转提交显示的表单内容
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    # 参数检查
    paginate = Image.query.filter_by(user_id = user_id).paginate(page=page,per_page=per_page)

    map = {'has_next':paginate.has_next} # false表示最后一页，true表示还有下一页
    images = []
    for image in paginate.items:
        imgvo = {'id':image.id, 'url':image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)
# has_next false 表示最后一页，true表示除了最后一页的其余页
# 输出格式：{"has_next": false, "images": [{"id": 300, "url": "http://images.nowcoder.com/head/672m.png", "comment_count": 3}]}


@app.route('/reglogin/')
def reglogin():
    # false不用获取，只用来过滤

    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):

        msg = msg + m
    # 如果已经登录的就跳到首页或当前页，使用next参数
    return render_template('login.html',msg=msg,next= request.values.get('next'))

# target是登录页
def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

# 添加一个登陆的接口
@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    # 校验
    user = User.query.filter_by(username=username).first()
    #判断是否为空
    if username == '' or password == '':
        return redirect_with_msg('/reglogin/', u'用户名和密码不能为空', 'reglogin')
    #先把用户名查询出来
    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg('/reglogin/', u'用户名不存在', 'reglogin')
    # 然后对密码重新加密
    m = hashlib.md5()
    # 更新m为盐和password
    m.update((password+user.salt).encode('utf-8'))
    # 当两者不相等时密码错误
    if m.hexdigest() != user.password:
        return redirect_with_msg('/reglogin/', u'密码错误', 'reglogin')

    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)
    return redirect('/')


#添加一个注册的接口
@app.route('/reg/',methods={'post','get'})
def reg():
    # request.args url的参数
    # request.form body的参数
    # request.values 全部
    # strip() 前后空格去掉
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    #校验
    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        return redirect_with_msg('/reglogin/', u'用户名和密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user!= None:
        return redirect_with_msg('/reglogin/',u'用户名已存在','reglogin')

    # 更多判断
    # MD5加密 加盐加密
    # hash = hashlib.md5()  # md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
    # hash.update(bytes('admin', encoding='utf-8'))  # 要对哪个字符串进行加密，就放这里
    # print(hash.hexdigest())  # 拿到加密字符串

    # 加盐-随机生成10个数字
    salt='.'.join(random.sample('01234567890abcdefghigABCDEFGHI',10))
    m = hashlib.md5()# md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
    m.update((password+salt).encode('utf-8'))# 要对哪个字符串进行加密，就放这里
    password = m.hexdigest() # 拿到加密字符串
    user =User(username,password,salt)
    db.session.add(user)
    db.session.commit()

    # 注册完可以直接登陆
    login_user(user)
    # next 跳转到当前页面(views,login,)
    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)
    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')