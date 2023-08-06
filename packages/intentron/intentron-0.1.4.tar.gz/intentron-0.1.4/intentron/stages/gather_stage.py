import json
import numpy as np
import pandas as pd
from alive_progress import alive_bar
from intentron.utils import *


def gather_stage(src, dst):
    if osp.exists(dst):
        log.info("Gathering is done")
    else:
        log.info("Gathering started")
        # touch(dst)
        # files = enum_files(src, ['json', 'csv'])
        mode2files = {}
        for folder in os.listdir(src):
            if folder.endswith('-fused'):
                for file in get_files(osp.join(src, folder), 'csv'):
                    name = osp.basename(file)
                    mode = name[name.index('-')+1:name.index('.')]
                    if mode in mode2files:
                        mode2files[mode] += [file]
                    else:
                        mode2files[mode] = [file]

        for mode, files in mode2files.items():
            for file in files:
                df = pd.read_csv(file)
                print(df.head())


