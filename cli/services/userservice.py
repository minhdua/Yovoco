import typer
import requests
from . import dataservice
import enum
from models import usermodels
import json
from utils import datautils

BASE_URL = "http://localhost:8000/api/v1"

PROFFILE_URL = BASE_URL + "/profile"
LOGIN_URL = BASE_URL + "/login"
REFRESH_TOKEN_URL =  BASE_URL + "/refresh"
CREATE_USER_URL =  BASE_URL + "/registration"
LOGOUT_URL =  BASE_URL + "/logout"
LOGOUT_VERYWHERE_URL =  BASE_URL + "/logout-everywhere"
REVERIFY_MAIL_URL = BASE_URL + "/reverify-email"
UPDATE_PROFILE_URL = BASE_URL + "/update-profile"
UPDATE_PASSWORD_URL = BASE_URL + "/change-password"

CONNECTION_ERROR = "Connection error"

class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    

def header_default():
    return {"Content-Type": "application/json",
            "Accept": "application/json"
            }
    
def header_token():
    return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {dataservice.get_access_token()}"
            }

def send_request(url,method,headers,data):
    data = json.dumps(data)
    try:
        if method == HttpMethod.GET:
            response = requests.get(url,headers=headers,data=data)
        elif method == HttpMethod.POST:
            response = requests.post(url,headers=headers,data=data)
        elif method == HttpMethod.PUT:
            response = requests.put(url,headers=headers,data=data)
        else:
            response = requests.delete(url,headers=headers,data=data)
        if response.status_code >= 400:
            typer.echo(response.data['detail'])
            raise typer.Exit(1)
        return response
    except requests.exceptions.RequestException as e:
        typer.echo("Error: {}".format(e))
        raise typer.Exit(1)

def get_profile():
    return send_request(PROFFILE_URL, HttpMethod.GET, header_token(), None)
    
def request_login(username, password):
    # send request to login
    return send_request(LOGIN_URL, HttpMethod.POST, header_default(), {"username":username,"password":password})
    
def request_refresh_token():
    access_token = dataservice.get_access_token()
    if access_token is None:
        typer.echo("Error: Can't access to system. Please login again.")
        raise typer.Exit(1)
    refresh_token = dataservice.get_refresh_token()
    return send_request(REFRESH_TOKEN_URL, HttpMethod.POST, header_default(), {"refresh_token":refresh_token})
    
def request_create(username, email, password, password2):
    return send_request(CREATE_USER_URL, HttpMethod.POST, header_default(), {"username":username,"email":email,"password":password,"password2":password2})

def logout():
    refresh_token = dataservice.get_refresh_token()
    return send_request(LOGOUT_URL, HttpMethod.DELETE, header_default(), {"refresh_token":refresh_token})

def logout_verywhere():
    return send_request(LOGOUT_VERYWHERE_URL, HttpMethod.DELETE, header_token(), None)

def update_profile(user: usermodels.UserDetails):
    data = json.loads(json.dumps(user.__dict__))
    data = {k: v for k, v in data.items() if v}
    return send_request(UPDATE_PROFILE_URL, HttpMethod.PUT, header_token(), data)

def reverify_email(username, email):
    return send_request(REVERIFY_MAIL_URL, HttpMethod.POST, header_default(), {"username":username,"email":email})

def change_password(old_password, new_password, new_password2):
    return send_request(UPDATE_PASSWORD_URL, HttpMethod.PUT, header_token(), {"old_password":old_password,"new_password":new_password,"new_password2":new_password2})