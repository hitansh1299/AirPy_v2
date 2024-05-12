import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

fig = plt.figure(figsize=(16,10))

gs = fig.add_gridspec(2,8)

ax1 = fig.add_subplot(gs[0:1, 0:4])
ax2 = fig.add_subplot(gs[0:1, 4:8])
ax3 = fig.add_subplot(gs[1:2, 0:3])
ax4 = fig.add_subplot(gs[1:2, 3:6])
ax5 = fig.add_subplot(gs[1:2, 6:8])
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=1.7,
                    hspace=0.2)


sites_master = pd.read_csv(r"CPCB_Issues\AirPy_v2\sites_master.csv")
count_var = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_count_all.csv")
count_var['org'] = pd.merge(count_var, sites_master, on='site_id', how='left')['org']
count_var['org'] = np.where(count_var['org'] == 'CPCB','CPCB','NOT CPCB')
t = count_var

lst = ['NO', 'NO2', 'NOx', 'Ozone',  'PM25', 'PM10']
for name in lst:
#     t = t[(t[name+'_clean'] != 0)]
    t.replace(0, np.nan, inplace=True)
    consecutives_copy =  t[name + '_consecutives'].copy(deep=True)
    t[name + '_consecutives'] = ((t[name] - consecutives_copy)/t[name])*100
    t[name + '_outliers'] = ((consecutives_copy - t[name+'_outliers'])/t[name])*100
#     if name[:2] == 'NO':
#         per_df[name + '_unit inconsistency'] =  (df[name + '_std']-df[name + '_outliers'])*100/df[name + '_outliers']
per_df = t


melt_df_1 = per_df.melt(id_vars=['org'], value_vars=[ 'NO_consecutives', 'NO2_consecutives', 
                                                            'NOx_consecutives', 'Ozone_consecutives','PM25_consecutives',
                                                            'PM10_consecutives'])
melt_df_1 [['Pollutant','Cleaning_method']] = pd.DataFrame(melt_df_1.variable.str.split('_',1).tolist(),
                                columns = ['Pollutant','Cleaning_method'])


flierprops = dict(marker='o', markerfacecolor='red', markersize=3,  markeredgecolor='black')

sns.stripplot(ax = ax1, x = melt_df_1['Pollutant'],
            y = melt_df_1['value'],
            hue = melt_df_1['org'],
            dodge=True,s=3,linewidth=0.3
             )



plt.ylim(-2, 45)
# ax[0].set_ylim([-2,5])


ax1.legend(title = "", loc='upper right',facecolor="white",framealpha=1)
# map(lambda axi: axi.set_axis_on(), ax.ravel())
ax1.yaxis.set_tick_params(labelbottom=True)
ax1.set_xticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$',"PM" + '$_{2.5}$',  "PM" + '$_{10}$'])
ax1.set_ylabel("Consecutive repeats [%]")
ax1.set_xlabel("Pollutants")
ax1.yaxis.set_major_locator(plt.MaxNLocator(5))
#ax1.set_ylim([-2, 50])



melt_df_1 = per_df.melt(id_vars=['org'], value_vars=[ 'NO_outliers', 'NO2_outliers', 
                                                            'NOx_outliers', 'Ozone_outliers','PM25_outliers',
                                                            'PM10_outliers'])
melt_df_1 [['Pollutant','Cleaning_method']] = pd.DataFrame(melt_df_1.variable.str.split('_',1).tolist(),
                                columns = ['Pollutant','Cleaning_method'])


flierprops = dict(marker='o', markerfacecolor='red', markersize=3,  markeredgecolor='black')

sns.stripplot(ax = ax2, 
            x = melt_df_1['Pollutant'],
            y = melt_df_1['value'],
            hue = melt_df_1['org'],
            dodge=True,s=3,linewidth=0.3
            )


plt.ylim(-2, 45)
# ax[0].set_ylim([-2,5])


ax2.legend(title = "", loc='upper right',facecolor="white",framealpha=1)
# map(lambda axi: axi.set_axis_on(), ax.ravel())
ax2.yaxis.set_tick_params(labelbottom=True)
ax2.set_xticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$',"PM" + '$_{2.5}$',  "PM" + '$_{10}$'])
ax2.set_ylabel("Outliers [%]")
ax2.set_xlabel("Pollutants")
ax2.yaxis.set_major_locator(plt.MaxNLocator(5))

