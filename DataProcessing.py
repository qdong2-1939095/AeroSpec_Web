import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

DATA_PATH = 'data/'

data_files = []
for f in os.listdir(DATA_PATH):
        if not f.startswith('.'):
                data_files.append(f)

data_array = []
device_names = []
for d in data_files:
        device_name = d.split('.')[0]
        device_names.append(device_name)
        data_df = pd.read_csv(DATA_PATH + d, skiprows=1)
        data_df.columns = data_df.columns.str.replace(' ','')
        data_df['Device'] = device_name
        data_array.append(data_df)
all_device_data = pd.concat(data_array)


# add datetime
all_device_data['Datetime'] = pd.to_datetime(all_device_data['Date'] + ' ' + all_device_data['Time'])

to_numeric_cols = all_device_data.columns.drop(['Time', 'Date', 'Battery', 'Fix', 'Longitude','Latitude', 'Temp(C)', 'RH(%)', 'P(hPa)', 'Alti(m)', 'Device', 'Datetime'])
all_device_data[to_numeric_cols] = all_device_data[to_numeric_cols].apply(pd.to_numeric, errors='coerce', downcast='float').astype(float)

all_device_data = all_device_data[['Datetime', 'Date', 'Time', 'Dp>0.3',
       'Dp>0.5', 'Dp>1.0', 'Dp>2.5', 'Dp>5.0', 'Dp>10.0', 'PM1_Std',
       'PM2.5_Std', 'PM10_Std', 'PM1_Env', 'PM2.5_Env', 'PM10_Env','Device']]

rounded = pd.DataFrame(all_device_data['Datetime'].dt.round('5s'))
all_device_data['Datetime_round'] = rounded

all_device_data_rounded = all_device_data.groupby(['Datetime_round','Device']).mean().reset_index()

# Helper functions
def plot_line_chart(df, x, y, title):
    plot = px.line(df,
                          x=x,
                          y=y,
                          color='Device',
                          title=title,
                          labels={'Datetime_round': 'Time'})
    return plot

def drop_numerical_outliers(df, z_thresh=4):
    constrains = df.select_dtypes(include=['float64']) \
        .apply(lambda x: np.abs(stats.zscore(x)) < z_thresh).all(axis=1)
    idx = df.index[constrains==False].tolist()
    new_df = df.drop(idx)
    return new_df

# Get data betweem a specific time 'YYYY-MM-DD HH:MM:SS'
START_TIME = '2022-04-22 16:00:00'
END_TIME = '2022-04-22 16:15:00'

data_in_time_range = all_device_data_rounded[(all_device_data_rounded['Datetime_round'] >= START_TIME) & (all_device_data_rounded['Datetime_round'] <= END_TIME)]

lineplt_by_time = plot_line_chart(df=data_in_time_range, x='Datetime_round', y='Dp>0.3', title='Dp>0.3 Collected by Device')
lineplt_by_time.write_html('./Figures/lineplt_by_time.html')

Z_thresh = 4
data_removed_extreme = drop_numerical_outliers(data_in_time_range.copy(), Z_thresh)

removed_extreme_plot = plot_line_chart(data_removed_extreme, 'Datetime_round', 'Dp>0.3', 'Dp>0.3 Collected by Device with Extreme Removed')
removed_extreme_plot.write_html('./Figures/removed_extreme_plot.html')

measured_type_plot = go.Figure()
columns = ['Dp>0.3', 'Dp>0.5', 'Dp>1.0', 'Dp>2.5', 'Dp>5.0', 'Dp>10.0', 'PM1_Std', 'PM2.5_Std', 'PM10_Std', 'PM1_Env', 'PM2.5_Env', 'PM10_Env']
for c in columns:
    measured_type_plot.add_traces(plot_line_chart(data_in_time_range, 'Datetime_round', c, c + 'Collected by Device').update_traces(visible=False).data)
measured_type_plot.update_traces()
measured_type_plot.update_layout(
updatemenus=[
    dict(
        active=0,
        buttons=list([
            dict(label="Select",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, False, False, False, False,False, False]},
                       {"title": "Select one field to start..."}]),
            dict(label="Dp>0.3",
                 method="update",
                 args=[{"visible": [True, False, False, False, False, False, False, False, False, False,False, False]},
                       {"title": "Dp>0.3"}]),
            dict(label="Dp>0.5",
                 method="update",
                 args=[{"visible": [False, True, False, False, False, False, False, False, False, False,False, False]},
                       {"title": "Dp>0.5"}]),
            dict(label="Dp>1.0",
                 method="update",
                 args=[{"visible": [False, False, True, False, False, False, False, False, False, False,False, False]},
                       {"title": "Dp>1.0"}]),
            dict(label="Dp>2.5",
                 method="update",
                 args=[{"visible": [False, False, False, True, False, False, False, False, False, False,False, False]},
                       {"title": "Dp>2.5"}]),
            dict(label="Dp>5.0",
                 method="update",
                 args=[{"visible": [False, False, False, False, True, False, False, False, False, False,False, False]},
                       {"title": "Dp>5.0"}]),
            dict(label="Dp>10.0",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, True, False, False, False, False,False, False]},
                       {"title": "Dp>10.0"}]),
            dict(label="PM1_Std",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, True, False, False, False,False, False]},
                       {"title": "PM1_Std"}]),
            dict(label="PM2.5_Std",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, False, True, False, False,False, False]},
                       {"title": "PM2.5_Std"}]),
            dict(label="PM10_Std",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, False, False, True, False, False, False]},
                       {"title": "PM10_Std"}]),
            dict(label="PM1_Env",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, False, False, False, True, False, False]},
                       {"title": "PM1_Env"}]),
            dict(label="PM2.5_Env",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, False, False, False, False, True, False]},
                       {"title": "PM2.5_Env"}]),
            dict(label="PM10_Env",
                 method="update",
                 args=[{"visible": [False, False, False, False, False, False, False, False, False, False, False, True]},
                       {"title": "PM10_Env"}]),

        ]),
    )
])

# measured_type_plot.add_trace(go.Scatter(
#     x=data_in_time_range['Datetime_round'],
#     y=data_in_time_range['Dp>0.3'],
#      fill='Device',
#     name = 'Dp>0.3'))
# measured_type_plot.add_trace( go.Scatter(
#         x=data_in_time_range['Datetime_round'],
#     y=data_in_time_range['Dp>0.5'],
#     name = 'Dp>0.5'))
measured_type_plot.write_html('./Figures/measured_type_plot.html')

