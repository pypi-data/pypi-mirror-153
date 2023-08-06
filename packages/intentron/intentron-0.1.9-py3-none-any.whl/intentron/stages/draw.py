import numpy as np
import pandas as pd
from alive_progress import alive_bar
from intentron.utils import *
from intentron.utils.fmt import pp_matrix
import matplotlib.pyplot as plt
import seaborn as sn


def draw_job(src, dst):
    touch(dst)
    files = get_files(src, 'csv')
    cmap = "PuRd"
    for file in files:
        arr = pd.read_csv(file).to_numpy()
        name = osp.basename(osp.splitext(file)[0]) + '.png'
        df = pd.DataFrame(arr)
        plt.figure(figsize=(20, 15))
        res = sn.heatmap(
            df.T,
            annot=True,
            cmap="Paired",
            cbar=False,
            vmax=10,
            vmin=0,
            linewidth=0.01,
            linecolor="#222",
        )
        plt.savefig(osp.join(dst, name), bbox_inches='tight', dpi=400)

