import pandas as pd
final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list_new.csv')
print(final_site_list.groupby('pollutant').count())