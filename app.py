from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def city1():
    markers = [
        {
            'lat': 47.9990,
            'lon': 7.8421,
            'popup': 'Freiburg im Breisgau'
        }
    ]
    return render_template('index.html', markers=markers)

@app.route('/bus_stops')
def bus_stops():
    bus_stops = [{'lat': 48.023901, 'lon': 7.724595, 'popup': 'Schutternstraße A'},
                 {'lat': 48.023775, 'lon': 7.724460, 'popup': 'Schutternstraße B'},
                 {'lat': 48.023414, 'lon': 7.719223, 'popup': 'Waltershofen Ochsen'}]

    return render_template('index.html', bus_stops_markers=bus_stops)

if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
