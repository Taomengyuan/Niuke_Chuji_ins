# -*- encoding=UTF-8 -*-
from nowins import app,db
from nowins.models import Image,User,Comment
from flask import render_template, redirect,request,flash,get_flashed_messages,send_from_directory
import random,hashlib,json,os
from datetime import date, datetime

from flask_login import login_user, logout_user,login_required,current_user
# from qiniusdk import qiniu_upload_file
import uuid# 产生唯一识别码，用于给文件名更名
# 如果使用current_user，那么要确保当前函数是在登陆之后被要求的

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)




@app.route('/')
def index():
    # return 'hello~~~~~'
    paginate = Image.query.order_by(Image.id.desc()).paginate(page=1, per_page=3)
    # paginate = Image.query.filter_by(user_id = user_id).order_by(Image.id.desc()).paginate(page=1, per_page=3)
    # paginate = Image.query.filter_by(user_id = user_id).order_by(Image.id.desc()).paginate(page=1, per_page=3)
    # has_next = paginate.has_next, images = paginate.items
    return render_template('index.html',has_next=paginate.has_next,images=paginate.items)

# 跳转提交显示的表单内容,分页显示
@app.route('/images/<int:page>/<int:per_page>/')
def index_images(page, per_page):
    # 参数检查
    paginate = Image.query.order_by(Image.id.desc()).paginate(page=page,per_page=per_page)

    map = {'has_next':paginate.has_next} # false表示最后一页，true表示还有下一页
    # images = []
    # for image in paginate.items:
    #     imgvo = {'id':image.id, 'url':image.url, 'comment_count': len(image.comments)}
    #     images.append(imgvo)
    image = []
    for item in paginate.items:
        # imgvo = {'id':image.id, 'url':image.url, 'comment_count': len(image.comments)}
        comment_user_username = []
        comment_user_id = []
        comment_content = []
        for comments_i in item.comments:
            comment_user_username.append(comments_i.user.username)
            comment_user_id.append(comments_i.user.id)
            comment_content.append(comments_i.content)

        imgvo = {'image_user_id': item.user.id,
                 'image_user_head_url': item.user.head_url,
                 'image_user_username': item.user.username,
                 'image_id': item.id,
                 'image_url': item.url,
                 'image_created_date':str(item.created_date),
                 'image_comments_length': len(item.comments),
                 'comment_user_username': comment_user_username,
                 'comment_user_id': comment_user_id,
                 'comment_content': comment_content}

        image.append(imgvo)
    map['images'] = image
    return json.dumps(map,cls=MyEncoder)
# has_next false 表示最后一页，true表示除了最后一页的其余页
# 输出格式：{"has_next": false, "images": [{"id": 300, "url": "http://images.nowcoder.com/head/672m.png", "comment_count": 3}]}


@app.route('/image/<int:image_id>/')
@login_required # 表示只有登陆之后才可使用

def image(image_id):

    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    else:
        # comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
        return render_template('pageDetail.html',image=image)



@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    # 分页显示，注意不要丢掉filterby，不然profile页面就只是前两张图片
    # per_page = 3 改成 每页显示3个
    # 加 oderby 来显示最新的三张图片
    paginate = Image.query.filter_by(user_id = user_id).order_by(Image.id.desc()).paginate(page=1, per_page=3)
    # 传输的数据在这里显示
    return render_template('profile.html', user = user,has_next=paginate.has_next,images=paginate.items)

# 跳转提交显示的表单内容,分页显示
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    # 参数检查
    paginate = Image.query.filter_by(user_id = user_id).order_by(Image.id.desc()).paginate(page=page,per_page=per_page)

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

# 将上传的图片在本地保存,并返回一个可以访问的URL地址
def save_to_local(file, file_name):

    save_dir = app.config['UPLOAD_DIR']  # 获取根目录
    file.save(os.path.join(save_dir, file_name))  # 将上一步的根目录与文件名结合保存在本地的文件夹中
    return '/image/' + file_name  # 返回一个可以访问的URL地址，比如为/image/xxxx.jpeg


# 4.上传图片之后，web需要显示；则此处添加一个图片显示函数；
@app.route('/image/<image_name>')
def view_image(image_name):
    # flask中集成了这么一个函数，send_from_directory；当用户直接访问该URL时，就直接显示该目录下的那个图；
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)



