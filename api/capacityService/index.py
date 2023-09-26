from flask import Flask, render_template

app = Flask(__name__)


@app.route("/api/python")
def hello_world():
    return "<p>Hello, Python!</p>"


@app.route("/api/hello", methods=["GET"])
def hello_world2():
    return render_template("index.html")


@app.route("/api/create", methods=["GET"])
def todo():
    mystring = createString()
    return mystring


if __name__ == "__main__":
    app.run(port=5328)


def createString():
    return "createdString"
