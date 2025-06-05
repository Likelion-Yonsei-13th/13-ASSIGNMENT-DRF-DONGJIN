import requests
import base64

SPOTIFY_CLIENT_ID = "d489c32c7ebd47b5906451ebfcb037ba"
SPOTIFY_CLIENT_SECRET = "49c6c340bec440b1a4a73eb6c02086d1"


def get_spotify_access_token():
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response.raise_for_status()
    token = response.json().get("access_token")
    return token