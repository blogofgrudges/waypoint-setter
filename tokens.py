from datetime import datetime, timedelta
import base64
import config
import json
import requests


def get_tokens_from_file():
    print('Retrieving tokens from ' + config.TOKEN_FILE)

    with open(config.TOKEN_FILE, 'r') as token_file:
        token_data = json.load(token_file)

    if is_access_token_valid(token_data) is False:
        get_new_token(token_data['refresh_token'])

    return token_data


def write_tokens_to_file(token_data):
    token_file = open(config.TOKEN_FILE, 'w')
    token_file.write(json.dumps(token_data, sort_keys=True, indent=4))
    token_file.close()


def is_access_token_valid(token_data):
    if datetime.now() >= datetime.strptime(token_data['refresh_after'], config.DT_FORMAT):
        print('Token has expired')
        return False
    print('Token is active')
    return True


def get_new_token(refresh_token):
    key_pair = (config.CLIENT_ID + ':' + config.SECRET_KEY).encode('utf-8')
    request_headers = {'Content-Type': 'application/json',
                       'Authorization': 'Basic ' + base64.b64encode(key_pair).decode('utf-8')}
    request_body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    print('Attemping to get new access token ', end='')
    token_uri = 'https://login.eveonline.com/oauth/token'
    response = requests.post(token_uri, data=json.dumps(request_body), headers=request_headers)
    print('(Status ' + str(response.status_code) + ')')

    token_data = {
        "access_token": response.json()['access_token'],
        "refresh_token": response.json()['refresh_token'],
        "refresh_after": (datetime.now() + timedelta(seconds=response.json()['expires_in'])).strftime(config.DT_FORMAT)
    }
    write_tokens_to_file(token_data)
    return token_data
