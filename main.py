from logging import info
from os import environ
import time

from flask import Flask, jsonify
from habitica_utils import create_habitica_auth_headers, create_habitica_task, complete_habitica_task
from todoist.api import TodoistAPI
from dotenv import load_dotenv
from flask import request

load_dotenv(verbose=True)
app = Flask(__name__)


@app.route('/todoist_item_completed', methods=['POST'])
def create_and_complete_task_in_habitica_if_completed_in_todoist():
    request_data = request.get_json()
    task_content = request_data["event_data"]["content"]
    info(f"Got task from Todoist: {task_content}")
    habitica_auth_headers = create_habitica_auth_headers()
    created_task_id = create_habitica_task(habitica_auth_headers, task_content)
    if created_task_id is None:
        raise RuntimeError("Unable to create Habitica task")
    info(f"Created Habitica task: {created_task_id}")
    # be nice to Habitica API and sleep some time
    time.sleep(30)
    is_completed = complete_habitica_task(habitica_auth_headers, created_task_id)
    if not is_completed:
        raise RuntimeError(f"Unable to complete Habitica task: {created_task_id}")
    info("Completed")
    return "OK", 200


@app.route('/todoist_projects')
def todoist_projects():
    token = environ["APP_TODOIST_TOKEN"]
    api = TodoistAPI(token)
    api.sync()
    projects = api.state['projects']
    return jsonify(projects)


@app.route('/exception')
def raise_error():
    raise RuntimeError("Here you are")


if __name__ == '__main__':
    app.run()
