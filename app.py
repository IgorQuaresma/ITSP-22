from flask import Flask, render_template, url_for, request, redirect, session
import pandas as pd
import folium

app = Flask(__name__)
app.secret_key = "12345"

@app.route('/')
def bus_stops_all():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id")  # combine both dataframes using "stop_id" column


    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
    dict_all_stops = df_combined.to_dict('records')

    test = 2

    return render_template('home.html', bus_stops_all_markers=dict_all_stops, test=test)

@app.route('/stop_times')
def stop_times():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id") #combine both dataframes using "stop_id" column

    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
    dict_combined = df_combined.to_dict('records')

    return render_template('home.html', bus_stops_all_markers=dict_combined)


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    form_input = request.form['input_field']
    session['form_input'] = form_input
    # process form input
    # ...
    print(form_input)
    return redirect(url_for('bus_stops_all', form_input = form_input))



if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
