import seaborn  as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

def plot_outlier_heatmap(monthly_condensed_summary: str, savefile: str):
    pols = ['NO', 'NO2', 'NOx', 'Ozone', 'PM10', 'PM25']
    net = pd.read_csv(monthly_condensed_summary)
    melts = pd.DataFrame(columns=['year','month','pol','repeats'])
    for pol in pols:
        net[pol] = (net[pol + '_consecutives'] - net[pol + '_outliers'])/net[pol + '_consecutives'] * 100
        # temp = net.groupby(['year','month'])
        temp = net.melt(id_vars=['year','month'], value_vars=[pol], var_name='pol', value_name='repeats')
        # print(temp.columns)
        melts = pd.concat([melts,temp], axis=0)
    print(melts)
    net = melts

    matplotlib.rcParams.update({'font.size': 11, "font.family": "Arial"})
    matplotlib.rcParams['legend.handlelength'] = 1
    matplotlib.rcParams['legend.handleheight'] = 1
    params = {'mathtext.default': 'regular' }         
    sns.set_style({'font.family':'sans-serif', 'font.serif':'Arial','font.size': 11})
    plt.rcParams.update(params)

    f,(ax1,ax2,ax3,ax4,ax5,axcb) = plt.subplots(1,6, figsize=(25,3),
                gridspec_kw={'width_ratios':[1,1,1,1,1,0.08]})
    ax1.get_shared_y_axes().join(ax2,ax3,ax4,ax5)

    net1 = net[(net['year'] == 2019)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g1 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax1,annot=True,fmt='.1f',annot_kws={"fontsize":7.7})
    g1.set_ylabel('Pollutant')
    g1.set_xlabel('')

    net1 = net[(net['year'] == 2020)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g2 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax2,annot=True,fmt='.1f',annot_kws={"fontsize":7.5})
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_yticks([])


    net1 = net[(net['year'] == 2021)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g3 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax3,annot=True,fmt='.1f',annot_kws={"fontsize":7.5})
    g3.set_ylabel('')
    g3.set_xlabel('')
    g3.set_yticks([])

    net1 = net[(net['year'] == 2022)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g4 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax4,annot=True,fmt='.1f',annot_kws={"fontsize":7.5})
    g4.set_ylabel('')
    g4.set_xlabel('')
    g4.set_yticks([])

    net1 = net[(net['year'] == 2023)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g5 = sns.heatmap(heatmap_data,cmap="jet",ax=ax5, cbar_ax=axcb,annot=True,fmt='.1f',annot_kws={"fontsize":7.5},cbar_kws={'label': 'Outliers [%]'})
    g5.set_xlabel('')
    g5.set_ylabel('')
    g5.set_yticks([])


    # may be needed to rotate the ticklabels correctly:
    for ax in [g1,g2,g3,g4,g5]:
        tl = ax.get_xticklabels()
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
        tly = ax.get_yticklabels()
        ax.set_yticklabels(tly, rotation=0)

        
    ax1.set_title("2019")
    ax2.set_title("2020")
    ax3.set_title('2021')
    ax4.set_title('2022')
    ax5.set_title('2023')
    g2.set_xlabel('Months')
    matplotlib.rcParams.update({'font.size': 11, "font.family": "Arial"})
    matplotlib.rcParams['legend.handlelength'] = 1
    matplotlib.rcParams['legend.handleheight'] = 1
    params = {'mathtext.default': 'regular' }         
    sns.set_style({'font.family':'sans-serif', 'font.serif':'Arial','font.size': 11})
    plt.rcParams.update(params)


    g1.set_yticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$',"PM" + '$_{10}$', "PM" + '$_{2.5}$'])
    plt.text(.005, 1.09, ' (f)', ha='left', va='top', transform=ax1.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (g)', ha='left', va='top', transform=ax2.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (h)', ha='left', va='top', transform=ax3.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (i)', ha='left', va='top', transform=ax4.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (j)', ha='left', va='top', transform=ax5.transAxes, size= 11, backgroundcolor = 'none')

    plt.show()
    f.savefig(savefile, dpi=1200, bbox_inches="tight")


def plot_consecutives_heatmap(monthly_condensed_summary: str, savefile: str):
    pols = ['NO', 'NO2', 'NOx', 'Ozone', 'PM10', 'PM25']
    net = pd.read_csv(monthly_condensed_summary)
    melts = pd.DataFrame(columns=['year','month','pol','repeats'])
    for pol in pols:
        net[pol] = (net[pol] - net[pol + '_consecutives'])/net[pol] * 100
        # temp = net.groupby(['year','month'])
        temp = net.melt(id_vars=['year','month'], value_vars=[pol], var_name='pol', value_name='repeats')
        # print(temp.columns)
        melts = pd.concat([melts,temp], axis=0)
    print(melts)
    net = melts

    matplotlib.rcParams.update({'font.size': 11, "font.family": "Arial"})
    matplotlib.rcParams['legend.handlelength'] = 1
    matplotlib.rcParams['legend.handleheight'] = 1
    params = {'mathtext.default': 'regular' }         
    sns.set_style({'font.family':'sans-serif', 'font.serif':'Arial','font.size': 11})
    plt.rcParams.update(params)

    f,(ax1,ax2,ax3,ax4,ax5,axcb) = plt.subplots(1,6, figsize=(25,3),
                gridspec_kw={'width_ratios':[1,1,1,1,1,0.08]})
    ax1.get_shared_y_axes().join(ax2,ax3,ax4,ax5)

    net1 = net[(net['year'] == 2019)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g1 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax1,annot=True,fmt='.1f',annot_kws={"fontsize":7.7})
    g1.set_ylabel('Pollutant')
    g1.set_xlabel('')

    net1 = net[(net['year'] == 2020)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g2 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax2,annot=True,fmt='.1f',annot_kws={"fontsize":7.5})
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_yticks([])


    net1 = net[(net['year'] == 2021)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g3 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax3,annot=True,fmt='.1f',annot_kws={"fontsize":7.5})
    g3.set_ylabel('')
    g3.set_xlabel('')
    g3.set_yticks([])

    net1 = net[(net['year'] == 2022)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g4 = sns.heatmap(heatmap_data,cmap="jet",cbar=False,ax=ax4,annot=True,fmt='.1f',annot_kws={"fontsize":7.5})
    g4.set_ylabel('')
    g4.set_xlabel('')
    g4.set_yticks([])

    net1 = net[(net['year'] == 2023)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g5 = sns.heatmap(heatmap_data,cmap="jet",ax=ax5, cbar_ax=axcb,annot=True,fmt='.1f',annot_kws={"fontsize":7.5},cbar_kws={'label': 'Similar Repeats [%]'})
    g5.set_xlabel('')
    g5.set_ylabel('')
    g5.set_yticks([])


    # may be needed to rotate the ticklabels correctly:
    for ax in [g1,g2,g3,g4,g5]:
        tl = ax.get_xticklabels()
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
        tly = ax.get_yticklabels()
        ax.set_yticklabels(tly, rotation=0)

        
    ax1.set_title("2019")
    ax2.set_title("2020")
    ax3.set_title('2021')
    ax4.set_title('2022')
    ax5.set_title('2023')
    g2.set_xlabel('Months')
    matplotlib.rcParams.update({'font.size': 11, "font.family": "Arial"})
    matplotlib.rcParams['legend.handlelength'] = 1
    matplotlib.rcParams['legend.handleheight'] = 1
    params = {'mathtext.default': 'regular' }         
    sns.set_style({'font.family':'sans-serif', 'font.serif':'Arial','font.size': 11})
    plt.rcParams.update(params)


    g1.set_yticklabels(["NO","NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$',"PM" + '$_{10}$', "PM" + '$_{2.5}$'])
    plt.text(.005, 1.09, ' (a)', ha='left', va='top', transform=ax1.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (b)', ha='left', va='top', transform=ax2.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (c)', ha='left', va='top', transform=ax3.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (d)', ha='left', va='top', transform=ax4.transAxes, size= 11, backgroundcolor = 'none')
    plt.text(.005, 1.09, ' (e)', ha='left', va='top', transform=ax5.transAxes, size= 11, backgroundcolor = 'none')

    plt.show()
    f.savefig(savefile, dpi=1200, bbox_inches="tight")
if __name__ == '__main__':
    plot_outlier_heatmap(r'CPCB_Issues/AirPy_v2/new_data/summary/monthly_condensed.csv', 
                         'outliers_monthly_heatmap.png')
    plot_consecutives_heatmap(r'CPCB_Issues/AirPy_v2/new_data/summary/monthly_condensed.csv',
                                'consecutives_monthly_heatmap.png')