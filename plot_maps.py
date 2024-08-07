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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# %matplotlib notebook
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from math import ceil, floor
from datetime import datetime
import os

from copy import deepcopy
#==========================================================
#=========================================================

'''
Sample:
    df = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean_final.csv")
    count_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_count_final.csv")
    sites_master = pd.read_csv(r"CPCB_Issues\AirPy_v2\sites_master.csv")
    create_map_plots(df, count_summary, sites_master, 2023, ['PM25', 'PM10', 'NO2', 'Ozone'])
'''

DA_THRESHOLD_AFTER_CLEANING = 50
DA_THRESHOLD_BEFORE_CLEANING = 75


def get_colorbar(pollutant: str) -> matplotlib.colors.LinearSegmentedColormap:
    if pollutant == 'NO2':
        cvals  = [-20,-10, 0, 20,40, 60, 80,100]
        colors = ["#c1e0ff",'#c1e0ff','#fcd059', "#ffcd74", "#FFA500", "#FF6347", "#FF4500", "#FF0000"]
        ticks = [-20, 0, 20, 40, 60, 80, 100]
        norm=plt.Normalize(min(cvals),max(cvals))
        tuples = list(zip(map(norm,cvals), colors))
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples, N = 6)
        cmap.set_extremes(over='#630000', under='#00008B')
    else:
        cvals  = [-6,-3, 0,3, 6]
        colors = ["#0077c0","#73C2FB","#E1EBEE","#FEBE10", "#FF0000"]
        ticks = [-6,-4,-2,0,2,4,6]
        norm=plt.Normalize()
        norm.autoscale(cvals)
        tuples = list(zip(map(norm,cvals), colors))
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples, N = 6)
        cmap.set_extremes(over='#630000', under='#00008B')
    return cmap, cvals, ticks

