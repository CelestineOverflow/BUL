# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os, sys, json


# %%
negative_result_folder = r'D:\BUL\lab-2\negative\data'
positive_result_folder = r'D:\BUL\lab-2\positive\data'
folder_to_look = [negative_result_folder, positive_result_folder]
files = []
for folder in folder_to_look:
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            files.append(os.path.join(folder, file))
            
df_all = pd.DataFrame()
            
for file in files:
    name = file.split('.')[0]
    filter_setting = name.split('_')[2]
    acc_setting = name.split('_')[5]
    gyro_setting = name.split('_')[8]
    file_count = name.split('_')[9] 
    # print(file)
    #check if path contains negative or positive
    orientation = 'negative' if 'negative' in file else 'positive'
    if not file_count == '1':
        continue
    df = pd.read_csv(file)
    df = df.drop(columns=['Unnamed: 0'])
    # display(df, filter_setting, acc_setting, gyro_setting, file_count)
    #add filter setting, acc setting, gyro setting, file count to df
    df['filter_setting'] = filter_setting
    df['acc_setting'] = acc_setting
    df['gyro_setting'] = gyro_setting
    df['file_count'] = file_count
    df['orientation'] = orientation
    df_all = pd.concat([df_all, df], ignore_index=True)

display(df_all)




# %%

#check if orientation key is valid
if not 'orientation' in df_all.keys():
    print('orientation key not found')
    sys.exit(1)
else:
    print('orientation key found')

# %%
#mean values for the gyro at 250 gyro setting
df_gyro_250 = df_all[df_all['gyro_setting'] == '250']
df_mean_gyro_250 = df_gyro_250.groupby(['filter_setting', 'acc_setting', 'file_count', 'orientation']).mean()
#delete all where the orientation is positive
df_mean_gyro_250 = df_mean_gyro_250.drop('positive', level=3)
display(df_mean_gyro_250)
filter_settings = ['5HZ', '10HZ', '21HZ', '44HZ', '94HZ', '184HZ', '260HZ']
for filter_setting in filter_settings:
    df_filter = df_mean_gyro_250.loc[filter_setting]
    #only one orientation
    df_filter = df_filter.reset_index()
    fig = px.line(df_filter, x="acc_setting", y="gyr_X", title=f'Gyro X for {filter_setting} filter setting, 250 gyro setting')
    fig.show()

# %%
#get only df where filter setting is 10HZ and acc setting is 2G
# filter_setting = '10HZ'
# acc_setting = '2G'

