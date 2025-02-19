# -*- coding: utf-8 -*-

import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans

class KmeansClustering():
    def __init__(self, stopwords_path=None):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()

    def load_stopwords(self, stopwords=None):
        """
        加载停用词
        :param stopwords:
        :return:
        """
        if stopwords:
            with open(stopwords, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f]
        else:
            return []

    # 当然这里也可以直接改成每个文件一个文本
    def preprocess_data(self, corpus_path):
        """
        文本预处理，每行一个文本
        :param corpus_path:
        :return:
        """
        corpus = []
        with open(corpus_path, 'r', encoding='utf-8') as f:
            # 加每一行文字
            for line in f:
                corpus.append(' '.join([word for word in jieba.lcut(line.strip()) if word not in self.stopwords]))
        return corpus

    def get_text_tfidf_matrix(self, corpus):
        """
        获取tfidf矩阵
        :param corpus:
        :return:
        """
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))

        # 获取词袋中所有词语
        # words = self.vectorizer.get_feature_names()

        # 获取tfidf矩阵中权重
        weights = tfidf.toarray()
        return weights

    def kmeans(self, corpus_path, n_clusters=5):
        """
        KMeans文本聚类
        :param corpus_path: 语料路径（每行一篇）,文章id从0开始
        :param n_clusters: ：聚类类别数目
        :return: {cluster_id1:[text_id1, text_id2]}
        """
        corpus = self.preprocess_data(corpus_path)
        weights = self.get_text_tfidf_matrix(corpus)
        clf = KMeans(n_clusters=n_clusters)
        # clf.fit(weights)
        y = clf.fit_predict(weights)
        # 中心点
        # centers = clf.cluster_centers_
        # 用来评估簇的个数是否合适,距离约小说明簇分得越好,选取临界点的簇的个数
        # score = clf.inertia_
        # 每个样本所属的簇
        result = {}
        for text_idx, label_idx in enumerate(y):
            if label_idx not in result:
                result[label_idx] = [text_idx]
            else:
                result[label_idx].append(text_idx)
        return result

# 关于原数据的说明——这玩意每一行就是一条新闻
if __name__ == '__main__':
    Kmeans = KmeansClustering(stopwords_path='stop_words.txt')
    result = Kmeans.kmeans('total.txt', n_clusters=5)
    print(result)
    # print(type(result))
    news_data = []
    with open('total.txt','r',encoding='utf-8') as f:
        line = f.readline()
        while line:
            # print(line.decode())
            news_data.append(line)
            line = f.readline()

    for k,v in result.items():
        f = open('%s.txt' % k,'w',encoding='utf-8')
        for num in v:
            # print(news_data[num])
            # print(type(news_data[num]))
            f.write(news_data[num])
        f.close()