    # ratio is calculated by dividing the sum of reported NO and NO2 by reported NOx
    local_df['ratio'] = (local_df['NO'] + local_df['NO2'])/local_df['NOx']
    #based on ratio calculated, a separate category is assigned using the fuction unit class
    local_df['score'] = local_df['ratio'].apply(unit_class)
    #if no unit is identified for that particular row, assign a dummy category "yellow"
    local_df['score'] = local_df['score'].replace(np.nan, 'yellow')
    # Using NO + NO2 = NOx (ppb); assume that NO2 is incorrectly reported in ppb
    local_df['score'].mask((((local_df['NO']) + (local_df['NO2']) - (local_df['NOx'])*1.9125).abs() < 5), 'green', inplace=True)
    # Using NO + NO2 = NOx (ppb); assume that NO2, NO is incorrectly reported in ppb
    local_df['score'].mask((((local_df['NO']) + (local_df['NO2']) - (local_df['NOx'])).abs() < 5), 'red', inplace=True)
    # Using NO + NO2 = NOx (ppb); assume that all are correctly reported according to CPCB standards
    local_df['score'].mask((((local_df['NO'])/1.23 + (local_df['NO2'])/1.88 - (local_df['NOx'])).abs() < 5), 'blue', inplace=True)