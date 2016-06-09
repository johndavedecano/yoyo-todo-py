from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo

from config import *
from requests import Requests

app = Flask(__name__, static_folder=ASSETS_FOLDER, template_folder=TEMPLATE_FOLDER)
app.config.from_object('config')
data = PyMongo(app, config_prefix='MONGO')
requests = Requests(mongo=data)

# Route all these to the public
@app.route("/")
@app.route("/create")
@app.route("/update/<todo_id>")
@app.route("/view/<todo_id>")
def entry_point():
    return render_template('index.html')

@app.route("/api", methods=["GET"])
def api():
    return "Welcome to our API!"

# Fetch todos
@app.route("/api/todos", methods=["GET"])
def todos_index():
    return requests.todos_index()

# Create todos
@app.route("/api/todos", methods=["POST"])
def todos_create():
    return requests.todos_create()

# Show todos
@app.route("/api/todos/<todo_id>", methods=["GET"])
def todos_show(todo_id):
    return requests.todos_show(todo_id=todo_id)

# Update todos
@app.route("/api/todos/<todo_id>", methods=["PUT"])
def todos_update(todo_id):
    return requests.todos_update(todo_id=todo_id)

# Delete todos
@app.route("/api/todos/<todo_id>", methods=["DELETE"])
def todos_delete(todo_id):
    return requests.todos_delete(todo_id=todo_id)

if __name__ == '__main__':
    app.run(port=3000, debug=True)












