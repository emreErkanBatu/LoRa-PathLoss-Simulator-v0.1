# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:15:31 2024

@author: emree
"""

import pandas as pd
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
current_directory = os.getcwd()+'/'

df = pd.read_csv("Env3_Err.csv")

L3Err = df['L3Err'].tolist()
L5Err = df['L5Err'].tolist()
L9Err = df['L9Err'].tolist()


L3ErrMean=round((sum(L3Err)/len(L3Err)),1)
L3ErrMax=max(L3Err)

L5ErrMean=round((sum(L5Err)/len(L5Err)),1)
L5ErrMax=max(L5Err)

L9ErrMean=round((sum(L9Err)/len(L9Err)),1)
L9ErrMax=max(L9Err)

from matplotlib import pyplot as plt
import seaborn as sns

aa=[x for x in range(len(L3Err))]
# plt.figure(figsize=(8,4))

plt.figure(figsize=(12,5)) 

F = plt.gcf()

# Now check everything with the defaults:
DPI = F.get_dpi()
print(DPI)
plt.plot(aa, L3Err, 'r', label="L3-L5-L8", linewidth=1)
plt.plot(aa, L5Err, 'y', label="L1-L3-L5-L7-L9", linewidth=1)
plt.plot(aa, L9Err, 'c', label="L1-L2-L3-L4-L5-L6-L7-L8-L9", linewidth=1)
plt.tick_params(left=False, labelleft=True) #remove ticks

# legend = plt.legend(loc='lower right', shadow=False, fontsize='large')

plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.5), loc="lower right", borderaxespad=0, ncol=8,fontsize=15)
# plt.legend.get_frame().set_facecolor('C0')

plt.tight_layout()
# sns.despine(top=True)
plt.subplots_adjust(left=0.07)
plt.ylabel('Error (m)', size=15)
plt.xlabel('Locations', size=15)
plt.title  ('Environment-3\n\n', size=20)



# plt.legend(fontsize=15)

F.tight_layout()

F.savefig("Env3_Err.png", dpi = (200))
plt.show();
