import pandas as pd
import numpy as np
from intentron.utils import *
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def get_metrics(folder):
    output = 0
    '''
    n = max([len(open(file).read()) for file in get_files(folder, 'csv')])
    ms = []
    for file in get_files(folder, 'csv'):
        df = pd.read_csv(file)
        total = len(df) / 3
        points = len(df.iloc[0])
        empty = df.isnull().values.sum() / 3
        m = round(100 * empty / (total * points), 2)
        ms += [m]
    x = [1, 2, 3, 4, 5]
    y = [1, 5, 4, 7, 4]

    sns.lineplot(range(len(ms)), ms)
    plt.savefig('/home/dm/Work/missing.png', dpi=700)
    print(ms)
    print(len(ms))
    return output
    '''


def estimate_job(src, dst):
    get_metrics(src)