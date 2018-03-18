from cli import Config, User, Init, Certificate
import hashlib
import codecs
import os

# Config tests
# c = Config()
# c.set('LXDUI', 'lxdui.port', '15151')
# print(c.get('LXDUI', 'lxdui.port'))
# c.save()
# c.show()


u = User()
# u.show()

# path = 'conf'
# for root, dirs, files in os.walk(path):
#     for file in files:
#         name, ext = os.path.splitext(file)
#         # print(extension)
#         if ext in ['.key', '.crt']:
#             print(path + '/' + file)


# c = Certificate()
# c.save('conf/test.key', c.key)
# c.save('conf/test.crt', c.cert)

# ec6d3ea0fde35b6e5220b16d9ba1a2b00160dbf8
# print(u.update('test22', 'pass'))

# print(u.authenticate('test2', 'pass2'))


# Init('secret3')
# print(Certificate.create())


# reply = input("Do you want to delete it and create a new one? [[y]/n] ")
# print(reply)

# account = u.get('test1')
# print(account)
# account[0]['password'] = u.sha_password('foo')
# print(account)

# account, err = u.get('test1')
# if account is None:
#     print(err)
# else:
#     print(account)
# print(u.get('admin'))
# u.delete('admin')
# u.show()

# u.add('test1', 'swsw')
# u.show()
# u.add('test2', 'qweqweqwe')
# u.show()
# u.add('test3', 'swasdasdassw')
# u.show()
# u.delete('test3')
# u.show()
# u.delete('foo')
# u.show()
# # u.delete('admin')
# # u.show()
# u.delete('zzz')
# u.show()
# u.delete('admin')
# u.show()

# print(u.users)
# index = None
# for user in u.users:
#     if user['user_name'] == 'test4':
#         index = u.users.index(user)
#         u.users.remove(user)
# print(u.users)
# print(index)

# print(u.users)
# # u.users.remove('user_name')
# print(u.users.index({
#     "user_name": "admin",
#     "password": "4015bc9ee91e437d90df83fb64fbbe312d9c9f05"
#   }))
# print(u.users)