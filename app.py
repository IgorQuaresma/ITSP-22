from flask import Flask, render_template, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def bus_stops_all():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id")  # combine both dataframes using "stop_id" column


    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
    df_combined = df_combined.drop_duplicates(subset=['stop_id'])

    dict_all_stops = df_combined.to_dict('records')


    return render_template('home.html', bus_stops_all_markers=dict_all_stops)

@app.route('/stop_times')
def stop_times():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id") #combine both dataframes using "stop_id" column

    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
    dict_combined = df_combined.to_dict('records')

    return render_template('home.html', bus_stops_all_markers=dict_combined)

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
