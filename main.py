from google.colab import drive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

drive.mount('/content/drive/')
file_path = '/content/drive/MyDrive/contact.json'

df = pd.read_json(file_path)

print(df.info())

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
