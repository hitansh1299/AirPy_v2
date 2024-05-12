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
from datetime import datetime
#==========================================================
#=========================================================

'''
Sample:
    df = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean_final.csv")
    count_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_count_final.csv")
    sites_master = pd.read_csv(r"CPCB_Issues\AirPy_v2\sites_master.csv")
    create_map_plots(df, count_summary, sites_master, 2023, ['PM25', 'PM10', 'NO2', 'Ozone'])
'''

def get_colorbar(pollutant: str) -> matplotlib.colors.LinearSegmentedColormap:
    if pollutant == 'NO2' or pollutant == 'Ozone':
        colors = ["#c1e0ff",'#c1e0ff','#fcd059', "#ffcd74", "#FFA500", "#FF6347", "#FF4500", "#FF0000"]
        cvals  = [-20,-10, 0, 20, 40, 60, 80, 100]
        norm=plt.Normalize()
        norm.autoscale(cvals)
        tuples = list(zip(map(norm,cvals), colors))
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples, N = 7)
    else:
        colors = ["#0077c0","#73C2FB","#E1EBEE","#FEBE10", "#FF0000"]
        cvals  = [-6,-3, 0,3, 6]
        norm=plt.Normalize()
        norm.autoscale(cvals)
        tuples = list(zip(map(norm,cvals), colors))
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples, N = 5)

    return cmap, cvals

