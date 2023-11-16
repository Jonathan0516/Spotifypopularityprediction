import pandas as pd
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CUR_DIR, 'datasets')

song_data = pd.read_csv(os.path.join(DATASET_DIR, 'song_only.csv'))
new_columns = ["genres","popularity","key","liveness","mode","tempo","time_signature","duration_ms"]

Spotify_data = pd.read_csv(os.path.join(DATASET_DIR, 'Spotify_Dataset_V3.csv'))

if not all(column in Spotify_data.columns for column in new_columns):
    for column in new_columns:
        Spotify_data[column] = None

for idx, row in Spotify_data.iterrows():
    song_id = row['id']
    song_data_row = song_data.loc[song_data['id'] == song_id]
    
    song_data_row = song_data_row.iloc[0]
    
    for column in new_columns:
        Spotify_data.at[idx, column] = song_data_row[column]
        
    print("Progress: ", idx, "/", len(Spotify_data) - 1)
    
# save to csv
Spotify_data.to_csv(os.path.join(DATASET_DIR, 'Spotify_Dataset_V4.csv'), index=False)