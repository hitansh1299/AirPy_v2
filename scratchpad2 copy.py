import pandas as pd
import matplotlib.pyplot as plt

# Load data
final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list_new.csv')
count_summary = pd.read_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count_all.csv')

# Filter sites based on site_id presence in final_site_list
sites = count_summary[count_summary['site_id'].isin(final_site_list['site_id'])]

# Define years of interest
years = [2019, 2020, 2021, 2022, 2023]

# Initialize lists to store data for plotting
percentage_error_free = []
total_sites_per_year = []
error_sites_per_year = []

# Analyze data per year
for year in years:
    sites_year = sites[sites['year'] == year]
    error_free = sites_year[sites_year['score'].str.contains('red|green|violet', regex=True, na=False)]
    
    total_sites = sites_year['site_id'].nunique()
    error_sites = total_sites - error_free['site_id'].nunique()
    
    percentage_error_free.append((error_free['site_id'].nunique() / total_sites) * 100)
    total_sites_per_year.append(total_sites)
    error_sites_per_year.append(error_sites)

    print(f"Year {year}: {error_free['site_id'].nunique()} error-free out of {total_sites} sites")

# Create the plot
fig, ax1 = plt.subplots(figsize=(10, 5))

# Bar chart for error-free percentage
ax1.bar(years, percentage_error_free, color='royalblue', label='Error Free (%)')
ax1.bar(x=years, height=list(map(lambda x: 100-x, percentage_error_free)), bottom=percentage_error_free, label='Unit Inconsistency Found', color='orangered')
ax1.set_xlabel('Year')
ax1.set_ylabel('Percentage Error Free (%)', color='royalblue')
# plt.bar(x=years, height=percentage_error_free, label='Error Free')
ax1.tick_params(axis='y', labelcolor='royalblue')

# Adding a second y-axis for the number of sites with errors
ax2 = ax1.twinx()
ax2.plot(years, error_sites_per_year, color='k', label='Sites with Errors', marker='o')
ax2.set_ylabel('Number of Sites with Errors', color='k')
ax2.tick_params(axis='y', labelcolor='k')
ax2.set_ylim(0,100)

# Adding legends
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

# Show the plot
plt.show()