#ax1.get_legend().remove()
#ax2.get_legend().remove()
# ax1.set_ylim([-2, 50])

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=2.2,
                    hspace=0.3)


# fig.savefig('Figure_S_consecutive_and_outliers_2019_2021.png', dpi=1200, bbox_inches="tight")
#############


count_var = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean_all.csv")
count_var['org'] = pd.merge(count_var, sites_master, on='site_id', how='left')['org']
count_var['org'] = np.where(count_var['org'] == 'CPCB', 'CPCB', 'NOT CPCB')
t = count_var
df = count_var


lst = ['NO', 'NO2', 'NOx', 'Ozone', 'PM25', 'PM10']
for name in lst:
    # t[name + '_consecutives'] = (t[name] - t[name+'_clean'])*100/t[name]
    # t[name + '_outliers'] = (t[name+'_outliers'] - t[name+'_clean'])*100/t[name+'_clean']
    consecutives_copy =  t[name + '_consecutives'].copy(deep=True)  
    t[name + '_consecutives'] = (t[name] - t[name + '_consecutives'])*100/t[name]
    t[name + '_outliers'] = (t[name] - t[name+'_outliers'])*100/t[name]

    if name[:2] == 'NO':
        per_df[name + '_Unit inconsistency'] =  (df[name]-df[name + '_outliers'])/df[name + '_outliers']*100
per_df = t

melt_df_1 = per_df.melt(id_vars=['org'], value_vars=[ 'NO_consecutives', 'NO2_consecutives', 
                                                            'NOx_consecutives', 'Ozone_consecutives','PM25_consecutives',
                                                            'PM10_consecutives'])
melt_df_1 [['Pollutant','Cleaning_method']] = pd.DataFrame(melt_df_1.variable.str.split('_',1).tolist(),
                                columns = ['Pollutant','Cleaning_method'])


flierprops = dict(marker='o', markerfacecolor='red', markersize=3,  markeredgecolor='black')

sns.stripplot(ax = ax3, x = melt_df_1['Pollutant'],
            y = melt_df_1['value'],
            hue = melt_df_1['org'],
            dodge=True,s=3,linewidth=0.3
            )


# plt.ylim(-2, 45)
# ax[0].set_ylim([-2,5])


ax3.legend(title = "", loc='upper right',facecolor="white",framealpha=1)
# map(lambda axi: axi.set_axis_on(), ax.ravel())
ax3.yaxis.set_tick_params(labelbottom=True)
ax3.set_xticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$',"PM" + '$_{2.5}$',  "PM" + '$_{10}$'])
ax3.set_ylabel("Relative change in " + "\n"+"annual mean [%]")
ax3.set_xlabel("Pollutants")
ax3.yaxis.set_major_locator(plt.MaxNLocator(5))
# ax3.set_ylim([-2, 50])
# ax[0].legend(loc='upper right',framealpha =1, fancybox = False)




melt_df_1 = per_df.melt(id_vars=['org'], value_vars=[ 'NO_outliers', 'NO2_outliers', 
                                                            'NOx_outliers', 'Ozone_outliers','PM25_outliers',
                                                            'PM10_outliers'])
melt_df_1 [['Pollutant','Cleaning_method']] = pd.DataFrame(melt_df_1.variable.str.split('_',1).tolist(),
                                columns = ['Pollutant','Cleaning_method'])


flierprops = dict(marker='o', markerfacecolor='red', markersize=3,  markeredgecolor='black')

sns.stripplot(ax = ax4, x = melt_df_1['Pollutant'],
            y = melt_df_1['value'],
            hue = melt_df_1['org'],
            dodge=True,s=3,linewidth=0.3
            )


#plt.ylim(-2, 45)
# ax[0].set_ylim([-2,5])


ax4.legend(title = "", loc='upper right',facecolor="white",framealpha=1)
# map(lambda axi: axi.set_axis_on(), ax.ravel())
ax4.yaxis.set_tick_params(labelbottom=True)
ax4.set_xticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$',"PM" + '$_{2.5}$',  "PM" + '$_{10}$'])
ax4.set_ylabel("Outliers [%]")
ax4.set_xlabel("Pollutants")
ax4.yaxis.set_major_locator(plt.MaxNLocator(5))
# ax4.set_ylim([2, 25])
# ax[0].legend(loc='upper right',framealpha =1, fancybox = False)



