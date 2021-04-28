import logging
import time
from collections import OrderedDict
from datetime import datetime

# Creating and configuring logger
logging.basicConfig(filename="LOGS.log",
                    format='%(asctime)s - %(levelname)s -[ %(funcName)s : %(lineno)d ]- %(message)s',
                    level=logging.INFO,
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# to compute execution time
current_time = time.time()

#to get current date and time
datetime_now = datetime.now()

# to store generated data
data_frame = OrderedDict()