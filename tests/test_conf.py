from api.src.lib import log as logger, conf
import pathlib
import logging
log = logging.getLogger(__name__)

# Enable logging
l = logger.Log(__name__)
# l.file = '/Users/vetoni/PycharmProjects/lxdui/conf/lxdui.log'

c = conf.Config()
c.show()
