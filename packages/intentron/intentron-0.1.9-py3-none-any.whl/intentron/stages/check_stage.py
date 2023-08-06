import json
import numpy as np
import pandas as pd
from alive_progress import alive_bar
from intentron.utils import *


def check_stage(src):
    log.info("Checking started")
    for gesture in os.listdir(src):
        for side in os.listdir(osp.join(src, gesture)):
            for trial in os.listdir(osp.join(src, gesture, side)):
                files = get_files(osp.join(src, gesture, side, trial, 'color'), 'all')
                print(len(files))
