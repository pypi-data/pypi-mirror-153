'''Nawah is rapid app development framework'''

import logging
import os

logger = logging.getLogger('nawah')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)

__version__ = '0.0.0'
with open(
    os.path.join(os.path.dirname(__file__), 'version.txt'), encoding='UTF-8'
) as f:
    __version__ = f.read().strip()
