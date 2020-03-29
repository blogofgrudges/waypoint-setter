import config
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
token_data = tokens.get_tokens_from_file()
access_token = token_data['access_token']
route_data = get_route()

for system in route_data:
    waypoint_params = {
        "add_to_beginning": "false",
        "clear_other_waypoints": "false",
        "datasource": "tranquility",
        "destination_id": system
    }
    post_waypoint(waypoint_params)
