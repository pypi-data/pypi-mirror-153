import json
import numpy as np
import pandas as pd
from alive_progress import alive_bar
from intentron.utils import *


def fuse_stage(src, dst):
    nl = get_lines(src)
    rows_2drgb = []
    rows_3drgb = []
    labels = []
    if osp.exists(dst):
        log.info("Fusing is done")
    else:
        log.info("Fusing started")
        touch(dst)
        files = enum_files(src, ['json', 'csv'])

        with alive_bar(len(files), theme='classic') as bar:
            for i, json_file, csv_file in files:
                bar()
                info = json.load(open(json_file))
                if info['is_valid']:
                    labels += [info['label']]
                    df_2drgb = pd.read_csv(csv_file)
                    df_3drgb = pd.read_csv(csv_file)

                    cols_2drgb = list(filter(lambda a: '__z' not in a and 'world' not in a, df_2drgb.columns.tolist()))
                    df_2drgb = padded(df_2drgb.filter(cols_2drgb), nl)
                    row_2drgb = np.reshape(df_2drgb.to_numpy(), -1)
                    rows_2drgb += [row_2drgb]

                    cols_3drgb = list(filter(lambda a: 'world' not in a, df_3drgb.columns.tolist()))
                    df_3drgb = padded(df_3drgb.filter(cols_3drgb), nl)
                    row_3drgb = np.reshape(df_3drgb.to_numpy(), -1)
                    rows_3drgb += [row_3drgb]

        df_2drgb = pd.DataFrame(np.row_stack(rows_2drgb))
        df_3drgb = pd.DataFrame(np.row_stack(rows_3drgb))
        nf_2drgb = int(len(df_2drgb.columns)/len(cols_2drgb))
        nf_3drgb = int(len(df_3drgb.columns)/len(cols_3drgb))
        df_2drgb['label'] = labels
        df_3drgb['label'] = labels
        header_2drgb = [f'{c}_{i}' for i, c in enumerate(cols_2drgb * nf_2drgb)] + ['label']
        header_3drgb = [f'{c}_{i}' for i, c in enumerate(cols_3drgb * nf_3drgb)] + ['label']
        df_2drgb.to_csv(osp.join(dst, f'samples-2drgb.csv'), header=header_2drgb, index=False)
        df_3drgb.to_csv(osp.join(dst, f'samples-3drgb.csv'), header=header_3drgb, index=False)
