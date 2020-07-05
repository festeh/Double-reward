from os import environ

from flask import Flask
from todoist.api import TodoistAPI

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sync')
def my_sync():
    token = environ["APP_TOKEN"]
    api = TodoistAPI(token)
    api.sync()
    projects = api.state['projects']
    print(projects)
    return "SOSI"


if __name__ == '__main__':
    app.run()
