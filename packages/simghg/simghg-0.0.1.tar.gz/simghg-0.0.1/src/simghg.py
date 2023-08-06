# モジュール読み込み
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering


# データ取得
url = 'https://www.nies.go.jp/gio/aboutghg/index.html#e'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
hrefs = [elem['href'] for elem in soup.find('div',id='block2').find_all('a')]
if hrefs:
    url = urljoin(url, hrefs[0])

# dfのラベル
labels = [str(i) for i in range(1990, 2020)]
labels.insert(0, '-')
labels.insert(1, 'Country')
labels.insert(2, 'Base year')
labels.insert(33, '-')

# N2O
df = pd.read_excel(url, sheet_name='N2O total without LULUCF',header=4, names=labels)
df = df.drop(df.columns[[0, 33]], axis=1)
df = df.drop(df.index[[45, 46, 47, 48, 49, 50]])
df_n2o = df.drop(['Country', 'Base year'], axis=1)
# 前年度との差
n2o_diff = df_n2o.diff(axis=1)
diff = n2o_diff.drop('1990', axis=1)

# 変化量を正規化
ss = preprocessing.MinMaxScaler()
n2o_diff_std = ss.fit_transform(diff)

# クラスタリング
cluster = AgglomerativeClustering(affinity='euclidean', linkage='ward',
                                  distance_threshold=1.5, n_clusters=None)
cluster.fit(n2o_diff_std.T)

cluster_labels = cluster.labels_.tolist()

# クラスタリングされたラベルをまとめる
cluster_list = []
for n in range(cluster.n_clusters_):
  same_cluster = [i for i, x in enumerate(cluster_labels) if x == n]
  if same_cluster not in cluster_list:
    cluster_list.append(same_cluster)

# 国名でまとめる
cluster_country = []
for l in cluster_list:
  for i, label in enumerate(l):
    l[i] = df.iloc[label].Country
  cluster_country.append(l)


def n2o_cluster(country):
  for l in cluster_list:
    if country in l:
      target_cluster = l

  df_country = df[['Country']]
  plot_df = df_country.join(n2o_diff)

  x = np.arange(1990, 2020)
  plt.figure(figsize=(10,7))
  for country in target_cluster:
    y = plot_df[plot_df.Country == country].values[0][1:]
    plt.plot(x, y, label=country)
  plt.xlabel('Y e a r', fontsize=12)
  plt.ylabel('k t', fontsize=12)
  plt.legend(fontsize=15)
  plt.grid()
  plt.savefig('../result_n2o.png')
  plt.show()


def main():
  print('Draw countries with similar N2O changes.')
  country = input('Country Name >>> ')
  n2o_cluster(country)

if __name__ == '__main__':
  main()
