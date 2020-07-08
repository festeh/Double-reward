from os import environ
from pprint import pprint

from flask import Flask
from todoist.api import TodoistAPI
from dotenv import load_dotenv
from flask import request

load_dotenv(verbose=True)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sync')
def my_sync():
    token = environ["APP_TODOIST_TOKEN"]
    api = TodoistAPI(token)
    api.sync()
    projects = api.state['projects']
    print(projects)
    return "OK"


@app.route('/todoist_item_completed', methods=['POST'])
def todoist_item_completed():
    request_data = request.get_json()
    return request_data, 200


if __name__ == '__main__':
    app.run()
