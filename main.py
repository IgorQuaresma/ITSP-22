from flask import Flask

app = Flask(__name__)

@app.route('/')
def ola():
    return '<h1>Hello World 2!</h1>'

app.run()
