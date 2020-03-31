import config
import json
import requests
import tokens


def format_waypoint_uri(params):
    endpoint = 'https://esi.evetech.net/latest/ui/autopilot/waypoint/?'
    p = '&'.join("{!s}={!s}".format(param, value) for (param, value) in params.items())  # flatten dict by =, &
    uri = endpoint + p
    return uri


def get_route():
    data = []
    with open(config.ROUTE_FILE, 'r') as route_file:
        for row in route_file:
            if row[0] == config.ROUTE_COMMENT_CHAR:
                continue
            data.append(row.rstrip())
    return data


def analyse_route(route):
    with open(config.SYSTEM_FILE, 'r') as system_file:
        system_data = json.load(system_file)

    cleaned_route_data = []
    errors = []
    for system_name in route:
        if system_name not in system_data and system_name not in system_data.values():
            errors.append(system_name)
            continue

        if system_name in system_data:
            cleaned_route_data.append(system_data[system_name])
        if system_name in system_data.values():
            cleaned_route_data.append(system_name)

    if errors:
        raise ValueError(errors)
    return cleaned_route_data


def post_waypoint(params):
    waypoint_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    waypoint_uri = format_waypoint_uri(params)
    print('Attemping to set destination to ' + params['destination_id'] + ' ', end='')
    response = requests.post(waypoint_uri, headers=waypoint_headers)
    print('(Status ' + str(response.status_code) + ')')


# do the magic
try:
    token_data = tokens.get_tokens_from_file()
except Exception as e:
    print(e.__str__())
    raise SystemExit(1)

access_token = token_data['access_token']

try:
    route_data = analyse_route(get_route())
except ValueError as e:
    print('Invalid system names/ids: ' + e.__str__())
    raise SystemExit(1)

for system in route_data:
    waypoint_params = {
        "add_to_beginning": "false",
        "clear_other_waypoints": "false",
        "datasource": "tranquility",
        "destination_id": system
    }
    post_waypoint(waypoint_params)
