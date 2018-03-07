import api.src.lib.conf as conf

# def envShow(self):
#     for k, v in os.environ.items():
#         if k in ['LXDUI_LOG', 'LXDUI_CONF']:
#             print('{} = {}'.format(k, v))

c = conf.Config()
c.envSet()
if c.envGet():
    print("Something found")
else:
    print("Nothing found")
print(c.envGet())
# c.envSet()
# print(c.envGet())