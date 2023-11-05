import requests
import json

Users = [
    
    {
        'client_id': '9d13407a5dda4659b35e1171a567d405',
        'redirect_uri': 'https://localhost:99',
        'client_id': 'e5747d6bba9545f787c0b56135341b93',
        'redirect_uri': 'https://localhost:99',
    },
    [   
        'e5747d6bba9545f787c0b56135341b93',
        'a3c4ea38a9524dbaac945c3d147824a1',
        'ce967a29c829468fbb5c959181289ee3',
        '542a554fb05a4056a3865e446c7f9d1a',
        'f795c42fd49547f6a226099f4c53246c',
        '84f7a38b02514b07b11f3112f048ad8f',
    ]
]

def get_genres(id: str) -> list[str]:
# id = "2UW7JaomAMuX9pZrjVpHAU"
    track_url = "https://api.spotify.com/v1/tracks/"
    audio_features_url = "https://api.spotify.com/v1/audio-features/"
    album_url = "https://api.spotify.com/v1/albums/"
    artists_url = "https://api.spotify.com/v1/artists?ids="
    access_token = "BQDM6kIpMQtUCoWaVAZNLr41pV6gNZoM2Gjjy_3Ibh__E03jzR0VP1F7ozmLK4xH7tVC9mbsI0QtBAMDtSFHk34iTBtU6m2syoSeE6FkRVL748mdqn9cTBeqmBnkBcRT08MYaDRR31xJXfHL-1wAjTpaOibJBDzhGx46LwDcJ4XhJZkeCRkSpOFWOfl2Y8bUmW0"
    code = "AQAjxJCqu1a80TZAgpruE6EblYXHHQf7yi0j25Ll-aVnARoT35OD_WxmAqmMH0Qg0G5CXmvdMz75EGyu9nyi1IvI9J-RiVe-0h7aaeYR9OGMbOYWn9_O7Qz46kBSuxyuj561_OtMkXz-zIHap2jTivVebTTXpI4h"
    authorize_url = f"https://accounts.spotify.com/authorize?client_id=84f7a38b02514b07b11f3112f048ad8f&redirect_uri=https://localhost:99&response_type=token"

    headers = {"Authorization": "Bearer " + access_token}

    track_res = requests.get(track_url + id, headers=headers)
    if track_res.status_code != 200:
        raise Exception("Error: ", track_res.status_code, track_res.text)
    track_json = json.loads(track_res.text)

    song_genres = set()
    artist_ids = []
    for artist in track_json['artists']:
        artist_ids.append(artist['id'])

    artists_res = requests.get(artists_url + ",".join(artist_ids), headers=headers)
    if artists_res.status_code != 200:
        raise Exception("Error: ", artists_res.status_code, artists_res.text)
    artists_json = json.loads(artists_res.text)
    for artist in artists_json['artists']:
        if artist['genres']:
            song_genres.update(artist['genres'])

    album_id = track_json['album']['uri'].split(":")[2]
    album_res = requests.get(album_url + album_id, headers=headers)
    if album_res.status_code != 200:
        raise Exception("Error: ", album_res.status_code, album_res.text)
    album_json = json.loads(album_res.text)
    if 'genres' in album_json and album_json['genres'] != []:
        song_genres.update(album_json['genres'])
    return list(song_genres)


