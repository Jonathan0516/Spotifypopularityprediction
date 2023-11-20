import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.inspection import permutation_importance
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score, silhouette_score, davies_bouldin_score, f1_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from enum import Enum
from sklearn.decomposition import PCA
warnings.filterwarnings("ignore")
song_data = pd.read_csv('datasets/Spotify_Dataset_V3.csv', delimiter=';')
song_data_copy=song_data.copy()
song_data_copy = song_data_copy.sample(n=6000, random_state=42)
song_data_copy['date_column'] = pd.to_datetime(song_data_copy['Date'])
song_data_copy['month'] = song_data_copy['date_column'].dt.month
song_data_copy.drop('date_column', axis=1, inplace=True)
song_data_copy.drop(columns=['Rank','Points (Ind for each Artist/Nat)','id','Song URL','# of Nationality','# of Artist'])
numeric_data = song_data_copy.select_dtypes(include=['int64', 'float64'])
categorical_data = song_data_copy.select_dtypes(include=['object'])

# categorical_columns = song_data.select_dtypes(include=['object']).columns
# song_rank = pd.get_dummies(song_data, columns=categorical_columns)
scaler = StandardScaler()
scaled_numeric_data = pd.DataFrame(scaler.fit_transform(numeric_data), columns=numeric_data.columns)

encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
encoded_categorical_data = pd.DataFrame(encoder.fit_transform(categorical_data), columns=encoder.get_feature_names_out(categorical_data.columns))
# Ensure the indices are aligned before concatenation
scaled_numeric_data.reset_index(drop=True, inplace=True)
encoded_categorical_data.reset_index(drop=True, inplace=True)
# Concatenate along the columns
final_data = pd.concat([scaled_numeric_data, encoded_categorical_data], axis=1)
X_feature_importance=final_data.drop(columns=['Points (Total)'])
y_feature_importance=final_data['Points (Total)']
####split the dataset to training sets and test sets
X_train, X_test, y_train, y_test = train_test_split(X_feature_importance, y_feature_importance, test_size=0.2, random_state=42)
###train the model first
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
####predict using the model
baseline_mse = mean_squared_error(y_test, model.predict(X_test))
print(f"Baseline Mean Squared Error: {baseline_mse:.4f}")

######calculate permutation importance
perm_importance = permutation_importance(model, X_test, y_test, n_repeats=30, random_state=42)
sorted_idx = perm_importance.importances_mean.argsort()
for i in sorted_idx[::-1]:  # Reverse the order to display most important features first
    print(f"Feature {X.columns[i]}: {perm_importance.importances_mean[i]:.4f}")

# Optional: Convert to a DataFrame for better visualization
feature_importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance_mean': perm_importance.importances_mean,
    'importance_std': perm_importance.importances_std
}).sort_values(by='importance_mean', ascending=False)

print(feature_importance_df)