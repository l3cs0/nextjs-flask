from flask import Flask

app = Flask(__name__)


@app.route("/api/python")
def hello_world():
    return "<p>Hello, Python!</p>"


@app.route("/api/hello", methods=["GET"])
def hello_world2():
    return "Hello, Hello!"
