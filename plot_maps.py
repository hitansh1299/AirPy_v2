import matplotlib.colors
import cmasher as cmr
from matplotlib import cm 
import numpy as np
import geopandas as gpd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# %matplotlib notebook
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
from matplotlib import cm 
import numpy as np
import geopandas as gpd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# %matplotlib notebook
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from math import ceil, floor
geodf = gpd.read_file("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")

fig, axs = plt.subplots(2, 2,figsize=(7,9),sharey=True,sharex=True)

for axes in axs:
    for axis in axes:
        geodf.plot(ax=axis, color='white', linewidth=.4,edgecolor='#545454')
#         axis.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        axis.set_xticklabels([])
        axis.set_yticklabels([])
        axis.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        axis.axis('off')

        axis.annotate('wwwwwwwwww' + '\n'   +
                          'wwwwwwwwww' + '\n', xy=(90,11),ha="center", va="center", color='white', fontsize=9,
                bbox=dict(boxstyle='square', facecolor='white', edgecolor='white',lw=0.4))
# for a in ax:


plt.subplots_adjust(wspace=0, hspace=0)

normalize = lambda x: x / x.abs().max()

def plot_all(ax, df,colorbar):
    CONST = 0.5
    #print(df.columns)
    temp = df[(df[pol+'_DA']<75) | (df[pol+'_DA'] == np.nan) | (df[pol] == np.nan) | (df[pol + suffix[idx]] == 1)]
    ax.scatter(temp['lon'], temp['lat'], label=None, c= '#808080', 
                               edgecolors='#808080', 
                               s=10, linewidth=0.1, alpha=1) # Plot all gray sites
    
    temp = df[df[pol+'_DA']>75]
    z1_plot = ax.scatter(temp['lon'], temp['lat'], label=None, c= temp['Percentage_change'], 
                               cmap=cmap, 
                               vmin = 0, 
                               vmax = int(ceil(temp['Percentage_change'].max())),
                               edgecolors='#c0c0c0', 
                               s=temp['NO2 _after_Cleaning_mass_conc']*CONST, linewidth=0.1, alpha=1)
    if colorbar == True: 
        cbaxes = inset_axes(ax, width="30%", height="3%",loc='lower right',
                            bbox_to_anchor=(-0.13,0.14,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes) 
        
        
        cbar = plt.colorbar(z1_plot, cbaxes,orientation='horizontal', 
                            ticks = np.linspace(0,int(ceil(temp['Percentage_change'].max())), 5).round(1),
                            # ticks=[0, 20, 40, 60, 80, 100]
                            shrink = 1)
        cbar.dividers.set_linewidth(0.4)
#         cbaxes.set_label
        cbaxes.set_title("Change in annual mean "+  pol + ' [%]', fontsize = 5.5)


        cbaxes.tick_params(labelsize=6,width = 0.4)
        cbar.outline.set_linewidth(0.4)
        
        for area in [10, 30, 50]:
            ax.scatter([], [], c='k', alpha=1, s=area,
                        label = area)
        ax.legend(scatterpoints=1, frameon=False,loc="upper right",
                  labelspacing=0.5, title='Annual mean'+"\n"+
                                          '    [µg m' + '$^{-3}$' + ']',
                  prop={'size': 6}, bbox_to_anchor =(0.89, 0.99), ncol = 1).get_title().set_fontsize('6')



    # temp = df[df['Percentage_change'] > 100]
    # ax.scatter(temp['lon'], temp['lat'], label=None, c= '#800000', s=temp['NO2 _after_Cleaning_mass_conc']*CONST, linewidth=0, alpha=1)
    # temp = df[df['Percentage_change'] < -5]
    # ax.scatter(temp['lon'], temp['lat'], label=None, c= '#00008B', s=temp['NO2 _after_Cleaning_mass_conc']*CONST, linewidth=0, alpha=1)

    temp = df[df[pol+'_DA']>75]
    temp = temp[temp['Complaince_change'] == 1]

    z1_plot = ax.scatter(temp['lon'], temp['lat'], label=None, c= temp['Percentage_change'], 
                               cmap=cmap, 
                            #    vmax=100,
                               edgecolors='black', 
                            #    vmin = -20, 
                               s=temp['NO2 _after_Cleaning_mass_conc']*CONST, linewidth=0.5, alpha=1)
    

    temp1 = temp[temp['Percentage_change'] > 100]
#     print(temp)
    ax.scatter(temp1['lon'], temp1['lat'], label=None, c= '#800000', s=temp1['NO2 _after_Cleaning_mass_conc']*CONST, 
               linewidth=0.5, alpha=1, edgecolors='black')
    temp2 = temp[temp['Percentage_change'] < -5]
    ax.scatter(temp2['lon'], temp2['lat'], label=None, c= '#00008B', s=temp2['NO2 _after_Cleaning_mass_conc']*CONST, 
               linewidth=0.5, alpha=1, edgecolors='black')
    
#==========================================================
#=========================================================
year = 2021
pollutants = ['PM25', 'PM10', 'NO2', 'Ozone']
# pollutants = ['NO2']
suffix = ['_clean','_clean','_CPCB','_clean']
axes = [(0,0), (0,1), (1,0), (1,1)]

for idx, pollutant in enumerate(pollutants):

    df = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean.csv")
    count_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_count.csv")
    sites_master = pd.read_csv(r"CPCB_Issues\AirPy_v2\sites_master.csv")
    df = df[df['year'] == year]
    pol = pollutant
    df[pol+'_DA'] = (count_summary[pol+'_clean']/count_summary['timestamp']) * 100
    df['lat'] = df['site_id'].map(sites_master.set_index('site_id')['latitude'])
    df['lon'] = df['site_id'].map(sites_master.set_index('site_id')['longitude'])
    df = df [[pol, pol+suffix[idx], 'site_name', 'lat' , 'lon', pol+'_DA']].copy()


    df['Percentage_change'] = (df[pol + suffix[idx]]-df[pol]).abs()*100/df[pol]
    df['before_com'] = np.where(df[pol] > 40,1 , 0)
    df['after_com'] = np.where(df[pol + suffix[idx]] > 40,1 , 0)
    df['Complaince_change'] = np.where(df['before_com'] == df['after_com'],0,1)
    df['NO2 _before_cleaning_mass_conc'] = df[pol]
    df['NO2 _after_Cleaning_mass_conc'] = df[pol+suffix[idx]]

    df = df.dropna()
    cities = df
    # Extract the data we're interested in
    lat = cities['lat'].values
    lon = cities['lon'].values
    sat = cities['site_name'].values


    cities['un_Complaince_change'] = cities['Complaince_change']
    population = cities['Percentage_change'].values
    area = cities['NO2 _after_Cleaning_mass_conc']


    # cvals  = [-20,-10, 0, 20,40, 60, 80,100]
    # colors = ["#c1e0ff",'#c1e0ff','#fcd059', "#ffcd74", "#FFA500", "#FF6347", "#FF4500", "#FF0000"]

    # norm=plt.Normalize(min(cvals),max(cvals))
    # tuples = list(zip(map(norm,cvals), colors))
    # cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples, N =6)
    cmap = cmr.tropical_r


    plot_all(axs[axes[idx][0], axes[idx][1]], df, True)
    import matplotlib as mpl
    geodf1 = gpd.read_file(r"CPCB_Issues\AirPy_v2\india_taluk.geojson")

    mpl.rcParams['axes.linewidth'] = 0.5 #set the value globally

        
    cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower left',
                        bbox_to_anchor=(-0.01-0.04+0.08,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)
    cbaxes.set_ylim([19.029+0.01, 19.102+0.01])       #mum
    cbaxes.set_xlim([72.82, 72.9])          #mum 
    geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
    cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
    plot_all(cbaxes, df, False)
    plt.text(.03, .94, ' 1', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')
    ax = fig.gca()
    for axis in ['top','bottom','left','right']:
        cbaxes.spines[axis].set_linewidth(0.4)

    cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower center',
                        bbox_to_anchor=(-0.01-0.04,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)

    geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
    cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
    plot_all(cbaxes, df, False)
    cbaxes.set_ylim([22.48, 22.662])       #kol
    cbaxes.set_xlim([88.25, 88.45])
    plt.text(.03, .94, ' 2', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')
    ax = fig.gca()
    for axis in ['top','bottom','left','right']:
        cbaxes.spines[axis].set_linewidth(0.4)

    cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower right',
                        bbox_to_anchor=(-0.01-0.05-0.07,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)
    geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
    cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
    plot_all(cbaxes, df, False)
    cbaxes.set_ylim([27.49+0.85,28.88])
    cbaxes.set_xlim([76+0.8, 77.4])
    plt.text(.03, .94, ' 3', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')

    ax = fig.gca()
    for axis in ['top','bottom','left','right']:
        cbaxes.spines[axis].set_linewidth(0.4)
        


    # plt.text(, 'K', ax=, fontsize=12)
    axs[axes[idx][0], axes[idx][1]].annotate('2', xy=(88.25, 22.48),ha="center", va="center", color='black', fontsize=6,
            bbox=dict(boxstyle='square', facecolor='white', edgecolor='black',lw=.4))

    axs[axes[idx][0], axes[idx][1]].annotate('1', xy=(72.82, 19.029+0.01),ha="center", va="center", color='black', fontsize=6,
            bbox=dict(boxstyle='square', facecolor='white', edgecolor='black',lw=0.4))

    axs[axes[idx][0], axes[idx][1]].annotate('3', xy=(76+0.8, 27.49+0.85),ha="center", va="center", color='black', fontsize=6,
            bbox=dict(boxstyle='square', facecolor='white', edgecolor='black',lw=0.4))
    

    site_id = df['site_name'].iloc[0]
    plt.savefig(f'CPCB_Issues/AirPy_v2/new_data/summary/summary_plots/{year}.png', dpi=300)

