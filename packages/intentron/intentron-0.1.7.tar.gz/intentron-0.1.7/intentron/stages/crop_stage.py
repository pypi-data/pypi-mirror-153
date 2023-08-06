import json
import numpy as np
import pandas as pd
from alive_progress import alive_bar
from intentron.utils import *


def crop_stage(src):
    log.info("Cropping started")
    for gesture in os.listdir(src):
        for side in os.listdir(osp.join(src, gesture)):
            for trial in os.listdir(osp.join(src, gesture, side)):
                for mode in os.listdir(osp.join(src, gesture, side, trial)):
                    files = get_files(osp.join(src, gesture, side, trial, mode))[121:]
                    for file in files:
                        rm(file)
