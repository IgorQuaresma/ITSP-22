from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def root():
    markers = [
        {
            'lat': 47.9990,
            'lon': 7.8421,
            'popup': 'Freiburg im Breisgau'
        }
    ]
    return render_template('index.html', markers=markers)


if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
