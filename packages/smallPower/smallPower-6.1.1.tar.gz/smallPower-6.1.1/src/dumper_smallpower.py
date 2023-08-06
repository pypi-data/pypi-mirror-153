#!/bin/python
import smallpower.smallPower as smallPower
from smallpower import conf
log_file = conf.LOG_FOLDER + '/dumper_smallPower.log'

dumperSmallPower = smallPower.SmallPower_dumper(log_file_name=log_file)
dumperSmallPower.start_dumping()
# dumperSmallPower.park_database()
