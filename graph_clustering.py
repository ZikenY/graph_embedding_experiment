from math import *
import numpy as np
import re
import matplotlib.pyplot as plt
import sys

def cluster_varience(clusters):
    cluster_count = len(clusters)
    # compute the varience between clusters
    avg_nodes = 0
    for i in range(cluster_count):
        avg_nodes += len(clusters[i])
    avg_nodes = avg_nodes * 1.0 / cluster_count
    varience = 0.0
    for i in range(cluster_count):
        varience += (len(clusters[i]) - avg_nodes)**2
    return sqrt(varience)

def interconnection(adjacent, clusters):
    picked = set()
    count = 0
    node_count = len(adjacent)
    cluster_count = len(clusters)
    for i in range(cluster_count):
        c_i = list(clusters[i])
        for j in range(len(c_i)):
            # check adjcents for each c_i[j] to see how many of them are on other clusters
            for n in range(node_count):
                if c_i[j] in adjacent:
                    adj_set = adjacent[c_i[j]]
                    if n in adj_set and not n in clusters[i] and not (c_i[j], n) in picked:
                        count += 1
                        picked.add((c_i[j], n))
                        picked.add((n, c_i[j]))
        print('.', end='')
        sys.stdout.flush()
    return count

def list2cluster(nodes):
    cluster = set()
    for i in range(len(nodes)):
        cluster.add(nodes[i])
    return cluster

def reconcile_mean(varience, inter):
    varience_factor = 1.0
    inter_factor = 1.0
    return varience_factor * varience + inter_factor * inter

def load_clusters(filename):
    clusters = list()
    file = open(filename)
    while True:
        line = file.readline().strip()
        if line == '':
            break
        line = file.readline().strip()
        nodes = line.split(' ')
        cluster = set()
        for node in nodes:
            cluster.add(int(node))
        clusters.append(cluster)
    file.close()
    return clusters

def adj_node(adjacent, node_id, adj_id):
    if adjacent.get(node_id) == None:
        adj_set = set()
        adj_set.add(adj_id)
        adjacent[node_id] = adj_set
    else:
        adjacent[node_id].add(adj_id)

# return: dict(key=node_id, val=set(adjacents of node_id))
def load_adjacent(filename):
    file = open(filename)
    node_count = -1
    edge_count = -1

    adjacent = dict()
    lines = file.readlines(50000)
    while len(lines) > 0:
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                segs = line.split()
                if len(segs) == 5 and segs[1] == 'Nodes:':
                    node_count = int(segs[2])
                if len(segs) == 5 and segs[3] == 'Edges:':
                    edge_count = int(segs[4])
                line = file.readline().strip()
                continue
            
            # segs = line.strip().split('\t')
            segs = re.split(' |\t', line)
            node_id = int(segs[0])
            adj_id = int(segs[1])
            adj_node(adjacent, node_id, adj_id)
            # undirected graph
            adj_node(adjacent, adj_id, node_id)
        lines = file.readlines(50000)
        
    print('Nodes: ', node_count, 'Edges: ', edge_count)
    sys.stdout.flush()
    return adjacent


if __name__ == '__main__':
    clusters_filename = './data/tt.txt.emd.clusters'
    adjacent_filename = './data/tt.txt'
    clusters = load_clusters(clusters_filename)
    adjacent = load_adjacent(adjacent_filename)

    varience = cluster_varience(clusters)
    print('varience: ', varience)
    sys.stdout.flush()

    inter = interconnection(adjacent, clusters)
    print('interconnection edge#: ', inter)
    sys.stdout.flush()

    reconciled_cost = reconcile_mean(varience, inter)
    print('reconciled_cost: ', reconciled_cost)    
