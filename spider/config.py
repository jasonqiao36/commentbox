import os
import random

from yaml import full_load

config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')

with open(config_path, 'r') as f:
    cont = f.read()

cf = full_load(cont)


def get_crawl_interal():
    interal = random.randint(cf.get('min_crawl_interal'), cf.get('max_crawl_interal'))
    return interal
