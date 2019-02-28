import random,hashlib
hash = hashlib.md5()#md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
# hash.update(bytes('admin',encoding='utf-8'))#要对哪个字符串进行加密，就放这里
# print(hash.hexdigest())#拿到加密字符串

#可以选择加盐方式1：
# 随机生成10个数字
hash.update(bytes('admin',encoding='utf-8'))#要对哪个字符串进行加密，就放这里
salt = '.'.join(random.sample('01234567890abcdefghigABCDEFGHI', 10))
print(hash.hexdigest()+salt)#拿到加密字符串
print(salt)
print('-----------------------')

# 【通用】可以选择加盐方式2：
# 随机生成10个数字
password='haha123456'
salt = '.'.join(random.sample('01234567890abcdefghigABCDEFGHI', 10))
m = hashlib.md5()
m.update((password + salt).encode('utf-8'))
passwordn = m.hexdigest()# 加密结果
print(salt)

print(passwordn)