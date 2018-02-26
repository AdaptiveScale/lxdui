from api.src.lib import log as logger, conf
import __metadata__ as m
import pathlib
import logging
import os
log = logging.getLogger(__name__)

# Enable logging
l = logger.Log(__name__)
# l.file = '/Users/vetoni/PycharmProjects/lxdui/conf/lxdui.log'

# c = conf.Config(conf='/Users/vetoni/PycharmProjects/lxdui/conf/lxdui.conf')
# c.show()
# c.setEnv()
# c.showEnv()
# k, i = c.getEnv()
# print(k)
# print(i)

# env = ['LXDUI_LOG_DIR', 'LXDUI_LOG_FILE', 'LXDUI_CONF_DIR', 'LXDUI_CONF_FILE']
# kv = os.environ.keys()
# for k in kv:
#     print(k)

env = ['PATH']
for ev in env:
    print(ev, ' = ', os.environ.get(ev))