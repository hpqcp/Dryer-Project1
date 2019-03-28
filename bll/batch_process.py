##
##
##

class silk_batch():
    def __init__(self, name):
        self.name = name






    def __kmeans_building(x1, x2, types_num, types, colors, shapes, _isPlot=False):
        X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
        # KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,n_clusters=3, n_init=10, n_jobs=None, precompute_distances='auto',random_state=None, tol=0.0001, verbose=0)
        kmeans_model = KMeans(n_clusters=types_num).fit(X)  # 设置聚类数n_clusters的值为types_num
        # 整理分类好的原始数据, 并画出聚类图
        x1_result = [];
        x2_result = []
        for i in range(types_num):
            temp = [];
            temp1 = []
            x1_result.append(temp)
            x2_result.append(temp1)
        for i, l in enumerate(kmeans_model.labels_):  # 画聚类点
            x1_result[l].append(x1[i])
            x2_result[l].append(x2[i])
            plt.scatter(x1[i], x2[i], c=colors[l], marker=shapes[l])
        for i in range(len(list(kmeans_model.cluster_centers_))):  # 画聚类中心点
            plt.scatter(list(list(kmeans_model.cluster_centers_)[i])[0],
                        list(list(kmeans_model.cluster_centers_)[i])[1],
                        c=colors[i], marker=shapes[i], label=types[i])
        if (_isPlot == True):
            plt.legend()
            plt.show()
        return kmeans_model, x1_result, x2_result