@app.route('/upload/', methods={"post"})
@login_required
def upload():
    #-------第五节 00:31:00-使用postman检测是否可以返回ok,且查看run的窗口是否显示下行----------#
    # ------ImmutableMultiDict([('file', <FileStorage: '001.jpg' ('image/jpeg')>)])----#
    #-------print 的步骤，点击rerun之后，使用postman 输入http://127.0.0.1:5000/upload/，在fromdata页签中上传一张图片 点击send即可，看屏幕下方是否显示ok，显示ok说明交互成功
    # print(request.files)
    # file = request.files['file']
    # print(dir(file)) #['__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parse_content_type', 'close', 'content_length', 'content_type', 'filename', 'headers', 'mimetype', 'mimetype_params', 'name', 'save', 'stream']
    # return 'ok'
    #-------------------------------------END------------------------------------#

    # 1.将上传的文件的信息通过request请求获取出来，保存在变量file中；files是请求提交过来时里面的一些文件；
    # []内是上传的文件定义的key名字。如果上传的多变量，比如还有file1,file2等，直接在这个dict里更改即可，可以提取file1,file2.
    print(request.files)
    # 多个图片：Print 内容ImmutableMultiDict([('file', <FileStorage: 'h5.jpeg' ('image/jpeg')>), ('file', <FileStorage: 'h6.jpeg' ('image/jpeg')>)])
    file = request.files['file']
    # http://werkzeug.pocoo.org/docs/0.10/datastructures/
    # 需要对文件进行裁剪等操作
    # 2.将文件后缀名取出存入file_ext变量中；
    file_ext = ''
    if file.filename.find('.') > 0:
        # 后尾去空，转换成小写的进行匹配，文件名后缀
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
        # 比如为xxx.bmp，则file_ext内容为bmp
    # 3.将图片提交至服务器之前，先对文件的后缀名做一个验证，看后缀名是否在配置文件允许范围之内;若符合，则将文件保存在服务器，并获得一个URL地址
    if file_ext in app.config['ALLOWED_EXT']:
        # 获得文件整体名字，为了防止名字中含有html等干扰信息，选择用一个uuid(通用唯一识别码，就是一个随机值)的方式代替真名字
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        # url = qiniu_upload_file(file, file_name)
        url = save_to_local(file, file_name)
        # 调用写好的函数，将文件保存在服务器，并获得一个URL地址

        # 4.如果URL存在，则将该图加载到数据库当中
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()
        # current_user.id已登陆的登陆id
    # # 5.如果上面某几步失败或者全部执行完后，将跳转回当前上传图片的用户的个人详情页去
    return redirect('/profile/%d' % current_user.id)

# 用户没登录时，会产生以下错误：'AnonymousUserMixin' object has no attribute 'id' // Werkzeug Debugger
# 你用的是@auth.before_app_request，而且是在未登录之前就请求了。按照flask-login文档，默认情况下，用户没有实
# 际登录的话，current_user会被设置为AnonymousUserMixin对象的。


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                图片详情页增加评论
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 增加评论的URL，为何用post请求？
# Post，它是可以向服务器发送修改请求，从而修改服务器的，比方说，我们要在论坛上回贴、在博客上评论，这就要用到Post了，当然
# 它也是可以仅仅获取数据的。详情：https://zhidao.baidu.com/question/1759920971069677948.html
@app.route('/addcomment/', methods={'post'})
@login_required
def add_comment_to_pageDetail():
    # 1.获取Comment实例所需的属性
    image_id = int(request.values['image_id'])
    content = request.values['content']
    # 2.构造comment实例
    comment = Comment(content, image_id, current_user.id)
    # 3.将comment该条数据添加到Comment表中
    db.session.add(comment)
    db.session.commit()
    # 4.每页的评论信息存入map中，最终返回json格式用于前端显示
    return json.dumps\
    ({
        "code":0,
        "id":comment.id,
        "content":content,
            # 从users换成user即可运行成功
        "username":comment.user.username,  # 因为Comment表与User表是多对多，relationship关系；
        "user_id":comment.user.id
     })
    # return json.dumps({"code":0,"id":comment.id})