# EVE Waypoint Setter

Creating long routes from a lot of waypoints in EVE Online sucks, they require a lot of manual actions to create. This script allows you to save routes into a file and then automate setting the waypoints by sending POST requests to the /ui/autopilot/waypoint/ endpoint.

## How to use

Steps to make this work:

1. Create an application on the third party developers portal [developers.eveonline.com](developers.eveonline.com)
2. Copy your client id and secret key from the application detail page into config.py
3. Authenicate with your application manually on the character you want to use
4. Generate an access token by following the instructions in the first half of [this article](https://developers.eveonline.com/blog/article/sso-to-authenticated-calls)
5. Copy the access token, refresh token and refresh after timestamp into tokens.json
6. Create your route in routes.txt
7. Install project requirements
8. Run waypoints.py

Your route should now be set in game.
 
### Requirements

```
requests>=2.22.0
```

### Rate limits

Be nice and don't hammer the ESI endpoints or you'll probably get rate limited

### Example output

Setting a waypoint should always return HTTP 204

```
Retrieving tokens from tokens.json
Token is active
Attemping to set destination to 30000140 (Status 204)
Attemping to set destination to 30000143 (Status 204)
Attemping to set destination to 30002789 (Status 204)

Process finished with exit code 0
```