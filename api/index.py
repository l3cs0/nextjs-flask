from flask import Flask, render_template, request
from api.capacityService.constraintSolver import constraintsolve
from api.capacityService.linearSolver import linearsolve

app = Flask(__name__)


@app.route("/api/python")
def hello_world():
    return "<p>Hello, Python!</p>"


@app.route("/api/hello", methods=["GET"])
def hello_world2():
    return render_template("index.html")


@app.route("/api/create", methods=["GET"])
def todo():
    mystring = create_string()
    return mystring


@app.route("/api/todo", methods=["GET"])
def create_todo_item():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return {"error": "Title is required"}, 400

    global todo_id_counter
    todo = {"id": todo_id_counter, "title": title, "completed": False}
    return todo, 201


@app.route("/api/solve", methods=["GET"])
def endpointsolve():
    data = request.get_json()
    A = data.get("A")
    # mystring = constraintsolve()

    return A


if __name__ == "__main__":
    app.run(port=5328)


def create_string():
    return "createdString"
