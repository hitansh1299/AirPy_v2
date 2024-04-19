import pandas as pd
import numpy as np
import glob
import pandas as pd
import tqdm

files = glob.glob('CPCB_Issues/AirPy_v2/new_data/After_Cleaning/*')
def summarize_count_file(files: list):
    summaries = []
    for file in tqdm.tqdm(files):
        df = pd.read_csv(file)
        summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['count'].to_dict()
        summary['site_id'] = df['site_id'][0]
        summary['site_name'] = df['site_name'][0]
        summary['year'] = df['year'][0]
        summaries.append(summary)
    summaries_df = pd.DataFrame(summaries)
    return summaries_df

def summarize_mean_file(files: list):
    summaries = []
    for file in tqdm.tqdm(files):
        df = pd.read_csv(file)
        summary = df.reset_index().rename(columns={'index':'timestamp'}).describe().loc['mean'].to_dict()
        summary['site_id'] = df['site_id'][0]
        summary['site_name'] = df['site_name'][0]
        summary['year'] = df['year'][0]
        summaries.append(summary)
    summaries_df = pd.DataFrame(summaries)
    return summaries_df


if __name__ == '__main__':
    summarize_count_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count.csv', index=False)
    summarize_mean_file(files).to_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_mean.csv', index=False)
