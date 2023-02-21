from flask import Flask, render_template, url_for
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def bus_stops_all():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id")  # combine both dataframes using "stop_id" column


    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)


    ##




    #get current time
    current_time = datetime.now()  # get current time
    time_interval = 30  # time interval in min
    weekday = current_time.weekday()  # from 0 to 6 from Monday to Sunday

    stop_times_prop_arrival = df_combined[pd.to_numeric(df_combined['arrival_time'].str[:2].values) < 24]  # eliminate not proper records
    df_combined['arrival_time'] = pd.to_datetime(stop_times_prop_arrival['arrival_time'], format='%H:%M:%S').dt.time  # change type to t

    up_time = (current_time + timedelta(minutes=time_interval)).time()  # get time in defined interval in min

    buses_current_timeinterval = df_combined[(df_combined['arrival_time'] > current_time.time()) & (df_combined['arrival_time'] < up_time)].sort_values(by="arrival_time").drop_duplicates(subset=["stop_id"])  # get only the first record (first bus that will come)



    dict_all_stops = buses_current_timeinterval.to_dict('records')


    return render_template('home.html', bus_stops_all_markers=dict_all_stops)


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
