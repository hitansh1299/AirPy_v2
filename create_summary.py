import pandas as pd
import numpy as np
import glob
import pandas as pd
import tqdm

files = glob.glob('CPCB_Issues/AirPy_v2/new_data/After_Cleaning_New/*2019*')
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
            # try:
            #     summary['score'] = df['score'].value_counts().sort_index().index.str.cat(sep=',')
            # except KeyError as e:
            #     summary['score'] = ''
            try:
                summary['prevalent_error'] = df['error'].value_counts().idxmax()
            except KeyError as e:
                summary['prevalent_error'] = ''
            try:
                summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',')
            except KeyError as e:
                summary['errors'] = ''

            # print(summary)
            summaries.append(summary)
        except Exception as e: 
            print('failed for file: ',str(e.with_traceback(e.__traceback__)),file, file=open('CPCB_Issues/AirPy_v2/new_data/summary/errors.txt','a'))
            # raise e
    summaries_df = pd.DataFrame(summaries)
     
    return summaries_df

def summarize_mean_file(files: list):
    summaries = []
    for file in tqdm.tqdm(files):
        try:
            df = pd.read_csv(file)
            summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['mean'].to_dict()
            summary['site_id'] = df['site_id'][0]
            summary['site_name'] = df['site_name'][0]
            summary['year'] = df['year'][0]
            summary['mismatch'] = df['mismatch'].sum()
            # print(df.columns)
            # try:
            #     summary['score'] = df['score'].value_counts().sort_index().index.str.cat(sep=',')
            # except KeyError as e:
            #     summary['score'] = ''
            try:
                summary['prevalent_error'] = df['error'].value_counts().idxmax()
            except KeyError as e:
                summary['prevalent_error'] = ''
            try:
                summary['errors'] = df['error'].value_counts().sort_index().index.str.cat(sep=',')
            except KeyError as e:
                summary['errors'] = ''
            
            # print(summary)
            summaries.append(summary)
        except Exception as e: 
            print('failed for file: ',str(e.with_traceback(e.__traceback__)),file, file=open('CPCB_Issues/AirPy_v2/new_data/summary/errors.txt','a'))   
    summaries_df = pd.DataFrame(summaries)
    return summaries_df


if __name__ == '__main__':
    summarize_mean_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_mean_2019.csv', index=False)
    summarize_count_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_2019.csv', index=False)
    # final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list.csv')
    # summary_count = summarize_count_file(files)
    # summary_count[summary_count['site_id'].isin(final_site_list['site_id'])].to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_final.csv', index=False)
    # summary_mean = summarize_mean_file(files)
    # summary_mean[summary_mean['site_id'].isin(final_site_list['site_id'])].to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_mean_final.csv', index=False)

    