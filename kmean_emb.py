# -*- coding: utf-8 -*-

import numpy as np
from numpy import *
import sys # sys.stdout.flush()
import time
import matplotlib.pyplot as plt


# calculate Euclidean distance
# e.g. sqrt(sum(power(matrix([2, 3]) - matrix([4, 5]), 2))) == 2.8
def euclDistance(vector1, vector2):
    return sqrt(sum(np.power(vector2 - vector1, 2)))


# init centroids with random samples
# return centroids - k row
def initCentroids(dataSet, k):
    sample_count, dim = dataSet.shape
    centroids = zeros((k, dim))
    for i in range(k):
        index = int(np.random.uniform(0, sample_count))
        centroids[i, :] = dataSet[index, :]
    # 一共返回k行 随机的centroids
    return centroids


def kmeans(dataset, k, max_iter):
    print('k = ', k)

    items = list(dataset.items())
    sample_count = len(items)
    vector_len = len(items[0][1])

    # node_id与dataSet及clusters的每一行对应
    node_ids = np.arange(sample_count, dtype = np.integer)
    dataSet = np.arange(sample_count * vector_len, dtype = np.float32).reshape(sample_count, vector_len)

    for i in range(sample_count):
        node_ids[i] = items[i][0]   # node_id
        for j in range(vector_len):
            dataSet[i][j] = items[i][1][j]

    # return clusters
    # first column stores which cluster this sample belongs to,             
    # second column stores the error between this sample and its centroid
    # 
    # 每行对应于每个sample
    # col0 - 属于第几个cluster
    # col1 - 这个sample与对应的centroid的距离平方，也就是所谓square error
    clusters = np.matrix(zeros((sample_count, 2)))    

    # 只有在step3 有cluster被更新后才需要重新计算
    # 如果没人跳槽说明已经收敛到稳定状态
    changed = True

    ## step 1: init centroids
    centroids = initCentroids(dataSet, k)

    iter_count = 0
    while changed:
        changed = False

        # 根据当前的每个centroids调整所有sample的分类和err
        '''
        循环每个sample：
            1. in each iteration, 循环k个centroid：
                    找到离这个sample最近的centroid，计算修改距离(err); 
            2. 如果跳槽，修改clusters[i, [cluster#, err]]
        '''
        for i in range(sample_count):            
            minIndex = "计算本轮距离这个sample最近的centroid的index"
            minDist = sys.maxsize # distance between this point to its centroid (err)

            # step 2: find the centroid who is closest
            for j in range(k):
                # 第j个centroid与第i个sample的距离
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist  = distance
                    minIndex = j

            # step 3: update its cluster
            if clusters[i, 0] != minIndex:              # 第0列是这个sample的cluster号
                clusters[i, :] = minIndex, minDist**2   # 注意是距离平方，non-negative
                changed = True                          # 有人跳槽了，得调整新的

        '''
        根据当前所有sample的位置，调整每个centroid
        '''
        ## step 4: update centroids
        for i in range(k):
            # 所有属于第j个cluster的samples的行号 -> acluster
            # clusters[:, 0].A表示取出每一行的第0列并转换为array  (col0 - 这个sample属于第几个cluster)
            # (clusters[:, 0].A == i) : 如果col0==第j个cluster就是[True], 否则是[False]， 返回一个array
            # nonzero(...)[0] : 返回所有True的行号，一个1D array
            acluster = nonzero(clusters[:, 0].A == i)[0]
            
            # 从dataset中取出行数in acluster的那些samples
            samples_in_cluster = dataSet[acluster]

            #                       按列求mean，变成一行?列
            # 更新第j个centroid
            if (samples_in_cluster.size > 0):
                centroids[i, :] = mean(samples_in_cluster, axis = 0)

        if iter_count >= max_iter:
            break
        iter_count += 1
        print('.', end='')
        sys.stdout.flush()
    print( '\nclustering complete! ', 'centroids.shape: ', centroids.shape, ', clusters.shape:', clusters.shape)

    cluster_map = dict()
    for i in range(len(node_ids)):
        cluster_id = int(clusters.A[i][0])
        if cluster_map.get(cluster_id) == None:
            cluster_map[cluster_id] = [node_ids[i]]
        else:
            cluster_map[cluster_id].append(node_ids[i])
    return centroids, clusters, cluster_map

def random_clustering(dataset, k):
    items = list(dataset.items())
    sample_count = len(items)
    cluster_len = sample_count // k
    cluster_map = dict()
    sample_index = 0
    for i in range(k):
        cluster = list()
        for j in range(cluster_len):
            if sample_index >= len(items):
                break
            cluster.append(items[sample_index][0])
            sample_index += 1
        if len(cluster) > 0:
            cluster_map[i] = cluster
    # put the reminders into clusters[0]
    if sample_index < len(items) - 1:
        if len(cluster_map) == 0:
            cluster = list()
            cluster_map[0] = cluster
        while sample_index < len(items):
            cluster_map[0].append(items[sample_index][0])
            sample_index += 1
    return cluster_map        

def load_emb(filename):
    print( "step 1: load .emd..."  )
    sys.stdout.flush()

    dataset = dict()
    emb_file = open(filename, 'r')
    segs = emb_file.readlines(1)
    segs = segs[0].split(' ')
    node_count = int(segs[0])
    vector_len = int(segs[1])
    lines = emb_file.readlines()
    for i in range(node_count):
        line = lines[i]
        line = line.split(' ')
        node_id = int(line[0])
        vector = np.arange(vector_len, dtype = np.float32)
        for j in range(vector_len):
            vector[j] = float(line[j+1])
        dataset[node_id] = vector
    emb_file.close()
    return dataset

def save_clusters(cluster_map, filename):
    clusters_file = open(filename, 'w')
    for cluster_id, nodes in cluster_map.items():
        clusters_file.write(str(cluster_id))
        clusters_file.write('\n')
        node_ids = ''
        for node_id in nodes:
            node_ids += (str(node_id) + ' ')
        node_ids = node_ids.strip()
        clusters_file.write(node_ids)
        clusters_file.write('\n')
    clusters_file.close()

if __name__ == '__main__':
    filename = './data/tt.txt.emd'
    k = 3
    max_iter = 200
        
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    dataset = load_emb(filename)

    items = list(dataset.items())
    node_count = len(items)
    vector_len = len(items[0][1])
    print('node_count:', node_count)
    print('vector_len:', vector_len)

    # clustering result
    centroids, clusters, cluster_map = kmeans(dataset, k, 300)
    save_clusters(cluster_map, filename + '.clusters')

    # randomly grouping result
#    cluster_map = random_clustering(dataset, k)
#    save_clusters(cluster_map, filename + '.random.clusters')
