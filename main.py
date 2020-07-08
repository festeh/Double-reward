import json
from os import environ
from pprint import pprint

from flask import Flask
from habitica_utils import create_habitica_auth_headers, create_habitica_task, complete_habitica_task
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
    print(json.dumps(request_data))
    task_content = request_data["content"]
    print("Got task from Todoist", task_content)
    habitica_auth_headers = create_habitica_auth_headers()
    created_task_id = create_habitica_task(habitica_auth_headers, task_content)
    print("Created task in Habitica", created_task_id)
    is_completed = complete_habitica_task(habitica_auth_headers, created_task_id)
    print("Task completion status", is_completed)
    return "OK", 200


if __name__ == '__main__':
    app.run()
