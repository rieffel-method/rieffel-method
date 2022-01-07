import pandas as pd
import matplotlib as plt
import numpy as np
from sklearn.model_selection import train_test_split
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

def data_visualization():
    df = pd.read_csv("data_set3.csv")
    df.head()
    df.describe()
    df.info()
    df.hist(bins=50)
    train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 42)
    df["Creators"].hist()
    df.plot(kind="scatter", x="Followers", y="Following", alpha=0.1)
    corr_matrix = df.corr()
    corr_matrix["Followers"].sort_values(ascending=False)
    attributes = ["Followers", "Following", "Restaurants", "Creators"]
    scatter_matrix(df[attributes], figsize=(12,8))
    df.plot(kind="scatter", x="Transportation", y="Food")
    label_encoder = LabelEncoder()
    df_encoded = label_encoder.fit_transform(df)
    pca = PCA()
    pca.fit(train_set)
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    d = np.argmax(cumsum >= 0.95) + 1
    pca = PCA(n_components = 0.95)
    X_reduced = pca.fit_transfor(train_set)