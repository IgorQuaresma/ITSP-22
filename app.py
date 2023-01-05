from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')

def city_center():
    markers = [
        {
            'lat': 47.9990,
            'lon': 7.8421,
            'popup': 'Freiburg im Breisgau'
        }
    ]
    return render_template('index.html', markers=markers)

@app.route('/bus_stops_all')
def bus_stops_all():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    dict_all_stops = df_all_stops.to_dict('records')

    return render_template('index.html', bus_stops_all_markers=dict_all_stops)

if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
