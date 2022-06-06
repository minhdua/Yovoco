import typer
from utils import displayutils

class UserDetails:
    def __init__(self, username = None, email = None, avartar = None, mobile_number = None, first_name = None, last_name = None, address = None, city = None, country = None, postal_code = None, birthday = None):
        self.username = username
        self.email = email
        self.avartar = avartar
        self.mobile_number = mobile_number
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.country = country
        self.postal_code = postal_code
        self.birthday = birthday
        
    def display(self):
        displayutils.emphasize("Username: {}".format(self.username))
        displayutils.emphasize("Email: {}".format(self.email))
        displayutils.emphasize("avartar: {}".format(self.avartar))
        displayutils.emphasize("Mobile number: {}".format(self.mobile_number))
        displayutils.emphasize("First name: {}".format(self.first_name))
        displayutils.emphasize("Last name: {}".format(self.last_name))
        displayutils.emphasize("Address: {}".format(self.address))
        displayutils.emphasize("City: {}".format(self.city))
        displayutils.emphasize("Country: {}".format(self.country))
        displayutils.emphasize("Postal code: {}".format(self.postal_code))
        displayutils.emphasize("Birthday: {}".format(self.birthday))
        
def userdetail_from_json(json_data: dict):
    user = UserDetails();
    user.username = json_data.get("username")
    user.email = json_data.get("email")
    user.avartar = json_data.get("avartar")
    user.mobile_number = json_data.get("mobile_number", None)
    user.first_name = json_data.get("first_name")
    user.last_name = json_data.get("last_name")
    user.address = json_data.get("address")
    user.city = json_data.get("city")
    user.country = json_data.get("country")
    user.postal_code = json_data.get("postal_code")
    user.birthday = json_data.get("birthday")
    return user