import time
from functools import lru_cache

import requests
from environment import *
from language import convert_time_to_iso8601


def send_request(request, method, body=None):
    response = requests.request(method, request, headers={
        "X-Api-Key": api_key
    }, json=body)
    if response.status_code == 401:
        raise Exception('Unauthorized. Please check your API key.')
    if not response.ok:
        print(response.text)
        response.raise_for_status()

    return response.json()


@lru_cache
def send_request_cached(request, method):
    return send_request(request, method)


def get_tags():
    return send_request_cached(
        f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/tags',
        'GET'
    )


def get_workspace_users():
    return send_request_cached(
        f'https://api.clockify.me/api/workspaces/{workspace_id}/users/',
        'GET'
    )


def get_time_entries_page(page: int = 1, page_size: int = 50):
    return send_request(
        f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries'
        f'?page-size={page_size}&page={page}',
        'GET'
    )


def get_time_entries(page_size=50):
    time_entries = []
    page = 1
    while True:
        temp = get_time_entries_page(page, page_size)
        time_entries.extend(temp)
        if len(temp) < page_size:
            break
        page += 1
    return time_entries


def get_time_entry_base(time_entry):
    return {
        'billable': True,
        'customFieldValues': time_entry['customFieldValues'],
        'description': time_entry['description'],
        'end': time_entry['timeInterval']['end'],
        'id': time_entry['id'],
        'projectId': time_entry['projectId'],
        'start': time_entry['timeInterval']['start'],
        'tagIds': time_entry['tagIds'],
        'taskId': time_entry['taskId'],
        'type': time_entry['type'],
    }


def add_tag(time_entries, tag_id):
    send_request(
        f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries',
        'PUT',
        [
            {
                **get_time_entry_base(time_entry),
                'tagIds': list(set(time_entry['tagIds'] + [tag_id])),
            } for time_entry in time_entries
        ]
    )


def replace_tag(time_entries, old_tag_id, tag_id):
    send_request(
        f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries',
        'PUT',
        [
            {
                **get_time_entry_base(time_entry),
                'tagIds': list(set(map(lambda tag: tag if tag != old_tag_id else tag_id, time_entry['tagIds']))),
            } for time_entry in time_entries
        ]
    )
