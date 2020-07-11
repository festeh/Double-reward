from os import environ
from pprint import pprint
from typing import Optional

import requests


def create_habitica_auth_headers():
    user_id = environ["APP_HABITICA_USER_ID"].strip()
    token = environ["APP_HABITICA_TOKEN"]
    headers = {"x-client": f"{user_id}-todobitica",
               "x-api-key": token,
               'x-api-user': user_id}
    return headers


def create_habitica_task(auth_headers, text):
    create_task_url = "https://habitica.com/api/v3/tasks/user"
    task = {"type": "todo", "text": text}
    res = requests.post(create_task_url, json=task, headers=auth_headers).json()
    if res['success'] is True:
        data = res['data']
        return data["id"]
    return None


def delete_habitica_task(auth_headers, task_id):
    delete_task_url = f"https://habitica.com/api/v3/tasks/{task_id}"
    result = requests.delete(delete_task_url, headers=auth_headers).json()
    return result["success"] is True


def get_habitica_user_todo_tasks(auth_headers) -> Optional[dict]:
    get_tasks_url = "https://habitica.com/api/v3/tasks/user"
    query_params = {"type": "todos"}
    result = requests.get(get_tasks_url, query_params, headers=auth_headers).json()
    if result["success"] is True:
        return result["data"]
    return None


def complete_habitica_task(auth_headers, task_id) -> bool:
    complete_task_url = f"https://habitica.com/api/v3/tasks/{task_id}/score/up"
    result = requests.post(complete_task_url, headers=auth_headers).json()
    return result["success"] is True


if __name__ == '__main__':
    auth_headers = create_habitica_auth_headers()
    pprint(get_habitica_user_todo_tasks(auth_headers))