def create_map_plots(mean_summary: pd.DataFrame, count_summary: pd.DataFrame, year: int, pollutants: list, site_list = pd.DataFrame):
    suffix = ['_clean','_CPCB','_clean','_clean']
    axes = [(0,0), (0,1), (1,0), (1,1)]
    sites_master = pd.read_csv(r"CPCB_Issues\AirPy_v2\sites_master.csv")
    def plot_all(ax, df: pd.DataFrame, colorbar):
        CONST = 0.25
        CONST = 0.5 * CONST if pol == 'PM10' else 1
        
        temp = df
        temp = df[(df[pol+'_DA']<75) | (df[pol+'_DA'] == np.nan) | (df[pol] == np.nan) | (df[pol + suffix[idx]] == 1)]
        print(temp['Percentage_change'].min(), temp['Percentage_change'].max())
        if len(temp['Percentage_change'].dropna()) == 0:
            return

        ax.scatter(temp['lon'], temp['lat'], label=None, c= '#808080', 
                                edgecolors='#808080', 
                                s=10, linewidth=0.1, alpha=1) # Plot all gray sites
        
        df = df[df[pol+'_DA'] > 75] # Plot only sites with more than 75% data availability
        # temp = df[(df[pol+'_DA']>75) & (df['Percentage_change'] > -20) & (df['Percentage_change'] < 100)]
        temp = df[(df['Percentage_change'] > -20) & (df['Percentage_change'] < 100)]
        # temp = df
        cmap, cvals = get_colorbar(pol)
        # print('MAX: ',int(ceil(temp['Percentage_change'].max())), int(ceil(temp['Percentage_change'].min())))
        # MAIN PLOT
        z1_plot = ax.scatter(temp['lon'], temp['lat'], label=None, c= temp['Percentage_change'], 
                                cmap=cmap, 
                                # vmin = 0, 
                                # vmax = int(ceil(temp['Percentage_change'].max())),
                                edgecolors='#c0c0c0', 
                                s=temp['pollutant_after_cleaning']*CONST, 
                                # s=2,
                                linewidth=0.1, alpha=1) 
        if colorbar == True: 
            cbaxes = inset_axes(ax, width="30%", height="3%",loc='lower right',
                                bbox_to_anchor=(-0.13,0.14,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes) 
        
            cbar = plt.colorbar(z1_plot, cbaxes,orientation='horizontal', ticks = np.linspace(min(cvals), max(cvals), len(cvals) - 1), shrink = 1)
            cbar.dividers.set_linewidth(0.4)
            cbaxes.set_title("Change in annual mean "+  pol + ' [%]', fontsize = 5.5)
            cbaxes.tick_params(labelsize=6,width = 0.4)
            cbar.outline.set_linewidth(0.4)
            #plot legend
            cleaned_min = int(floor((temp['pollutant_after_cleaning']*0.25).min()))
            cleaned_max = int(ceil((temp['pollutant_after_cleaning']*0.25).max()))
            base = 5
            for area in (np.ceil(np.linspace(cleaned_min, cleaned_max, 3)/base) * base):
                ax.scatter([], [], c='k', alpha=1, s=area,
                            label = area)
            ax.legend(scatterpoints=1, frameon=False,loc="upper right",
                    labelspacing=0.5, title='Annual mean'+"\n"+
                                            '    [µg m' + '$^{-3}$' + ']',
                    prop={'size': 6}, bbox_to_anchor =(0.89, 0.99), ncol = 1).get_title().set_fontsize('6')

            # temp = df[df[pol+'_DA']>75]
            temp = temp[temp['compliance_change'] == 1]

            z1_plot = ax.scatter(temp['lon'], temp['lat'], label=None, c= temp['Percentage_change'], 
                                    cmap=cmap, 
                                    #    vmax=100,
                                    edgecolors='black', 
                                    #    vmin = -20, 
                                    s=temp['pollutant_after_cleaning']*CONST, linewidth=0.5, alpha=1)
        

        temp1 = temp[temp['Percentage_change'] > 100]
    #     print(temp)
        ax.scatter(temp1['lon'], temp1['lat'], label=None, c= '#00008B', s=temp1['pollutant_after_cleaning']*CONST, 
                linewidth=0.5, alpha=1, edgecolors='black')
        temp2 = temp[temp['Percentage_change'] < -20]
        ax.scatter(temp2['lon'], temp2['lat'], label=None, c= '#00008B', s=temp2['pollutant_after_cleaning']*CONST, 
                linewidth=0.5, alpha=1, edgecolors='black')

    fig, axs = plt.subplots(2, 2,figsize=(7,9),sharey=True,sharex=True)
    #Plot all outlines
    for ax in axs:
        for axis in ax:
            geodf = gpd.read_file("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
            geodf.plot(ax=axis, color='white', linewidth=.4,edgecolor='#545454')
            axis.set_xticklabels([])
            axis.set_yticklabels([])
            axis.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
            axis.axis('off')

            axis.annotate('wwwwwwwwww' + '\n'   +
                            'wwwwwwwwww' + '\n', xy=(90,11),ha="center", va="center", color='white', fontsize=9,
                    bbox=dict(boxstyle='square', facecolor='white', edgecolor='white',lw=0.4))


    plt.subplots_adjust(wspace=0, hspace=0)
    for idx, pollutant in enumerate(pollutants):
        print('PLOTTING FOR: ', year, pollutant)
        #Choose which sites to plot for this pollutant
        pol = pollutant
        df = mean_summary[mean_summary['year'] == year].copy()
        df[pol+'_DA'] = (count_summary[pol]/count_summary['timestamp']) * 100
        if (len(site_list) > 0):
            if 'pollutant' in site_list.columns:
                df = df[df['site_id'].isin(site_list.loc[site_list['pollutant'] == pollutant, 'site_id'])]
            else:
                df = df[df['site_id'].isin(site_list['site_id'])]
        
        print(len(df['site_id']))
        df['lat'] = df['site_id'].map(sites_master.set_index('site_id')['latitude'])
        df['lon'] = df['site_id'].map(sites_master.set_index('site_id')['longitude'])
        df = df [[pol, pol+suffix[idx], 'site_name', 'lat' , 'lon', pol+'_DA']].copy()
        df['Percentage_change'] = (df[pol + suffix[idx]] - df[pol])*100/df[pol]
        # df['compliance_change'] = np.where((df[pol+suffix[idx]] - df[pol]).abs()/df[pol], 1, 0)
        # df['compliance_change'] = np.where((df[pol+suffix[idx]] - df[pol]))

        df['before_com'] = np.where(df[pol] > 40,1 , 0)
        df['after_com'] = np.where(df[pol + suffix[idx]] > 40,1 , 0)
        df['compliance_change'] = np.where(df['before_com'] == df['after_com'],0,1)

        df['pollutant_before_cleaning_mass_conc'] = df[pol]
        df['pollutant_after_cleaning'] = df[pol+suffix[idx]]

        df = df.dropna()
        cities = df

        cities['un_compliance_change'] = cities['compliance_change']
        print(cities['compliance_change'].value_counts())
        mumbai = df[(df['lat'] > 19.03) & (df['lat'] < 19.112) & (df['lon'] > 72.82) & (df['lon'] < 72.9)]
        kolkata = df[(df['lat'] > 22.48) & (df['lat'] < 22.662) & (df['lon'] > 88.25) & (df['lon'] < 88.45)]
        delhi = df[(df['lat'] > 28.34) & (df['lat'] < 28.88) & (df['lon'] > 76.08) & (df['lon'] < 77.4)]

        df = df[(df.isin(mumbai) == False) & (df.isin(kolkata) == False) & (df.isin(delhi) == False)]

        plot_all(axs[axes[idx][0], axes[idx][1]], df, True,)
        import matplotlib as mpl
        geodf1 = gpd.read_file(r"CPCB_Issues\AirPy_v2\india_taluk.geojson")

        mpl.rcParams['axes.linewidth'] = 0.5 #set the value globally

        #Mumbai
        cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower left',
                            bbox_to_anchor=(-0.01-0.04+0.08,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)
        cbaxes.set_ylim([19.029+0.01, 19.102+0.01])       #mum
        cbaxes.set_xlim([72.82, 72.9])          #mum 
        geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
        cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        plot_all(cbaxes, mumbai, False)
        plt.text(.03, .94, ' 1', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')
        ax = fig.gca()
        for axis in ['top','bottom','left','right']:
            cbaxes.spines[axis].set_linewidth(0.4)

        #Kolkata
        cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower center',
                            bbox_to_anchor=(-0.01-0.04,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)

        geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
        cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        plot_all(cbaxes, kolkata, False)
        cbaxes.set_ylim([22.48, 22.662])       #kol
        cbaxes.set_xlim([88.25, 88.45])
        plt.text(.03, .94, ' 2', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')
        ax = fig.gca()
        for axis in ['top','bottom','left','right']:
            cbaxes.spines[axis].set_linewidth(0.4)

        #Delhi
        cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower right',
                            bbox_to_anchor=(-0.01-0.05-0.07,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)
        geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
        cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        plot_all(cbaxes, delhi, False)
        cbaxes.set_ylim([27.49+0.85,28.88])
        cbaxes.set_xlim([76+0.8, 77.4])
        plt.text(.03, .94, ' 3', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')

        ax = fig.gca()
        for axis in ['top','bottom','left','right']:
            cbaxes.spines[axis].set_linewidth(0.4)
            

        axs[axes[idx][0], axes[idx][1]].annotate('2', xy=(88.25, 22.48),ha="center", va="center", color='black', fontsize=6,
               bbox=dict(boxstyle='square', facecolor='white', edgecolor='black',lw=.4))

        axs[axes[idx][0], axes[idx][1]].annotate('1', xy=(72.82, 19.029+0.01),ha="center", va="center", color='black', fontsize=6,
               bbox=dict(boxstyle='square', facecolor='white', edgecolor='black',lw=0.4))

        axs[axes[idx][0], axes[idx][1]].annotate('3', xy=(76+0.8, 27.49+0.85),ha="center", va="center", color='black', fontsize=6,
               bbox=dict(boxstyle='square', facecolor='white', edgecolor='black',lw=0.4))
    plt.suptitle(f"YEAR: {year}")
    plt.savefig(f'CPCB_Issues/AirPy_v2/new_data/summary/final_plots/{year}_4map_plot_new_{datetime.now().strftime("%Y%m%d_%H%M")}.png', dpi=300)

    # plt.show()

if __name__ == '__main__':
    years = [2019,2020,2021,2022,2023]
    # years = [2020, 202]
    for year in years:
        mean_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean_all.csv")
        count_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_count_all.csv")
        
        sites_to_plot = pd.read_csv(r"CPCB_Issues\AirPy_v2\final_site_list_new.csv")
        # sites_to_plot = pd.read_csv(r"C:\Users\hitan\OneDrive\Desktop\MiniProjects\ML_NMIMS Codes\CPCB_Issues\original_40_sites.csv")[0:40]
        # print(len(sites_to_plot['site_id'].unique()))
        # print(len(df['site_id'].unique()))
        # exit()
        create_map_plots(mean_summary, count_summary, year, ['Ozone','NO2', 'PM25', 'PM10'], site_list = sites_to_plot)
