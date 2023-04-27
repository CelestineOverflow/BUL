# %%
import pandas as pd
import plotly.express as px
import os

# %%
folder_dir = r'D:\BUL\lab-1\result-two'
file_list = os.listdir(folder_dir)

df = pd.DataFrame(columns=['file_name', 'microseconds', 'distance[cm]'])

for file in file_list:
    if file.endswith('.csv'):
        file_name = file.split('.')[0]
        t = pd.read_csv(os.path.join(folder_dir, file))
        t['file_name'] = file_name
        #rename raw data to microseconds
        t = t.rename(columns={'raw_data': 'microseconds'})
        df = pd.concat([df, t], ignore_index=True)
        filename = file.split('.')[0]
        df = df.drop(columns=['Unnamed: 0'])

display(df)

# %%
for row in df.iterrows():
    expected_distance = int(row[1]['file_name'].split('cm')[0])
    df.loc[row[0], 'expected_distance[cm]'] = expected_distance
df['speed[m/s]'] = df['expected_distance[cm]'] * 2 * 10000 / (df['microseconds'])

display(df)

# %%


# %%
#creat a histogram per file_name
for file_name in df['file_name'].unique():
    df_temp = df[df['file_name'] == file_name]
    fig = px.histogram(df_temp, x='microseconds', nbins=100)
    fig.update_layout(title_text=file_name)
    fig.show()

# %%
display(df)

# %%
display(df)

# %%
#delete 0cm data
df = df[df['expected_distance[cm]'] != 0.0]
display(df)

# %%
for file_name in df['file_name'].unique():
    df_temp = df[df['file_name'] == file_name]
    fig = px.histogram(df_temp, x='microseconds', nbins=100)
    fig.update_layout(title_text=file_name)
    fig.show()

# %%
display(df)

# %%
df['expected_microseconds'] = df['expected_distance[cm]'] * 2 * 1000000 / (34300)
df['relative_error'] = (df['microseconds'] - df['expected_microseconds']) / df['expected_microseconds']

display(df)

# %%
fig = px.line(df, x='expected_microseconds', y='microseconds', color='file_name')
fig.show()

# %%
#take meas 0cm away from the table

fig = px.scatter(df, x='expected_distance[cm]', y='microseconds', color='file_name')
display(fig)
# show trend
df['speed[m/s]'] = df['expected_distance[cm]'] * 2 * 10000 / (df['microseconds'])
fig = px.scatter(df, x='expected_distance[cm]', y='speed[m/s]', color='file_name')
display(fig)

# %%
speed_of_sound = 34300 #cm/s
microseconds_to_100cm = 100 * 2 * 10000 / speed_of_sound
print(microseconds_to_100cm)

df

# %%
#plot mean values per file
print(type(df['microseconds'][0]))
df['microseconds'] = df['microseconds'].astype('float64')
#mean of microseconds
df_mean = df.groupby('file_name').mean()

# #drop 0cm distance
df_mean = df_mean.drop(index='0cm')

# # drop 1cm distance
df_mean = df_mean.drop(index='1cm')
df_mean = df_mean.reset_index().sort_values(by='distance[cm]')
#add the actual distance as a secondary row
df_mean['real_distance[cm]'] = df_mean['file_name'].apply(lambda x: int(x.split('cm')[0]))
df_mean['expected_microseconds'] = df_mean['real_distance[cm]'] * 2 * 1000000 / 34300

display(df_mean)
# fig = px.scatter(df_mean, x='real_distance[cm]', y='distance[cm]', trendline='ols')
# fig.update_layout(title_text='real_distance[cm] vs distance[cm] (mean)')
# fig.show()

# fig = px.scatter(df_mean, x='microseconds', y='expected_microseconds', trendline='ols')
# fig.update_layout(title_text='microseconds vs expected_microseconds')
# fig.show()


df_mean['relative_error_microseconds'] = (df_mean['microseconds'] - df_mean['expected_microseconds']) / df_mean['expected_microseconds']
df_mean['relative_error_microseconds_percent'] = df_mean['relative_error_microseconds'] * 100
df_microseconds = df_mean[['real_distance[cm]', 'microseconds', 'expected_microseconds', 'relative_error_microseconds', 'relative_error_microseconds_percent']]

#drop file_name 1cm


# fig = px.scatter(df_microseconds, x='real_distance[cm]', y='relative_error_microseconds_percent', trendline='ols')
# fig.update_layout(title_text='relative_error_microseconds_percent')
# fig.show()

# print(df_microseconds.to_markdown())
# df_microseconds.to_csv('df_microseconds.csv')

# %%


# %%
#speed of sound by mean 
df_speed = df[['expected_distance[cm]', 'speed[m/s]']].groupby('expected_distance[cm]').mean()
#drop were expected_distance is 0.0
df_speed = df_speed.drop(index=0.0)
df_speed = df_speed.drop(index=1.0)
fig = px.scatter(df_speed, x=df_speed.index, y='speed[m/s]', trendline='ols')
fig.update_layout(title_text='speed of sound by mean')
#add more ticks in x axis
fig.update_xaxes(dtick=10)
fig.update_yaxes(dtick=5)
fig.show()
display(df_speed)
# fig = px.scatter(df_speed, x="distance[cm]", y="microseconds", trendline="ols")

