import pandas as pd
import numpy as np
import glob
import pandas as pd
import tqdm
from aqi_calculator import calculate_gvaqi
files = glob.glob('CPCB_Issues/AirPy_v2/new_data/After_Cleaning/*')
import warnings
warnings.simplefilter(action='ignore')

def summarize_count_file(files: list):
    summaries = []
    for file in tqdm.tqdm(files):
        try:
            df = pd.read_csv(file)
            summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['count'].to_dict()
            summary['site_id'] = df['site_id'][0]
            summary['site_name'] = df['site_name'][0]
            summary['year'] = df['year'][0]
            summary['mismatch'] = df['mismatch'].sum() 
            summary['prevalent_error'] = df['error'].value_counts().idxmax()
            summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',')
            summary['errors'] = ''

            if len(df['error'].dropna()) > 0:
                summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',') 
                summary['prevalent_error'] = df['error'].value_counts().idxmax()
            else:
                summary['errors'] = ''
                summary['prevalent_error'] = ''

            # print(summary)
            summaries.append(summary)
        except KeyError as e:
            summary[e.args[0]] = ''
        except Exception as e: 
            print('failed for file: ',str(e.with_traceback(e.__traceback__)),file, file=open('CPCB_Issues/AirPy_v2/new_data/summary/errors_count.txt','a'))
            # raise e
    summaries_df = pd.DataFrame(summaries)
     
    return summaries_df

def summarize_mean_file(files: list):
    summaries = []
    # files = files[724:725]
    # files = ['CPCB_Issues/AirPy_v2/new_data/After_Cleaning/site_5071_Phase-1_GIDC_Vapi_GPCB_2023.csv']
    # print(files[724])
    # exit()
    for file in tqdm.tqdm(files):
        try:
            df = pd.read_csv(file)
            summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['mean'].to_dict()
            summary['site_id'] = df['site_id'][0]
            summary['site_name'] = df['site_name'][0]
            summary['year'] = df['year'][0]
            summary['mismatch'] = df['mismatch'].sum()
            summary['AQI_before_cleaning'] = calculate_gvaqi(df, cols=['NO2','PM10','PM25','Ozone'])['AQI'].mean()
            summary['AQI_after_cleaning'] = calculate_gvaqi(df)['AQI'].mean()
            # print(df['error'].value_counts().sort_index().index)
            # exit()
            if len(df['error'].dropna()) > 0:
                summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',') 
                summary['prevalent_error'] = df['error'].value_counts().idxmax()
            else:
                summary['errors'] = ''
                summary['prevalent_error'] = ''
            
        except KeyError as e:
            summary[e.args[0]] = ''
        except Exception as e: 
            print('failed for file: ',str(e.with_traceback(e.__traceback__)),file, file=open('CPCB_Issues/AirPy_v2/new_data/summary/errors.txt','a'))
            raise e
            # raise e 
        finally:
            summaries.append(summary)  
    summaries_df = pd.DataFrame(summaries)
    return summaries_df


if __name__ == '__main__':
    summarize_count_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_AQI.csv', index=False)
    summarize_mean_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_mean_AQI.csv', index=False)
    # final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list.csv')
    # summary_count = summarize_count_file(files)
    # summary_count[summary_count['site_id'].isin(final_site_list['site_id'])].to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_final.csv', index=False)
    # summary_mean = summarize_mean_file(files)
    # summary_mean[summary_mean['site_id'].isin(final_site_list['site_id'])].to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_mean_final.csv', index=False)

    