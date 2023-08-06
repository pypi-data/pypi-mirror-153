# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns

# Load Dataset
df = pd.read_csv("./ML LAB/Online Shopping Preferences.csv")
# print("DATASET : \n", df.head(5))
print("DATASET SHAPE : ", df.shape)

df2=df.rename(columns={
   'From how many online shopping websites you have purchased so far (in numerical value) ?': 'websites purchased so far',
   'How many hours do you spend per week for online shopping (in numerical value) ?': 'hours spend per week'
})
df_scale = df2[['websites purchased so far','hours spend per week']]
# print(df_scale.columns)

# Apply Feature Scaling
# scaler = MinMaxScaler()
# scale = scaler.fit_transform(df[['From how many online shopping websites you have purchased so far (in numerical value) ?','How many hours do you spend per week for online shopping (in numerical value) ?']])
# df_scale = pd.DataFrame(scale, columns = ['websites purchased so far','hours spend per week'])
# print("DATASET After Apply Feature Scaling: \n", df.head(5))
# df_scale[['websites purchased so far','hours spend per week']].head(5)

# 1) Elbow Method with Within-Cluster-Sum of Squared Error (WCSS)
K=range(2,12)
wcss = [] 
for k in K:
    kmeans = KMeans(n_clusters = k, init = 'k-means++', random_state = 42) 
    kmeans.fit(df_scale) 
    wcss.append(kmeans.inertia_)

plt.plot(K, wcss) 
plt.xlabel('Number of clusters (K)') 
plt.ylabel('Within-Cluster-Sum of Squared Errors (WSS)') 
plt.show() 

kl = KneeLocator(K, wcss, curve="convex", direction="decreasing")
k_wcss = kl.elbow
print("Optimal K value by WCSS Elbow Method : ", k_wcss)

# 2) The Silhouette Method
silhouette = []
for k in K:
    kmeans = KMeans(n_clusters = k, init = 'k-means++', random_state = 42) 
    kmeans.fit(df_scale) 
    silhouette.append(silhouette_score(df_scale,kmeans.labels_,metric="euclidean",sample_size=1000,random_state=200))

plt.plot(K, silhouette) 
plt.xlabel('Number of clusters (K)') 
plt.ylabel('Silhouette Score') 
plt.show() 

# print(max(silhouette))
k_silh = silhouette.index(max(silhouette)) + 2
print("Optimal K value by The Silhouette Method : ",k_silh) 

k_opt = k_wcss
# Training the K-Means model on the dataset using optimal k value 
kmeans = KMeans(n_clusters = k_opt, init = 'k-means++', random_state = 42) 
y_kmeans = kmeans.fit_predict(df_scale)

df_scale['Clusters'] = kmeans.labels_
ax = sns.scatterplot(data= df_scale, x='websites purchased so far', y='hours spend per week', hue = 'Clusters', palette='viridis', alpha=0.75, s=12)
ax = sns.scatterplot(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], hue=range(k_opt), palette='viridis', s=25, ec='black', legend=False, ax=ax)
plt.show() 

# DUNN INDEX
def delta(ck, cl):
    values = np.ones([len(ck), len(cl)])*10000
    
    for i in range(0, len(ck)):
        for j in range(0, len(cl)):
            values[i, j] = np.linalg.norm(ck[i]-cl[j])
            
    return np.min(values)
    
def big_delta(ci):
    values = np.zeros([len(ci), len(ci)])
    
    for i in range(0, len(ci)):
        for j in range(0, len(ci)):
            values[i, j] = np.linalg.norm(ci[i]-ci[j])
            
    return np.max(values)
    
def dunn(k_list):
    deltas = np.ones([len(k_list), len(k_list)])*1000000
    big_deltas = np.zeros([len(k_list), 1])
    l_range = list(range(0, len(k_list)))
    
    for k in l_range:
        for l in (l_range[0:k]+l_range[k+1:]):
            deltas[k, l] = delta(k_list[k], k_list[l])
        
        big_deltas[k] = big_delta(k_list[k])

    di = np.min(deltas)/np.max(big_deltas)
    return di

cluster_list = []
for k in range(k_opt):
    cluster_list.append(df_scale.loc[df_scale.Clusters == k].values)

print(f'DUNN Index for k value ({k_opt}) : {dunn(cluster_list)}')