from flask import Flask, render_template, render_template_string, request, redirect, session
import pandas as pd
import folium
from jinja2 import Template
from folium.map import Marker

app = Flask(__name__)
app.secret_key = "12345"

# @app.route('/')
# def bus_stops_all():
#     df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
#     df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
#     df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id")  # combine both dataframes using "stop_id" column
#
#
#     df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
#     dict_all_stops = df_combined.to_dict('records')


@app.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map()

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


@app.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        width=1100,
        height=600,
        location=[47.9990, 7.8421],
        zoom_start=12
    )

    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id")  # combine both dataframes using "stop_id" column


    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
    df_combined['stop_lat'] = df_combined['stop_lat'].astype(str) #treat name as str to be used by folium
    df_combined['stop_lon'] = df_combined['stop_lon'].astype(str) #treat name as str to be used by folium
    df_combined = df_combined.drop_duplicates(subset=['stop_id']) #remove duplicates


    #Creating list with coordinates to be ued by folium markers
    locations = df_combined[['stop_lat','stop_lon']]
    locations_list = locations.values.tolist()

    # for point in range(0, len(locations_list)):
    #     folium.Marker(locations_list[point]).add_to(m)

    for bus_stop in range(0, len(df_combined)):
        folium.Marker(
            location=[df_combined.iloc[bus_stop]['stop_lat'], df_combined.iloc[bus_stop]['stop_lon']],
            popup=df_combined.iloc[bus_stop]['stop_name'].split(",")[1].strip()
        ).add_to(m)



    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Using componentssss</h1>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )



@app.route('/stop_times')
def stop_times():
    df_all_stops = pd.read_csv("./data/gtfs/stops.txt")
    df_stop_times = pd.read_csv("./data/gtfs/stop_times.txt")
    df_combined = pd.merge(df_all_stops, df_stop_times, left_on="stop_id", right_on="stop_id") #combine both dataframes using "stop_id" column

    df_combined = df_combined[df_combined["stop_name"].str.contains("Freiburg")] #filter only stops in Freiburg (optimize performance)
    dict_combined = df_combined.to_dict('records')

    return dict_combined

    #return render_template('home.html', bus_stops_all_markers=dict_combined)


@app.route('/about/')
def about():
    return render_template('about.html')



if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
