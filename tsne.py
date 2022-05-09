import numpy as np
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec
from sklearn.manifold import TSNE
 
# 学習済みモデルを読み込む
m = Doc2Vec.load('./model/2022.05.10.01.03.50:apt-get-install.model')
weights = []
for i in range(0, len(m.docvecs)):
  weights.append(m.docvecs[i].tolist())
weights_tuple = tuple(weights)
X = np.vstack(weights_tuple)
 
# t-SNEで次元圧縮する
tsne_model = TSNE(n_components=2, random_state=0, verbose=2)
np.set_printoptions(suppress=True)
t_sne = tsne_model.fit_transform(X)
 
# クラスタリング済みのデータを読み込む
# with open('drive/My Drive/Colab Notebooks/syosetu/novel_cluster.csv', 'r') as f:
#   reader = csv.reader(f)
#   clustered = np.array([row for row in reader])
#   clustered = clustered.astype(np.dtype(int).type)
#   clustered = clustered[np.argsort(clustered[:, 0])]
#   clustered = clustered.T[1]
 
# グラフ描画
fig, ax = plt.subplots(figsize=(10, 10), facecolor='w', edgecolor='k')
 
# Set Color map
cmap = plt.get_cmap('Dark2')
 
for i in range(t_sne.shape[0]):
  cval = cmap(clustered[i] / 4)
  ax.scatter(t_sne[i][0], t_sne[i][1], marker='.')
  ax.annotate(i, xy=(t_sne[i][0], t_sne[i][1]))
plt.show()