from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import langid
from sklearn.cluster import KMeans

def create_csv():
  # Load the dataset
  tracks = pd.read_csv('spotify_tracks.csv', nrows=101939)
  
  # Filter out non-English songs
  english_tracks = []
  for name in tracks['name']:
    lang = langid.classify(name)
    if lang == 'en':
      english_tracks.append(True)
    else:
      english_tracks.append(False)
  tracks = tracks[english_tracks]
  
  # Drop duplicates
  tracks.drop_duplicates(subset='name', inplace=True)
  
  # columns for clustering
  X = tracks[['danceability', 'energy', 'loudness', 'key', 'tempo', 'valence']]
  
  # KMeans model
  model = KMeans(n_clusters=10, randomstate=42)
  model.fit(X)
  
  tracks['cluster'] = model.labels
  
  # Calculate the distance between each song and its cluster centroid
  distances = model.transform(X)
  tracks['distance'] = np.min(distances, axis=1)
  
  # Sort by cluster and distance
  sorted_tracks = tracks.sort_values(['cluster', 'distance'], ascending=False)
  
  top_songs = pd.DataFrame(columns=['cluster', 'name', 'distance'])
  
  # top 30 songs from each cluster to the datarame
  for i in range(20):
    top_songs = top_songs.append(
      sorted_tracks[sorted_tracks['cluster'] == i].head(20)[['cluster', 'name']])
  
  top_songs.to_csv('top_songs_by_cluster.csv', index=False)

def recommend(song):
  if song == "":
    top_1 = ""
    return (top_1)
  else:
    tracks = pd.read_csv('top_songs_by_cluster.csv')
    name = song.strip().split(',')
    favorites = tracks[tracks.name.isin(name)]
    cluster_numbers = list(favorites['cluster'])
    clusters = {}
    for num in cluster_numbers:
      clusters[num] = cluster_numbers.count(num)
    
    user_favorite_cluster = [(k, v) for k, v in sorted(clusters.items(), key=lambda item: item[1])][0][0]
    
    suggestions = tracks[tracks.cluster == user_favorite_cluster]
    top = suggestions[['name']].head(1)
    top_1 = top.to_string()
    print(top_1)
    return (top_1)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Home Page
@app.route('/')
def base_page():
  # Only needed to run once
  # create_csv()
  return render_template('base.html')

# Page to trigger the recommendation algorithm
@app.route('/rec')
def recomendation_page():
  song = request.args.get('song')
  rec = recommend(song)
  print("Done")
  return render_template('rec.html', rec = rec, song = song)


app.run(host='0.0.0.0', port=81)
