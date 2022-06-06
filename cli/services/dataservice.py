import json

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)
        
def load_data():
    with open('data.json', 'r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError as e:
            type.echo("Error: {}".format(e))
        return data
    
def get_refresh_token():
   data = load_data()
   return data["refresh_token"]
    
def get_access_token() :
    data = load_data()
    return data["access_token"]
    