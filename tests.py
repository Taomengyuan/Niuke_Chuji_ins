#-*- encoding=UTF-8 -*-
import unittest
from nowins import app

class NowinsTest(unittest.TestCase):
    #  # 每次跑单元测试的时候都会跑，用于初始化测试数据
    def setUp(self):
        #添加测试配置
        app.config['TESTING']=True
        self.app=app.test_client()# 获得测试所需的实例app
        print('setup')


    # 每次都会运行,清理测试数据
    def tearDown(self):# 清理数据
        print('teardown')
    #
    # def test1(cls):
    #     print('test1')

    # 模拟注册函数，其实就是仿照postman；对注册函数使用post请求，看返回码是否符合；
    def register(self,username,password):
        return self.app.post('/reg/', data={"username":username, "password":password}, follow_redirects=True)
    # 模拟登录函数
    def login(self, username, password):
        return self.app.post('/login/', data={"username": username, "password": password}, follow_redirects=True)
 # 模拟登出函数
    def logout(self):
        return self.app.get('/logout/') #写法一定要和views中保持一致

 # 测试函数，测试注册登录登出-------------OK
    def test_reg_logout_login(self):
        assert self.register("hello", "world").status_code == 200  # 测试是否为200的status_code
        # # 下面‘-hello’显示错误：TypeError: a bytes-like object is required, not 'str'
        # # 需要进行str-bytes转换
        # # str to bytes:(3种方式） https://www.cnblogs.com/dpf-learn/p/8028121.html
        # assert '-hello'.encode(encoding='utf-8') in self.app.open('/').data  # 测试注册的用户hello是否在数据库中
        # self.logout()
        # # assert '-hello'.encode(encoding='utf-8') not in self.app.open('/').data  # 各种测试，总之就是考虑全面，才能保证测试的完整性
        # self.login("hello", "world")
        # assert '-hello'.encode(encoding='utf-8') in self.app.open('/').data

        hello='-hello'.encode(encoding='utf-8')
        assert hello in self.app.open('/').data  # 测试注册的用户hello是否在数据库中
        self.logout()
        self.assertNotIn(hello,self.app.open('/').data)# 该方法和下面那种方法都可以
        # assert hello not in self.app.open('/').data  # 各种测试，总之就是考虑全面，才能保证测试的完整性
        self.login("hello", "world")

        assert hello in self.app.open('/').data