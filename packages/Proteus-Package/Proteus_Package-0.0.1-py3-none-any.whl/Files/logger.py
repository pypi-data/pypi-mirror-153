# Added by Mahesh Saggam on [29-JUNE-21] To print console in a separate log file

import logging
from logging.handlers import RotatingFileHandler
# from jproperties import Properties
import os


dir = 'log'

if not os.path.exists(dir):
    os.makedirs(dir)

for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

# The below commented code will required if the configuration is defined in Properties file

# configs = Properties()
# propDetails = {}

# with open('PythonLogger.Properties', 'rb') as read_prop:
#     configs.load(read_prop)


# prop_view = configs.items()
   
# for item in prop_view:
#     propDetails[item[0]] = item[1].data

# format = propDetails['FORMAT']
# filename = propDetails['FILE_NAME']
# filemode = propDetails['FILE_MODE']
# loggerName = propDetails['LOGGER_NAME']
# maxBytes = propDetails['MAX_BYTES']
# backUpcount = propDetails['BACKUP_COUNT']

format = '%(asctime)s %(levelname)s %(name)s %(message)s'
filename = 'python_server.log'
filemode = 'w'
loggerName = '[BaseLogger]'
maxBytes = 5242880
backUpcount = 100
ibaseDebugLvl = 10

logging.basicConfig(format=format,
                     filename=dir+'/' + filename, 
                     filemode=filemode, 
                     level=logging.DEBUG)
logger = logging.getLogger(loggerName)
logHandler = RotatingFileHandler(dir+'/'+filename, maxBytes=int(maxBytes), backupCount=int(backUpcount))
logger.addHandler(logHandler)

def log(msg, debugLevel):
    if debugLevel.strip() == '':
        debugLevel = 0
    else:
        debugLevel = int(debugLevel)

    # to print normal log use debugLvl 1
    if debugLevel == 0:
        logger.debug(msg)
    
    # to print stack trace use debugLvl 9
    if debugLevel == 1:
        logger.exception(msg)
