import flask
import msal
import json
import sys
import logging
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app) 

authority = "https://login.microsoftonline.com/<tenant-id>"
client_id = "<client-id>"
scope = [ "https://storage.azure.com/.default" ]
secret = "<secret>"
endpoint = "https://storage.azure.com/"

@app.route('/', methods=['GET'])
def home():
    return "response from the API from promgraf with CORS enabled"

@app.route('/token', methods=['GET'])
def fetchToken():
    # Create a preferably long-lived app instance that maintains a token cache.
    app = msal.ConfidentialClientApplication(
    client_id, authority=authority,
    client_credential=secret,
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

    # The pattern to acquire a token looks like this.
    result = None
    token = None

    # First, the code looks up a token from the cache.
    # Because we're looking for a token for the current app, not for a user,
    # use None for the account parameter.
    result = app.acquire_token_silent(scope, account=None)

    if not result:
       logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
       result = app.acquire_token_for_client(scopes=scope)

    if "access_token" in result:
    # Call a protected API with the access token.
       logging.info(result["token_type"])
       logging.info(result["access_token"])
       token = result["access_token"]
    else:
       logging.info(result.get("error"))
       logging.info(result.get("error_description"))
       logging.info(result.get("correlation_id"))  # You might need this when reporting a bug.


    return token

app.run(host='0.0.0.0')
