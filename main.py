from privkey import CLIENT_ID, CLIENT_SECRET
import base64 
from requests import post, get
import json

client_id = CLIENT_ID
client_secret = CLIENT_SECRET

def get_token():
    url = "https://accounts.spotify.com/api/token"
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth_str}"}
    payload = {"grant_type": "client_credentials"}
    response = post(url, headers=headers, data=payload)
    return response.json()["access_token"]

def search_artists(token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    parama = {"q": "genre:rai", "type": "artist", "market": "DZ", "limit": 50}
    response = get(url, headers=headers, params=parama)
    return response.json()

def save_artists(artists):
    with open("artists.json", "w") as f:
        json.dump(artists, f, indent=4)

def json_to_csv():
    with open("artists.json") as f:
        artists = json.load(f)
    with open("artists.csv", "w") as f:
        for artist in artists["artists"]["items"]:
            f.write(f"{artist['name']};{artist['popularity']}\n")

def sort_csv():
    with open("artists.csv") as f:
        artists = f.readlines()
    artists = [artist.strip().split(";") for artist in artists]
    artists = sorted(artists, key=lambda x: int(x[1]), reverse=True)
    with open("artists.csv", "w") as f:
        for artist in artists:
            f.write(f"{artist[0]};{artist[1]}\n")

def main():
    token = get_token()
    artists = search_artists(token)
    save_artists(artists)
    json_to_csv()
    sort_csv()

if __name__ == "__main__":
    main()