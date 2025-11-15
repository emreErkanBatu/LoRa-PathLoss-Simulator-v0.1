# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 17:00:21 2025

@author: emree
"""

import pandas as pd
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# CSV dosyasını oku
df_history1 = pd.read_csv("dataSet_3L_Hist.csv")
df_history2 = pd.read_csv("dataSet_5L_Hist.csv")
df_history3 = pd.read_csv("dataSet_9L_Hist.csv")

# Veriyi incele
# print(df_history.head())


# def draw(xL,yL,ax,p,cVal,vVal,ok):
#     ax.annotate(str(round(yL[p],4)),fontsize=14,
#                 xy=(xL[p], yL[p]), xycoords='data',color=cVal,
#                 xytext=(-90, vVal), textcoords='offset points',
#                 bbox=dict(boxstyle="round", fc='white'),
#                 arrowprops=dict(arrowstyle="->",
#                                 connectionstyle="angle,angleA=0,angleB="+ok+",rad=10",color=cVal))

# def draw(xL, yL, ax, p, cVal, vVal, ok,sec):
#     ax.annotate(
#         str(round(yL[p], 4)),
#         fontsize=14,
#         xy=(xL[p], yL[p]), xycoords='data', color=cVal,
#         xytext=(-90, vVal), textcoords='offset points',
#         bbox=dict(boxstyle="round", fc='white'),
#         arrowprops=dict(
#             arrowstyle="->",
#             connectionstyle="angle,angleA=0,angleB=" + ok + ",rad=10",
#             color=cVal,
#             linestyle=sec   # 🔹 Kesikli çizgi eklendi
#         )
#     )

def draw(xL, yL, ax, p, cVal, vVal, ok, sec):
    # 🔹 Noktayı marker ile göster
    ax.plot(
        xL[p], yL[p],
        marker='o',              # Daire marker
        markersize=7,            # Boyut
        color=cVal,              # Renk
        markeredgecolor='black', # Dış hat kontrastı
        zorder=5
    )

    # 🔹 Etiketi ve oku çiz
    ax.annotate(
        str(round(yL[p], 4)),
        fontsize=14,
        xy=(xL[p], yL[p]), xycoords='data', color=cVal,
        xytext=(-90, vVal), textcoords='offset points',
        bbox=dict(boxstyle="round", fc='white', ec=cVal, lw=0.8),
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle=f"angle,angleA=0,angleB={ok},rad=10",
            color=cVal,
            linestyle=sec,       # Kesikli veya düz
            lw=1.5
        )
    )



# Örneğin loss grafiği
import matplotlib.pyplot as plt


plt.figure(figsize=(12,5)) 
F = plt.gcf()
DPI = F.get_dpi()
print(DPI)




# 🔹 Mevcut ekseni al
ax = plt.gca()

# 🔹 Eksen merkezine yazı ekle
plt.text(
    0.5, 0.7, "Environment-1",
    fontsize=30,
    color='gray',
    alpha=0.3,
    ha='center', va='center',
    transform=ax.transAxes,  # eksen koordinat sistemi
    fontweight='bold'
)


plt.plot(df_history1["loss"],linestyle='-', color='#1f77b4')
plt.plot(df_history1["val_loss"],linestyle='--', color='#1f77b4')

plt.plot(df_history2["loss"],linestyle='-', color='#ff7f0e')
plt.plot(df_history2["val_loss"],linestyle='--', color='#ff7f0e')

plt.plot(df_history3["loss"],linestyle='-', color='#2ca02c')
plt.plot(df_history3["val_loss"],linestyle='--', color='#2ca02c')



plt.xlabel('Epoch', fontsize=16)
plt.ylabel('Total Loss', fontsize=16)

plt.grid(True) 



plt.legend(['Model-1_Train', 'Model-1_Val','Model-2_Train', 'Model-2_Val','Model-3_Train', 'Model-3_Val'],bbox_to_anchor=(0, 1.02, 1, 0.5), loc="lower right", borderaxespad=0, ncol=8,fontsize=10)
# plt.legend(['train', 'val'], loc='upper left')


# Epoch sayısı
epochs = range(1, len(df_history1["loss"]) + 1)
draw(epochs,df_history1["loss"],plt,len(df_history1["loss"])-2,'#1f77b4',30,"110",'-')
draw(epochs,df_history1["val_loss"],plt,len(df_history1["val_loss"])-2,'#1f77b4',60,"90",'--')

epochs = range(1, len(df_history2["loss"]) + 1)
draw(epochs,df_history2["loss"],plt,len(df_history2["loss"])-2,'#ff7f0e',30,"110",'-')
draw(epochs,df_history2["val_loss"],plt,len(df_history2["val_loss"])-2,'#ff7f0e',60,"90",'--')

epochs = range(1, len(df_history3["loss"]) + 1)
draw(epochs,df_history3["loss"],plt,len(df_history3["loss"])-2,'#2ca02c',30,"110",'-')
draw(epochs,df_history3["val_loss"],plt,len(df_history3["val_loss"])-2,'#2ca02c',60,"90",'--')

plt.show()

F.tight_layout()

F.savefig("Comp_Loss.png", dpi = (200))


