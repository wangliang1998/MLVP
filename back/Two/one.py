import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris, make_moons, make_circles, make_blobs
from sklearn.metrics import silhouette_score, homogeneity_completeness_v_measure
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering


def create(num=500,noise=0.5,centers = 3,cluster_std=0.1):
    # 使用make_blobs产生3个簇的数据，使用make_moons产生2个簇的数据
    moons = make_moons(num, noise=noise)
    blobs = make_blobs(num, centers=centers, cluster_std=cluster_std, center_box=(-1, 1))
    global synthetic_data
    synthetic_data = {"moons": moons, "blobs": blobs}
    # 绘制图形
    plt.figure(figsize=(15, 5))
    i = 0
    for name, (X, y) in synthetic_data.items():
        plt.subplot(121 + i)
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap=ListedColormap(['#FF0000']))
        plt.title(name)
        i += 1
    plt.savefig(r"D:\machine_img\two\one\1.png")



def julei(k):
    # 使用K-means算法对数据进行聚类-k=3
    clfs = {}
    for name, (X, y) in synthetic_data.items():
        clf = KMeans(n_clusters=k, n_init=3)
        clf.fit(X)
        clfs[name] = clf
    plt.figure(figsize=(15, 5))
    i = 0
    for name, (X, y) in synthetic_data.items():
        plt.subplot(121 + i)
        plt.scatter(X[:, 0], X[:, 1], c=clfs[name].labels_)
        plt.title(name)
        i += 1
    plt.savefig(r"D:\machine_img\two\one\2.png")


def dbscan(eps = 0.15,min_samples = 5):
    # 使用DBSCAN算法对数据进行聚类
    clfs = {}
    for name, (X, y) in synthetic_data.items():
        clf = DBSCAN(eps=eps, min_samples=min_samples)
        clf.fit(X)
        clfs[name] = clf
    plt.figure(figsize=(15, 5))
    i = 0
    for name, (X, y) in synthetic_data.items():
        plt.subplot(121 + i)
        plt.scatter(X[:, 0], X[:, 1], c=clfs[name].labels_, cmap=ListedColormap(['#FF0000', '#0000FF']))
        h = 0.02
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        plt.title(name)
        i += 1
    plt.savefig(r"D:\machine_img\two\one\3.png")

if __name__ == '__main__':
    create()
    print(synthetic_data)