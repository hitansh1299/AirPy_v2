import pandas as pd
import numpy as np
import glob
import pandas as pd
import tqdm

def summarize_count_file(files: list):
    summaries = []

    for file in tqdm.tqdm(files):
        try:
            df = pd.read_csv(file)
            df['month'] = pd.to_datetime(df['dates']).dt.month
            # df['dates'] = pd.to_datetime(df['dates'])
            df_group = df.groupby('month')
            for month in df_group:
                month = month[1]
                temp = month.reset_index().rename(columns={'index':'timestamp'})
                summary = temp.describe().loc['count'].to_dict()
                summary['site_id'] = temp['site_id'][0]
                summary['site_name'] = temp['site_name'][0]
                summary['year'] = temp['year'][0]
                summary['month'] = temp['month'][0]
                summaries.append(summary)
        except Exception as e: 
            raise e
            print('failed for file: ',file, file=open('errors.txt','a'))   
    summaries_df = pd.DataFrame(summaries)
     
    return summaries_df


if __name__ == '__main__':
    import os
    files = glob.glob('CPCB_Issues/AirPy_v2/new_data/After_Cleaning/*')
    final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list_new.csv')
    files = list(filter(lambda x: '_'.join(os.path.basename(x).split('_')[0:2]) in final_site_list['site_id'].values, files))
    summarize_count_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/monthly_condensed_new.csv', index=False)

    