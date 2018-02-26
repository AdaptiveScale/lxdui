from api.src.lib import log as logger, conf
import __metadata__ as m
import pathlib
import logging
import os
log = logging.getLogger(__name__)

# Enable logging
l = logger.Log(__name__)
# l.file = '/Users/vetoni/PycharmProjects/lxdui/conf/lxdui.log'

c = conf.Config(conf='/Users/vetoni/PycharmProjects/lxdui/conf/lxdui.conf')
# c.show()
c.setEnv()
c.showEnv()
k, i = c.getEnv()
print(k)
print(i)
