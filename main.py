from google.colab import drive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import folium

drive.mount('/content/drive/')
file_path = '/content/drive/MyDrive/contact.json'

df = pd.read_json(file_path)

print(df.info())

df = df[df['latitude'] < 90]
df['timestamp'] = pd.to_datetime(df['timestamp'])

samples = df['id'].sample(5).unique()
df_sample = df[df['id'].isin(samples)]

print(f'data duration : {df['timestamp'].min()} to {df['timestamp'].max()}')


df['hour'] = df['timestamp'].dt.hour
plt.figure(figsize = (10, 10))
sns.histplot(data = df, x = 'hour')
plt.show()



plt.figure(figsize = (10, 10))
sns.scatterplot(data = df_sample, x = 'latitude', y = 'longitude', hue = 'id')
plt.legend(bbox_to_anchor = (1.05, 1), loc = 2)
plt.show()

eps = 20 / 6378000
position = df[['latitude', 'longitude']].apply(np.radians)
dbscan = DBSCAN(min_samples = 2, eps = eps, algorithm = 'ball_tree', metric = 'haversine')
dbscan.fit(position)

df['clusters'] = dbscan.labels_

score = silhouette_score(position, dbscan.labels_, metric = 'haversine')
print(score)

def get_color(cluster) :
if cluster == -1 :
  return 'grey'
elif cluster == 0 :
  return 'red'
elif cluster == 1 :
  return 'blue'
elif cluster == 2 :
  return 'green'
elif cluster == 3 :
  return 'orange'
else :
  return 'yellow'


avg_lat = df['latitude'].mean()
avg_long = df['longitude'].mean()

map = folium.Map(location = [avg_lat, avg_long], zoom_start = 12)

for _, row in df.iterrows() :
 folium.CircleMarker(
    location = [row['latitude'], row['longitude']],
    radius = 3,
    color = get_color(row['clusters']),
    fill = True,
    fill_color = get_color(row['clusters']),
    tooltip = f' user : {row['id']},\n cluster : {row['clusters']}'
).add_to(map)
map
