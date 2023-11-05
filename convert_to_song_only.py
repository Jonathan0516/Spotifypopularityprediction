import pandas as pd
from scrap import get_genres, get_popularity
import traceback
def convert_and_save_to_song_only(df: pd.DataFrame) -> None:

    df = pd.read_csv('datasets/Spotify_Dataset_V3.csv', sep=';')
    df = df.drop_duplicates(subset=['id'])
    columns_to_drop = [ 'Rank', 'Date', '# of Artist', 'Artist (Ind.)', '# of Nationality', 'Nationality', 'Points (Total)' , 'Points (Ind for each Artist/Nat)', 'Song URL']
    df = df.drop(columns_to_drop, axis=1)

    df.to_csv('datasets/song_only.csv', index=False)

def add_genres_to_song_only() -> None:
    df = pd.read_csv('datasets/song_only.csv')
    if 'genres' not in df.columns:
        df['genres'] = None
    try:
        for index, row in df.iterrows():
            # check if genres already exists
            if not pd.isna(row['genres']):
                continue
            genres = get_genres(row['id'])
            df.at[index, 'genres'] = ','.join(genres)
            print("Progress: ", index, "/", len(df) - 1)
    except Exception as e:
        print("Error at index: ", index, " reason: ", e)
        traceback.print_exc()
    finally:
        df.to_csv('datasets/song_only.csv', index=False)

def add_popularity_to_song_only() -> None:
    df = pd.read_csv('datasets/song_only.csv')
    if 'popularity' not in df.columns:
        df['popularity'] = None
    try:
        for index, row in df.iterrows():
            if not pd.isna(row['popularity']):
                continue
            popularity = get_popularity(row['id'])
            df.at[index, 'popularity'] = popularity
            print("Progress: ", index, "/", len(df) - 1)
    except Exception as e:
        print("Error at index: ", index, " reason: ", e)
        traceback.print_exc()
    finally:
        df.to_csv('datasets/song_only.csv', index=False)
# add_genres_to_song_only()
add_popularity_to_song_only()