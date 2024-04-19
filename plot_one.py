# path = os.path.join(directory, filename) 
from pathlib import Path
import pandas as pd
from data_cleaning import *
from sub_super_script import *
from html_utils import *
from formatting import *
from init_html import *
from plot_diurnal import *
from unit_inconsistency import *
from numbers_to_strings import *
from termcolor import *
import warnings
warnings.filterwarnings("ignore")
import os 
from datetime import datetime as time

os.chdir('CPCB_Issues\AirPy_v2')

data_dir = Path('../data/')
files = os.listdir(data_dir)
sites = pd.read_csv('sites.csv')
start = 0

prospective_sites = pd.read_csv('prospective_sites.csv')
years = [2019,2020,2021,2022,2023]

for idx, file in enumerate(files[start:], start=start):
    try:
        filepath = os.path.join(data_dir, file)
        # path = r'CPCB_Issues\AirPy_v2\new_data\Before_Cleaning\site_103_CRRI_Mathura_Road_Delhi_IMD_15Min_2017.csv'
        mixed_unit_identification = False
        print(filepath)
        site_id = '_'.join(file.split('_')[0:2])
        site_name = '_'.join(file.split('_')[2:-2])
        year = int(file.split('_')[-1].replace('.csv', ''))

        if site_id not in prospective_sites['site_id'].values or year not in years:
            print("Skipping ", site_name, " ", year)
            continue

        # print(site_name)
        
        city = sites[sites['site_code'] == site_id]['city'].values[0]
        true_df, station_name, city, state = get_formatted_df(filepath, site_name, city, '')
        true_df = true_df[true_df['dates'].dt.year == year]
        true_df = true_df.loc[~true_df.index.duplicated(keep='first')]

        df = true_df.copy(deep=True)

        filename=station_name+"_"+str(year) 
        # start_html(filename)
        
        print(colored("===========================================================================================", 'magenta', attrs=['bold']))
        print(colored(station_name,  'magenta', attrs=['bold']))
        print(colored("===========================================================================================", 'magenta', attrs=['bold']))




        # print(true_df)
        local_df = true_df.copy(deep=True)

        local_df['date'] =  pd.to_datetime(local_df['dates']).dt.date
        local_df = local_df.sort_values(by=['dates'])

        local_df = local_df[local_df['date'].notna()]
        local_df['site_id'] = site_id
        local_df['site_name'] = site_name
        local_df['city'] = city
        local_df['state'] = state
        pollutants = ['PM25', 'PM10', 'NOx', 'NO2', 'NO', 'Ozone' ]
        for pollutant in pollutants:
            if len(df[pollutant].value_counts()) == 0:
                print("No available ", pollutant, " data")
                continue
            else:
                local_df = group_plot(local_df, pollutant, pollutant,station_name,filename, plot=True)           
                local_df[pollutant + '_hourly'] = local_df.groupby("site_id")[pollutant].rolling(window = 4*1, min_periods = 1).mean().values
                local_df[pollutant + '_clean'] = local_df[pollutant + '_outliers']
                local_df[pollutant + '_clean'].mask(local_df[pollutant+ '_hourly'] < 0, np.nan, inplace=True)
                local_df.drop(columns=f"{pollutant}_hourly", inplace=True)

                print("successfully cleaned ", pollutant, " ", station_name)
        if df['NOx'].isnull().all() or df['NO2'].isnull().all() or df['NO'].isnull().all():
            print("No available NOx, NO2, NO data | Not checking for unit inconsistency")
        else:
            print("finding unit inconsistencies ", station_name)
            local_df = correct_unit_inconsistency(local_df,filename, mixed_unit_identification, plot=True)

        local_df = local_df.reindex()
        local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='_int')))]
        local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='(?<!_)consecutives')))]
        local_df = local_df.drop(columns=['t', 'std', 'med', 'date','ratio','Benzene', 'Toluene', 'Xylene', 'O Xylene', 'Eth-Benzene','MP-Xylene', 'AT', 'RH', 'WS', 'WD', 'RF', 'TOT-RF', 'SR', 'BP', 'VWS'], errors='ignore')
        local_df = local_df[['dates', 'site_id', 'city','state'] + [col for col in local_df.columns if col not in ['dates', 'site_id', 'city','state']]]
        local_df['year'] = year
        local_df.to_csv(str("new_data\\After_Cleaning\\") + str(station_name) +'_'+ str(year)+ ".csv", index=False)
        
        print(colored("----------------------------------------------------------------------------------------", 'green', attrs=['bold']))
        print(colored('saved successfully for'  + station_name,  'green', attrs=['bold']))
        print(colored("----------------------------------------------------------------------------------------", 'green', attrs=['bold']))
        plt.close('all')
    except Exception as e:
        print(f'EXCEPTION OCCURED IN {idx} : {file}', file = open('logs.txt', 'a'))
        print(e.with_traceback(e.__traceback__), file = open('logs.txt', 'a'))
        print('================================================================\n\n\n', file = open('logs.txt', 'a'))