from matplotlib.patches import Rectangle
# rectangle = plt.Rectangle((0,0), 50, 20, fc='blue',ec="red",axis = inset_ax1)

# ax[0].set_ylim([-2,60])

ax3.get_legend().remove()
ax4.get_legend().remove()

# ax3.set_ylim([-5,30])
# ax4.set_ylim([-15,35])



#================================


#========================
per_df = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean_all.csv")
per_df['org'] = pd.merge(per_df, sites_master, on='site_id', how='left')['org']
per_df['org'] = np.where(per_df['org'] == 'CPCB', 'CPCB','NOT CPCB')
for name in ['NO', 'NO2', 'NOx']:
    per_df[name + '_Unit inconsistency'] =  (per_df[name] - per_df[name + '_outliers'])*100/per_df[name]
melt_df_1 = per_df.melt(id_vars=['org'], value_vars=[ 'NO_Unit inconsistency', 'NO2_Unit inconsistency', 
                                                            'NOx_Unit inconsistency'])
melt_df_1 [['Pollutant','Cleaning_method']] = pd.DataFrame(melt_df_1.variable.str.split('_',1).tolist(),
                                columns = ['Pollutant','Cleaning_method'])

sns.stripplot(ax = ax5, x = melt_df_1['Pollutant'],
            y = melt_df_1['value'],
            hue = melt_df_1['org'],
            dodge=True,s=3,linewidth=0.3
            )




ax5.legend(title = "", loc='upper right',facecolor="white",framealpha=1)
# map(lambda axi: axi.set_axis_on(), ax.ravel())
ax5.yaxis.set_tick_params(labelbottom=True)
ax5.set_xticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$'])
ax5.set_ylabel("Outliers [%]")
ax5.set_xlabel("Pollutants")
ax5.yaxis.set_major_locator(plt.MaxNLocator(5))
# ax[0].legend(loc='upper right',framealpha =1, fancybox = False)


ax5.get_legend().remove()



# t = plt.text(0.5, 0.5, 'text', transform=ax.transAxes, fontsize=30)
# t.set_bbox(dict(facecolor='white', alpha=0.5, edgecolor='red'))

# plt.text(.01, .94, ' (c)', ha='left', va='top', transform=ax3.transAxes,  backgroundcolor = 'none')
# plt.text(.01, .94, ' (d) ', ha='left', va='top',transform=ax4.transAxes, backgroundcolor = 'none')
# plt.text(.01, .94, ' (e) ', ha='left', va='top',transform=ax5.transAxes,backgroundcolor = 'none')

# ax[0].get_yaxis().set_visible(False)
# ax[1].get_yaxis().set_visible(False)
# ax[2].get_yaxis().set_visible(False)

ax3.set_ylabel("Relative change in annual mean [%]")
ax4.set_ylabel("")
ax5.set_ylabel("")


plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=1.7,
                    hspace=0.18)

ax1.set_xlabel("")
ax2.set_xlabel("")
ax3.set_xlabel("")
ax4.set_xlabel("")
ax5.set_xlabel("")
fig.suptitle('(B) With outliers ', fontsize=14)

#ax1.set_ylim([-2, 105])
# ax2.set_ylim([-2, 60])
ax3.set_ylim([-85, 100])
ax4.set_ylim([-60, 70])
# ax5.set_ylim([-50, 150])

plt.text(.03, .96, '(h) Consecutive repeats', ha='left', va='top', transform=ax3.transAxes,  backgroundcolor = 'none')
plt.text(.03, .96, '(i)          Outliers', ha='left', va='top',transform=ax4.transAxes, backgroundcolor = 'none')
plt.text(.03, .96, '(j)      Unit' + "\n" + ' Inconsistency', ha='left', va='top',transform=ax5.transAxes, backgroundcolor = 'none')
plt.text(.03, .96, ' (f)', ha='left', va='top', transform=ax1.transAxes, backgroundcolor = 'white')
plt.text(.03, .96, ' (g)', ha='left', va='top',transform=ax2.transAxes, backgroundcolor = 'white')

ax3.set_ylabel("Relative change in" + "\n"+"annual mean [%]")

fig.savefig('stripplot_consecutive_and_outliers_2019_2023_outliers.png', dpi=1200, bbox_inches="tight")

plt.show()