def create_map_plots(mean_summary: pd.DataFrame, count_summary: pd.DataFrame, year: int, pollutants: list, site_list = pd.DataFrame):
    suffix = ['_clean','_CPCB','_clean','_clean']
    # axes = [(0,0), (1,0), (2,0), (3,0)]
    axes = [(0,0), (0,1), (1,0), (1,1)]
    # fig, axs = plt.subplots(2, 2,figsize=(7,9),sharey=True,sharex=True)
    fig, axs = plt.subplots(4, 1,figsize=(4,18),sharey=True,sharex=True)
    fig.tight_layout()
    sites_master = pd.read_csv(r"CPCB_Issues\AirPy_v2\sites_master.csv")
    size_consts = {'PM25': 0.7, 'PM10': 0.35, 'NO2': 0.7, 'Ozone': 0.7}
    save_df = pd.DataFrame()
    master_summary = pd.merge(mean_summary,count_summary,how='left',on=['site_id','year'],suffixes=(None,'_count'))
    # print(master_summary)
    

    def plot_all(ax, df: pd.DataFrame, colorbar:bool, pol:str):
        CONST = size_consts[pol]
        # print(df.columns)
        # temp = df[(df[pol+'_DA_before'] < DA_THRESHOLD_BEFORE_CLEANING)] # Plot hollow red sites less than 75% data availability even BEFORE cleaning
        # # print(temp[['site_id', 'site_name', pol+'_DA', pol+'_DA_before']])
        # ax.scatter(temp['lon'], temp['lat'], label=None, facecolors='#808080', 
        #                         edgecolors='#808080', 
        #                         s=1.5, linewidth=0.25, alpha=1) # Plot all gray sites
        # temp = df[(df[pol+'_DA'] < DA_THRESHOLD_AFTER_CLEANING) & (df[pol+'_DA_before'] > DA_THRESHOLD_BEFORE_CLEANING)] # Plot black sites with less than 50% data availability AFTER cleaning
        # # print(temp[['site_id', 'site_name', pol+'_DA', pol+'_DA_before']])
        # ax.scatter(temp['lon'], temp['lat'], label=None, 
        #                         edgecolors='#000000', c='#000000',
        #                         s=1.5, linewidth=0.1, alpha=1) # Plot all gray sites

        temp_da = df[(df[pol+'_DA'] >= DA_THRESHOLD_AFTER_CLEANING) & (df[pol+'_DA_before'] >= DA_THRESHOLD_BEFORE_CLEANING)] # Plot only sites with more than 75% data availability
        temp_da_percentage = temp_da[(temp_da['percentage_change'] > -20) & (temp_da['percentage_change'] < 100)]
        temp_da_percentage = temp_da_percentage[np.logical_not(temp_da_percentage['compliance_change'])]
        
        cmap, cvals, ticks = get_colorbar(pol)
        normalizer = (min(cvals), max(cvals))
        temp_da_percentage = temp_da_percentage.sort_values(by='percentage_change'  )
        z1_plot = ax.scatter(temp_da_percentage['lon'], temp_da_percentage['lat'], label=None, c=temp_da_percentage['percentage_change'], 
                                cmap=cmap, 
                                vmin = normalizer[0], 
                                vmax = normalizer[1],
                                edgecolors='#707070', 
                                s=temp_da_percentage['pollutant_after_cleaning']*CONST, 
                                linewidth=0.25, alpha=1) 
        if colorbar == True: 
            pol_string = {
                'Ozone':'O' + '$_{3}$',
                'NO2':'NO' + '$_{2}$',
                'PM25':'PM' + '$_{2.5}$',
                'PM10':'PM' + '$_{10}$'
            }
            cbaxes = inset_axes(ax, width="30%", height="3%",loc='lower right',
                                bbox_to_anchor=(-0.13,0.14,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes) 
            cvals = np.array(cvals)

            cbar = plt.colorbar(z1_plot, cbaxes,orientation='horizontal', ticks = ticks, shrink = 1, extend='both', extendfrac=0.1)
            # cbar = plt.colorbar(z1_plot, cbaxes,orientation='horizontal', ticks = cvals, shrink = 1)
            cbar.dividers.set_linewidth(0.4)

            cbaxes.set_title("Change in annual mean "+  pol_string[pol] + ' [%]', fontsize = 5.5)
            cbaxes.tick_params(labelsize=5,width = 0.5)
            cbar.outline.set_linewidth(0.4)
            pol_areas = {
                'Ozone': [5,30,50],
                'NO2': [5,50,80],
                'PM25': [20,50,90],
                'PM10': [20,50,90]
            }
            for area in pol_areas[pol]:
                if area == 0: area = 1
                ax.scatter([], [], c='k', alpha=1, s=area, label = area)
            ax.legend(scatterpoints=1, frameon=False,loc="upper right",
                    labelspacing=1, title='Annual mean'+"\n"+
                                            '    [µg m' + '$^{-3}$' + ']',
                    prop={'size': 6}, bbox_to_anchor =(0.89, 0.99), ncol = 1).get_title().set_fontsize('6')
        
        temp_compliance = temp_da[temp_da['compliance_change']]
        ax.scatter(temp_compliance['lon'], temp_compliance['lat'], label=None, c=temp_compliance['percentage_change'], 
                                cmap=cmap, 
                                vmax=100,
                                vmin = -20, 
                                edgecolors='black', 
                                s=temp_compliance['pollutant_after_cleaning']*CONST, linewidth=0.5, alpha=1)

    
    
    #Plot all outlines
    
    #RESHAPING SO CODE WORKS with 2x2 grid and 4x1
    if axs.shape == (4,):
        axs = axs.reshape(2,2)

    for ax in axs:
        for axis in ax:
            # geodf = gpd.read_file("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
            geodf = gpd.read_file("CPCB_Issues/AirPy_v2/india_state_original.geojson")
            geodf.plot(ax=axis, color='white', linewidth=.4,edgecolor='#545454')
            axis.set_xticklabels([])
            axis.set_yticklabels([])
            axis.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
            axis.axis('off')

            axis.annotate('wwwwwwwwww' + '\n'   +
                            'wwwwwwwwww' + '\n', xy=(90,11),ha="center", va="center", color='white', fontsize=9,
                    bbox=dict(boxstyle='square', facecolor='white', edgecolor='white',lw=0.4))


    plt.subplots_adjust(wspace=0,hspace=0.3,top=0.95,bottom=0.05)

    for idx, pollutant in enumerate(pollutants):
        print('PLOTTING FOR: ', year, pollutant)
        #Choose which sites to plot for this pollutant
        pol = pollutant
        df = deepcopy(master_summary)
        # print(df.shape)
        # exit()
        if (len(site_list) > 0):
            if 'pollutant' in site_list.columns:
                unplotted_sites = site_list['site_id'][~site_list['site_id'].isin(df['site_id'])]
                # print('UNPLOTTED SITES: ',unplotted_sites)

                new_rows = []
                for site_id in unplotted_sites.values:
                    new_row_dict = {col: 0 for col in df.columns}
                    new_row_dict['site_id'] = site_id
                    new_row_dict['timestamp'] = 1
                    new_rows.append(new_row_dict)
                new_rows_df = pd.DataFrame(new_rows)
                df = pd.concat([df, new_rows_df], ignore_index=True)

                unplotted_sites = site_list['site_id'][~site_list['site_id'].isin(df['site_id'])]
                # print('UNPLOTTED SITES AFTER PROCESSING: ',unplotted_sites)
                df = df[df['site_id'].isin(site_list['site_id'])]
            else:
                df = df[df['site_id'].isin(site_list['site_id'])]

        df[pol+'_DA_before'] = ((df[pol + '_count']/df['timestamp_count']) * 100).fillna(0)
        df[pol+'_DA'] = ((df[pol + suffix[idx] + '_count']/df['timestamp_count']) * 100).fillna(0)

        df = df[df['year'] == year]
        # df_count = df_count[df_count['year'] == year]
        # print(len(df['site_id']))
        df['lat'] = df['site_id'].map(sites_master.set_index('site_id')['latitude'])
        df['lon'] = df['site_id'].map(sites_master.set_index('site_id')['longitude'])
        df = deepcopy(df[['site_id', pol, pol+suffix[idx], 'site_name', 'lat' , 'lon', pol + suffix[idx] + '_count', pol+'_DA', 'year',pol+'_count',pol+'_DA_before','timestamp_count']])
        df['percentage_change'] = ((df[pol + suffix[idx]] - df[pol])*100)/df[pol] #(After - Before) / Before

        COMPLIANCE_THRESHOLD = 40 if pol in ['NO2','PM25'] else 100
        df['compliance_change_non_to_compl'] = ((df[pol] > COMPLIANCE_THRESHOLD) & (df[pol+suffix[idx]] < COMPLIANCE_THRESHOLD))
        df['compliance_change_compl_to_non'] = ((df[pol] < COMPLIANCE_THRESHOLD) & (df[pol+suffix[idx]] > COMPLIANCE_THRESHOLD))
        df['compliance_change'] = df['compliance_change_compl_to_non'] | df['compliance_change_non_to_compl']


        df['pollutant_before_cleaning_mass_conc'] = df[pol]
        df['pollutant_after_cleaning'] = df[pol+suffix[idx]]    
        
        mumbai = df[(df['lat'] > 19.03) & (df['lat'] < 19.112) & (df['lon'] > 72.82) & (df['lon'] < 72.9)]
        kolkata = df[(df['lat'] > 22.48) & (df['lat'] < 22.662) & (df['lon'] > 88.25) & (df['lon'] < 88.45)]
        delhi = df[(df['lat'] > 28.34) & (df['lat'] < 28.88) & (df['lon'] > 76.08) & (df['lon'] < 77.4)]
        save_df_path = f'CPCB_Issues/AirPy_v2/new_data/summary/{year}_summary_mapping.csv'
        df['pollutant'] = pol
        df.to_csv(save_df_path, index=False, mode='a', header = not os.path.exists(save_df_path))


        df = df[(df.isin(mumbai) == False) & (df.isin(kolkata) == False) & (df.isin(delhi) == False)]

        plot_all(axs[axes[idx][0], axes[idx][1]], df, True,pol=pol)
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
        plot_all(cbaxes, mumbai, False, pol=pol)
        plt.text(.03, .94, ' 1', ha='left', va='top', transform=cbaxes.transAxes, size= 6, backgroundcolor = 'none')
        ax = fig.gca()
        for axis in ['top','bottom','left','right']:
            cbaxes.spines[axis].set_linewidth(0.4)

        #Kolkata
        cbaxes = inset_axes(axs[axes[idx][0], axes[idx][1]], width="25%", height="25%", loc='lower center',
                            bbox_to_anchor=(-0.01-0.04,-0.18,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes)

        geodf1.plot(ax=cbaxes, color='white', linewidth=.4,edgecolor='grey')
        cbaxes.tick_params(left = False, right = False , labelleft = False ,labelbottom = False, bottom = False)
        plot_all(cbaxes, kolkata, False, pol=pol)
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
        plot_all(cbaxes, delhi, False, pol=pol)
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

        if year == 2019:
            plt.text(-0.10, .94, '(a) '+"O" + '$_{3}$', ha='left', va='top', transform=axs[0,0].transAxes, size= 11, backgroundcolor = 'none')
            plt.text(-0.1, .94, '(b) '+ "NO" + '$_{2}$', ha='left', va='top', transform=axs[0,1].transAxes, size= 11, backgroundcolor = 'none')
            plt.text(-0.1, .94, '(c) '+"PM" + '$_{2.5}$', ha='left', va='top', transform=axs[1,0].transAxes, size= 11, backgroundcolor = 'none')
            plt.text(-0.1, .94, '(d) '+"PM" + '$_{10}$', ha='left', va='top', transform=axs[1,1].transAxes, size= 11, backgroundcolor = 'none')
        elif year == 2023:
            plt.text(-0.10, .94, '(e) '+"O" + '$_{3}$', ha='left', va='top', transform=axs[0,0].transAxes, size= 11, backgroundcolor = 'none')
            plt.text(-0.1, .94, '(f) '+ "NO" + '$_{2}$', ha='left', va='top', transform=axs[0,1].transAxes, size= 11, backgroundcolor = 'none')
            plt.text(-0.1, .94, '(g) '+"PM" + '$_{2.5}$', ha='left', va='top', transform=axs[1,0].transAxes, size= 11, backgroundcolor = 'none')
            plt.text(-0.1, .94, '(h) '+"PM" + '$_{10}$', ha='left', va='top', transform=axs[1,1].transAxes, size= 11, backgroundcolor = 'none')


        plt.suptitle(f"YEAR: {year}")
        print('SAVING',df.shape, save_df.shape)
        plt.savefig(f'CPCB_Issues/AirPy_v2/new_data/summary/final_plots/{year}_4map_plot_columnar_without_gray_{datetime.now().strftime("%Y%m%d_%H%M")}.png', dpi=300)

    # plt.show()

if __name__ == '__main__':
    years = [2019,2023]
    # years = [2019,2020,2021,2022,2023]
    # years = [2019]
    for year in years:
        os.remove(f'CPCB_Issues/AirPy_v2/new_data/summary/{year}_summary_mapping.csv')
        mean_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_mean_AQI.csv")
        count_summary = pd.read_csv(r"CPCB_Issues\AirPy_v2\new_data\summary\summary_count_AQI.csv")
        sites_to_plot = pd.read_csv(r"CPCB_Issues\AirPy_v2\final_site_list_new.csv")
        create_map_plots(mean_summary, count_summary, year, ['Ozone','NO2', 'PM25', 'PM10'], site_list = sites_to_plot)
