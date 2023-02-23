from flask import Flask, render_template, url_for
import pandas as pd
from datetime import datetime, timedelta
import re


#Create all necessary functions
def create_final_df(df_input):
    ''''based on the input of the df with combined data of stops.txt and stop_times.txt
     create a dictionary of the already treated information'''

    df_combined = df_input[df_input["stop_name"].str.contains("Freiburg")]  # filter only stops in Freiburg (optimize performance)

    # get current time
    current_time = datetime.now() # get current time
    time_interval = 30  # time interval in min
    weekday = current_time.weekday()  # from 0 to 6 from Monday to Sunday

    current_calendar_type = ''
    if weekday <= 4:
        current_calendar_type = 'T0'
    elif weekday == 5:
        current_calendar_type = 'T2'
    else:
        current_calendar_type = 'T3'

    stop_times_prop_arrival = df_combined[pd.to_numeric(df_combined['arrival_time'].str[:2].values) < 24]  # eliminate not proper records
    df_combined['arrival_time'] = pd.to_datetime(stop_times_prop_arrival['arrival_time'],
                                              format='%H:%M:%S').dt.time  # change type to t

    up_time = (current_time + timedelta(minutes=time_interval)).time()  # get time in defined interval in min

    buses_current_timeinterval = (df_combined[(df_combined['arrival_time'] > current_time.time())
                                           & (df_combined['arrival_time'] < up_time)
                                           & (df_combined['trip_id'].map(lambda x: x.split(".")[1].strip()) == current_calendar_type)]  # filter only correct weekday
                                  .sort_values(by="arrival_time"))  # sort the arrival times from closer to further time of the user
                                    # get only the first record (first bus that will come)

    # crete new coloum where each row contains the list of trip_id values for the corresponding stop_id value in that row
    buses_current_timeinterval['all_lines'] = buses_current_timeinterval.apply(lambda x: buses_current_timeinterval.loc[buses_current_timeinterval['stop_id'] == x['stop_id'], 'trip_id']
                                                                               .tolist(), axis=1)

    #return all lines information formatted to show to the user (only show bus line number)
    for i in range(len(buses_current_timeinterval['all_lines'])):
        buses_current_timeinterval['all_lines'].iloc[i] = ", ".join(set(
            re.findall(r'-(\d+)-', j)[0] for j in buses_current_timeinterval['all_lines'].iloc[i]))

    #buses_current_timeinterval['all_lines'] = buses_current_timeinterval['all_lines'].map(lambda x: x[0].split("-")[0].split(".")[-1]) #transform format to show bus line

    buses_current_timeinterval_drop = buses_current_timeinterval.drop_duplicates(subset=['stop_id']) # keep only the first line to plot the information (improve performance)

    dict_all_stops = buses_current_timeinterval_drop.to_dict('records') # transform the dataframe into a dictionary

    return dict_all_stops


#Create flask app
app = Flask(__name__)

@app.route('/')
def bus_stops_all():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id")  # combine both dataframes using "stop_id" column


    return render_template('home.html', bus_stops_all_markers=create_final_df(df_combined))


@app.route('/city_center')
def city_center():
    markers = [
        {
            'lat': 47.9990,
            'lon': 7.8421,
            'popup': 'Freiburg im Breisgau'
        }
    ]
    return render_template('home.html', markers=markers)

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
#
