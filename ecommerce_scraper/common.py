from random import random
from time import sleep
from constants import *


def _random_delay():
    if random.random() > 0.5:
        sleep(abs(random.gauss(DELAY_MEAN, DELAY_STD)) * random.uniform(0.5,1.5))
    else:
        sleep(abs(random.gauss(DELAY_MEAN, DELAY_STD)) + random.random())