filter_settings = ['10HZ', '21HZ', '44HZ', '260HZ']
acc_settings = ['2G', '4G', '8G', '16G']
for filter_setting in filter_settings:
    for acc_setting in acc_settings:
        df_filtered = df_all[(df_all['filter_setting'] == filter_setting) & (df_all['acc_setting'] == acc_setting)]
        display(df_filtered)
        #only where acc_X is negative
        df_filtered = df_filtered[df_filtered['acc_X'] < 0]
        #make a histogram of the acc_X
        fig = px.histogram(df_filtered, x="acc_Y", color="orientation", marginal="rug", hover_data=df_filtered.columns)
        fig.update_layout(
            title_text='Histogram of acc_Y where filter setting is ' + filter_setting + ' and acc setting is ' + acc_setting,
            xaxis_title_text='acc_Y int 16 signed value',
            yaxis_title_text='Count',
            bargap=0.2, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        fig.show()

# %%
#plot the average for each filter setting 
for filter_setting in filter_settings:
    df_filtered = df_all[(df_all['filter_setting'] == filter_setting)]
    #if acc_X is the abs of the value
    df_filtered['acc_X'] = df_filtered['acc_X'].abs()
    
    def acc_X_to_lsb(acc_X):
        return 1 / acc_X
    
    #apply the function to the column
    df_filtered['acc_X_lsb'] = df_filtered['acc_X'].apply(acc_X_to_lsb)
    
    df_filtered = df_filtered.groupby(['acc_setting', 'orientation']).mean().reset_index()
    #sort by acc setting 2 4 8 16
    df_filtered['acc_setting'] = pd.Categorical(df_filtered['acc_setting'], ['-16G', '-8G', '-4G', '-2G', '2G', '4G', '8G', '16G'])
    df_filtered = df_filtered.sort_values('acc_setting')
    fig = px.line(df_filtered, x="acc_setting", y="acc_X_lsb", color="orientation")
    fig.update_layout(
        title_text='Average of acc_X where filter setting is ' + filter_setting,
        xaxis_title_text='acc setting',
        yaxis_title_text='Average acc_X int 16 signed value',
    )
    #flip the y axis
    fig.show()

# %%
#plot the average for each filter setting 
for filter_setting in filter_settings:
    df_filtered = df_all[(df_all['filter_setting'] == filter_setting)]
    #if acc_X is negative then acc setting is - acc setting
    df_filtered['acc_setting'] = np.where(df_filtered['acc_X'] > 0, df_filtered['acc_setting'], '-' + df_filtered['acc_setting'])
    
    df_filtered = df_filtered.groupby(['acc_setting', 'orientation']).mean().reset_index()
    #sort by acc setting 2 4 8 16
    df_filtered['acc_setting'] = pd.Categorical(df_filtered['acc_setting'], ['-16G', '-8G', '-4G', '-2G', '2G', '4G', '8G', '16G'])
    df_filtered = df_filtered.sort_values('acc_setting')
    fig = px.line(df_filtered, x="acc_setting", y="acc_X", color="orientation")
    fig.update_layout(
        title_text='Average of acc_X where filter setting is ' + filter_setting,
        xaxis_title_text='acc setting',
        yaxis_title_text='Average acc_X int 16 signed value',
    )
    #flip the y axis
    fig.show()

# %%
filter_settings = ['10HZ', '21HZ', '44HZ', '260HZ']
gyro_settings = ['250', '500', '1000', '2000']
for filter_setting in filter_settings:
    for gyro_setting in gyro_settings:
        df_filtered = df_all[(df_all['filter_setting'] == filter_setting) & (df_all['gyro_setting'] == gyro_setting)]
        display(df_filtered)
        #make a histogram of the acc_X
        fig = px.histogram(df_filtered, x="gyr_X", marginal="rug", hover_data=df_filtered.columns)
        fig.update_layout(
            title_text='Histogram of gyro_X where filter setting is ' + filter_setting + ' and gyro setting is ' + gyro_setting,
            xaxis_title_text='gyro_X int 16 signed value',
            yaxis_title_text='Count',
            bargap=0.2, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        fig.show()

# %%
#measure the noise on acc_y
#get the std deviance of acc_y for each filter setting and acc setting
df_std = pd.DataFrame(columns=['filter_setting', 'acc_setting', 'std_deviance'])
for filter_setting in filter_settings:
    for acc_setting in acc_settings:
        df_filtered = df_all[(df_all['filter_setting'] == filter_setting) & (df_all['acc_setting'] == acc_setting)]
        df_std = pd.concat([df_std, pd.DataFrame([[filter_setting, acc_setting, df_filtered['acc_Y'].std()]], columns=['filter_setting', 'acc_setting', 'std_deviance'])], ignore_index=True)
display(df_std)

fig = px.line(df_std, x="acc_setting", y="std_deviance", color="filter_setting")
fig.show()

# %%
#do the same for gyro
gyro_settings = ['250', '500', '1000', '2000']
df_std = pd.DataFrame(columns=['filter_setting', 'gyro_setting', 'std_deviance'])
for filter_setting in filter_settings:
    for gyro_setting in gyro_settings:
        df_filtered = df_all[(df_all['filter_setting'] == filter_setting) & (df_all['gyro_setting'] == gyro_setting)]
        df_std = pd.concat([df_std, pd.DataFrame([[filter_setting, gyro_setting, df_filtered['gyr_X'].std()]], columns=['filter_setting', 'gyro_setting', 'std_deviance'])], ignore_index=True)
display(df_std)
fig = px.line(df_std, x="gyro_setting", y="std_deviance", color="filter_setting")
fig.show()



