# -*- coding: utf-8 -*-
import os

log_dir = './log'
os.makedirs(log_dir) if not os.path.exists(log_dir) else None

DATA_PATH = './data'
os.makedirs(DATA_PATH) if not os.path.exists(DATA_PATH) else None
