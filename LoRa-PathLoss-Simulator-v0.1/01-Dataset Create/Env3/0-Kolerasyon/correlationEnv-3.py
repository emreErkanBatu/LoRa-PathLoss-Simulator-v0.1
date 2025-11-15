# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 05:17:42 2024

@author: emree
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

my_df = pd.read_csv("dataSet_9L.csv")
# using seaborn
# If yoy want to the see the value also then annot=True must be added to the parameters.
f, ax = plt.subplots(figsize=(10, 8))
corr = my_df.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),
            cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax, annot=True,fmt=".2f",
            annot_kws={"size": 12}         # Hücre değerlerinin yazı boyutu
            )


plt.xticks(fontsize=12,rotation=45)
plt.yticks(fontsize=12,rotation=0)
plt.savefig("dataSet_9L_heatmap.png", dpi=300, bbox_inches="tight")



# my_df = pd.read_csv("newDataSet.csv")
# # using seaborn
# # If yoy want to the see the value also then annot=True must be added to the parameters.
# f, ax = plt.subplots(figsize=(10, 8))
# corr = my_df.corr()
# sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),
#             cmap=sns.diverging_palette(220, 10, as_cmap=True),
#             square=True, ax=ax, annot=True,
#             annot_kws={"size": 16}
#             )

# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)

# plt.savefig("heatmapNew.png", dpi=300, bbox_inches="tight")