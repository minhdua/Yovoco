from sre_parse import expand_template
import typer
from services import dataservice, userservice
from models import usermodels
from copy import deepcopy

user_app = typer.Typer()

@user_app.command(help="Get user info")
def whoami():
    response = userservice.get_profile()
    if response.status_code == 200:
        json_data = response.json().get("results")
        user = usermodels.userdetail_from_json(json_data)
        user.display()
        raise typer.Exit(0)
    typer.echo("Error: {}".format(response.reason))
    raise typer.Exit(1)
    
    
@user_app.command(help="Login to the system")
def login(username: str = typer.Option(None, "--username", "-u", prompt_required=True)):
    # define username. if not defined, prompt for it. If it is empty, exit with error
    if username is None:
        username = typer.prompt("Username")
        if username is None:
            raise typer.Errors("Username is required").exit(code=1)
    # input password. If password empty, prompt again 3 times
    time = 0;
    while time < 3:
        password = typer.prompt("Password", hide_input=True)
        if password is None:
            if time == 3:
                raise typer.Abort("Too many attempts")
            typer.echo("Password is required. Try again.")
        else:
            break
        time += 1
    
    # send request to login
    response = userservice.request_login(username, password)
    # if login success, save access token to data.json
    if (response.status_code == 200):
        content = response.json()
        data = dataservice.load_data()
        data.update({
            "access_token": content.get('results').get('access'),
            "refresh_token": content.get('results').get('refresh')
        })
        # save data to data.json file
        dataservice.save_data(data)
        # echo message
        typer.echo(content.get('detail')) 
        raise typer.Exit(code=0)
    typer.echo("Login failed")
    raise typer.Exit(code=1)

@user_app.command(help="Create a new user")
def create(username: str = typer.Argument(...,metavar="username"),
           email:str = typer.Argument(...,metavar="email"),
           password:str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True),
           ):
    response = userservice.request_create(username, email, password, password)
    if response.status_code == 201:
        typer.echo(response.json().get('detail'))
        raise typer.Exit(0)
    typer.echo("Error: {}".format(response.reason))
    raise typer.Exit(1)

@user_app.callback()
def refresh_token(ctx: typer.Context):
    # refresh token each time the app is started
    if ctx.invoked_subcommand not in ("login", "create", "logout"):
        response = userservice.request_refresh_token()
        if response.status_code == 200:
            content = response.json()
            data = dataservice.load_data()
            data.update({
            "access_token": content.get('results').get('access'),
            "refresh_token": content.get('results').get('refresh')
            })
            # save data to data.json file
            dataservice.save_data(data)
        else:
            typer.echo("You need to login again", err=True)
            typer.Exit(code=1)
 
@user_app.command(help="logout of the system")   
def logout(all: bool = typer.Option(False, "--all", "-a")):
    if all:
        response = userservice.logout_verywhere()
    else:
        response = userservice.logout()
        
    if response.status_code == 200:
            typer.echo(response.json().get('detail'))
            data = dataservice.load_data()
            data["access_token"] = None
            dataservice.save_data(data)
            raise typer.Exit(0)
    typer.echo("Error: {}".format(response.reason))
    raise typer.Exit(1)

@user_app.command("verify-email", help="Verify user email")
def verify_email(username: str = typer.Option(..., "--username", "-u", prompt_required=True),
                 email: str =  typer.Option(..., "--email", "-e", prompt_required=True)):
    response = userservice.reverify_email(username, email)
    if response.status_code == 201:
        typer.echo(response.json().get('detail'))
        raise typer.Exit(0)
    typer.echo("Error: {}".format(response.reason))
    raise typer.Exit(1)

@user_app.command("update-profile", help="Update user profile")
def update_profille(email: str = typer.Option(None, "--email", "-e"),
                 first_name: str =  typer.Option(None, "--first-name", "-f"),
                 last_name: str =  typer.Option(None, "--last-name", "-l"),
                 phone: str =  typer.Option(None, "--phone", "-p"),
                 address: str =  typer.Option(None, "--address", "-a"),
                 city: str =  typer.Option(None, "--city", "-c"),
                 postal_code: str =  typer.Option(None, "--postal-code", "-p"),
                 country: str =  typer.Option(None, "--country", "-co"),
                 avatar: str =  typer.Option(None, "--avatar", "-av"),
                 birthday: str =  typer.Option(None, "--birthday", "-b")
                 ):
    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'mobile_number': phone,
        'address': address,
        'city': city,
        'postal_code': postal_code,
        'country': country,
        'avatar': avatar,
        'birthday': birthday
    }
    user = usermodels.userdetail_from_json(data)
    response = userservice.update_profile(user)
    if response.status_code == 200:
        typer.echo(response.json().get('detail'))
        raise typer.Exit(0)
    typer.echo("Error: {}".format(response.reason))
    raise typer.Exit(1)                

@user_app.command("update-password", help="Update user password")
def update_password(old_password: str = typer.Option(..., "--old-password", "-op", prompt=True, hide_input=True),
                    new_password: str = typer.Option(..., "--new-password", "-np", prompt=True, confirmation_prompt=True, hide_input=True)):
    response = userservice.change_password(old_password, new_password, new_password)
    if response.status_code == 200:
        typer.echo(response.json().get('detail'))
        raise typer.Exit(0)
    typer.echo("Error: {}".format(response.reason))
    raise typer.Exit(1)    

if __name__ == "__main__":
    user_app()