df_mean_microseconds = df[['expected_distance[cm]', 'microseconds']].groupby('expected_distance[cm]').mean()
df_mean_microseconds = df_mean_microseconds.drop(index=[0.0, 1.0])
display(df_mean_microseconds)

fig = px.scatter(df_mean_microseconds, x=df_mean_microseconds.index, y='microseconds', trendline='ols')
fig.update_layout(title_text='tof by expected_measurement')
#add more ticks in x axis
fig.show()

# %%
#relative error to the speed of sound 
df_speed['relative_error'] = (df_speed['speed[m/s]'] - 343) / 343
#relative error as percentage
df_speed['relative_error[%]'] = df_speed['relative_error'] * 100
fig = px.scatter(df_speed, x=df_speed.index, y='relative_error', trendline='ols')
fig.update_layout(title_text='relative error to the speed of sound')
#print to markdown
print(df_speed.to_markdown())

# %%
#calculate the relative error for each file
df_mean['relative_error'] = (df_mean['distance[cm]'] - df_mean['real_distance[cm]']) / df_mean['real_distance[cm]']
fig = px.scatter(df_mean, x='real_distance[cm]', y='relative_error')
fig.show()
#make a table with the relative error for markdown
print(df_mean[['real_distance[cm]', 'relative_error']].round(3).to_markdown(index=False))


# %%
result_dir = r'D:\BUL\lab-1'

files = os.listdir(result_dir)
count_diagonal = 0
count_horizontal = 0
df = pd.DataFrame(columns=['file_name', 'microseconds', 'distance[cm]'])
for file in files:
    if file.endswith('diagonal.csv'):
        count_diagonal += 1
        print('diagponal: ', file)
    elif file.endswith('.csv'):
        count_horizontal += 1
        print('horizontal: ', file)
    

# %%
files_dir = r'D:\BUL\lab-1\results_sideways'
files = os.listdir(files_dir)

map = {
  "10": { "x": 1, "y": 0, "distance[cm]": 62.26 },
  "11": { "x": 2, "y": 0, "distance[cm]": 78.38 },
  "1": { "x": 0, "y": 1 , "distance[cm]": 26.95},
  "3": { "x": 1, "y": 1 , "distance[cm]": 45.96},
  "5": { "x": 2, "y": 1 , "distance[cm]": 66.18},
  "7": { "x": 3, "y": 1 , "distance[cm]": 86.78},
  "9": { "x": 4, "y": 1 , "distance[cm]": 107.53},
  "0": { "x": 0, "y": 2 , "distance[cm]": 26.95},
  "2": { "x": 1, "y": 2 , "distance[cm]": 45.96},
  "4": { "x": 2, "y": 2 , "distance[cm]": 66.18},
  "6": { "x": 3, "y": 2 , "distance[cm]": 86.78},
  "8": { "x": 4, "y": 2 , "distance[cm]": 107.53},
  "12": { "x": 1, "y": 3 , "distance[cm]": 62.26},
  "13": { "x": 2, "y": 3 , "distance[cm]": 78.38},
}

df = pd.DataFrame(columns=['x', 'y', 'mean distance[cm]', 'type', 'expected_distance[cm]', 'error'])

for file in files:
    if file.endswith('.csv'):
        diagonal = False
        if 'diagonal' in file:
            diagonal = True
        if 'circular' in file:
            continue
        t = pd.read_csv(os.path.join(files_dir, file))
        t.drop(columns=['Unnamed: 0'], inplace=True)
        mean = t['distance[cm]'].mean()
        # print(file, mean)
        number = file.split('cm')[1].split('.')[0].split('diagonal')[0]
        # print(number)
        if number not in map:
            continue
        x = map[number]['x']
        y = map[number]['y']
        expected_distance = map[number]['distance[cm]']
        error = (mean - expected_distance) / expected_distance
        df = pd.concat([df, pd.DataFrame([[x, y, mean, 'diagonal' if diagonal else 'horizontal', expected_distance, error]], columns=['x', 'y', 'mean distance[cm]', 'type', 'expected_distance[cm]', 'error'])], ignore_index=True)
        
display(df)

# %%
horizontal = df[df['type'] == 'horizontal']
display(horizontal)
#show the heatmap for horizontal and error
fig = px.density_heatmap(horizontal, x='x', y='y', z='error', marginal_x='histogram', marginal_y='histogram')
fig.update_layout(title_text='horizontal error')
fig.show()

# %%
diagonal = df[df['type'] == 'diagonal']
display(diagonal)
#show the heatmap for diagonal
fig = px.density_heatmap(diagonal, x='x', y='y', z='error', marginal_x='histogram', marginal_y='histogram')
fig.update_layout(title_text='diagonal error')
fig.show()

# %%
import matplotlib.pyplot as plt
import numpy as np
import random
#draw heat map grid for random values in a grid of 10x10

#generate random values
#the grid with be 4x5
random_values = np.random.randint(0, 100, size=(4, 5))

#set value on 1,1 to 0
random_values[1, 1] = 0
print(random_values)


fig, ax = plt.subplots()

#change the ticks to 0 to 4
ax.set_xticks(np.arange(0, 5, 1))
ax.set_yticks(np.arange(0, 4, 1))

#set the x axis to be on top
ax.xaxis.tick_top()
im = ax.imshow(random_values)




# %%




