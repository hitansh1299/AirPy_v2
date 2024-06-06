import pandas as pd
import matplotlib.pyplot as plt
final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list_new.csv')
count_summary = pd.read_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_all.csv')
sites = count_summary[count_summary['site_id'].isin(final_site_list['site_id'])]
years = [2019,2020,2021,2022,2023]
percentage_error_free = []
for year in years:
    sites_year = sites[sites['year'] == year]
    error_free = sites_year[sites_year['score'].str.contains('red|green|violet', regex=True, na=False)]
    print(len(error_free), len(sites_year), len(error_free)/len(sites_year))
    # summarize in a stacked column plot (2 Y axis, one number and one %), that from 2019-2023 how many sites has one or the other issue
    # and how many of them are error free
    x = sites_year['site_id'].nunique()
    y = len(error_free)
    percentage_error_free += [(y/x) * 100]
plt.figure(figsize=(10,5))
plt.bar(x=years, height=percentage_error_free, label='Error Free')
plt.bar(x=years, height=list(map(lambda x: 100-x, percentage_error_free)), bottom=percentage_error_free, label='Unit Inconsistency Found')
plt.line(x=years, )
plt.show()
