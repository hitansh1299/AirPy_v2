import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
plt.figure(figsize=(16, 9))
changes = pd.read_csv(r'CPCB_Issues\AirPy_v2\summary_mean_map_plot.csv')
sites_to_plot = pd.read_csv(r"CPCB_Issues\AirPy_v2\final_site_list_new.csv")

changes = changes[changes['site_id'].isin(sites_to_plot['site_id'])]
changes_grouped = changes.groupby('pollutant')

# #create a table of percentage change for each year for each pollutant
# sns.boxplot(x='pollutant', y='Percentage_change', data=changes[changes['pollutant'].isin(['Ozone','PM25','PM10','NO2'])], hue='year', showfliers=False)
# plt.yticks(ticks = np.round(np.linspace(-100,200, 60)))
# plt.savefig(r'boxplot.png')


# plt.show()


# create a histogram for each pollutant for each year
for pollutant, data in changes_grouped:
    for year in data['year'].unique():
        data_year = data[data['year'] == year]
        sns.histplot(data_year['Percentage_change'], bins=1000, alpha=0.7, kde=True)
        plt.title(pollutant + ' | ' + str(year))
        plt.xticks(ticks = np.linspace(data_year['Percentage_change'].min(),data_year['Percentage_change'].max(), 50), fontsize=8, rotation='vertical')
        # plt.xticks(ticks = np.sort(np.unique(np.round(np.linspace(data_year['Percentage_change'].min(),data_year['Percentage_change'].max(), 20)))))

        # plt.legend()
        # plt.show()
        plt.savefig(r'CPCB_Issues\AirPy_v2\new_data\summary\temp_'+pollutant+'_'+str(year)+'.png')
        plt.close()