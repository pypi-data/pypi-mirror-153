import numpy as np
import pandas as pd
from intentron.utils.fmt import pp_matrix

array = np.array(
    [
        [13, 0, 1, 0, 2, 0],
        [0, 50, 2, 0, 10, 0],
        [0, 13, 16, 0, 0, 3],
        [0, 0, 0, 13, 1, 0],
        [0, 40, 0, 1, 15, 0],
        [0, 0, 0, 0, 0, 20],
    ]
)

# get pandas dataframe
df_cm = pd.DataFrame(array, index=range(1, 7), columns=range(1, 7))
# colormap: see this and choose your more dear
cmap = "PuRd"
m = pp_matrix(df_cm, cmap=cmap)
print(type(m))

# import numpy as np
#
# from intentron.utils.fmt import pp_matrix, pp_matrix_from_data
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# df = sns.load_dataset('iris')
# sns_plot = sns.pairplot
#     sns.pairplot(df, hue='species', height=2.5)
# plt.savefig('output.png')
#
# y_test = np.array([1, 2, 3, 4, 5])
# predic = np.array([3, 2, 4, 3, 5])
#
# pp_matrix_from_data(y_test, predic, cmap="PuBu_r", path='/home/dm/Work/image.png')
