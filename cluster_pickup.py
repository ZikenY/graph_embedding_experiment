from math import *
import numpy as np
import re
import matplotlib.pyplot as plt
import sys

# adjacent: dict(key=node_id, val=set(adjacents of node_id))
# clusters: list of set(node_ids)
# return: cluster_index -> average adjacent number of nodes in this cluster
def count_adjacent(adjacent, clusters):
    cluster_id2avgnumber = dict()
    cluster_count = len(clusters)
    for i in range(cluster_count):
        c_i = list(clusters[i])
        # count the average adjacent number of nodes in this group
        count = 0.0
        for node_id in c_i:
            count += len(adjacent[node_id])
        cluster_id2avgnumber[i] = count / len(c_i)
    return cluster_id2avgnumber

def list2cluster(nodes):
    cluster = set()
    for i in range(len(nodes)):
        cluster.add(nodes[i])
    return cluster

# return: list of set(node_ids)
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
    node_count = 0
    edge_count = 0

    adjacent = dict()
    lines = file.readlines(50000)
    while len(lines) > 0:
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                '''
                segs = line.split()
                if len(segs) == 5 and segs[1] == 'Nodes:':
                    node_count = int(segs[2])
                if len(segs) == 5 and segs[3] == 'Edges:':
                    edge_count = int(segs[4])
                line = file.readline().strip()
                '''
                continue
            
            # segs = line.strip().split('\t')
            segs = re.split(' |\t', line)
            node_id = int(segs[0])
            adj_id = int(segs[1])
            adj_node(adjacent, node_id, adj_id)
            # undirected graph
            adj_node(adjacent, adj_id, node_id)
            edge_count += 1;
        lines = file.readlines(50000)
        
    node_count = len(adjacent)
    print('Nodes: ', node_count, 'Edges: ', edge_count)
    sys.stdout.flush()
    return adjacent

   
# adjacent: dict(key=node_id, val=set(adjacents of node_id))
# clusters: list of set(node_ids)
# cluster_id2avgnumber: cluster_index -> average adjacent number of nodes in this cluster
def save_data(filename, adjacent, clusters, cluster_id2avgnumber):
    # sort clusters by average adjacent numbers
    avgs = list()
    for i in range(len(clusters)):
        avgs.append(cluster_id2avgnumber[i])
    avgs = np.array(avgs)
    sorted_indices = np.argsort(avgs)
    sorted_indices = sorted_indices[::-1] # descending order, not ascending
    
    print('writting', end='')
    clusters_file = open(filename, 'w')
    for index in sorted_indices:
        nodes = clusters[index]

        clusters_file.write('------------------------------------------------------------------\n')
        clusters_file.write('average adjacent number: ')
        clusters_file.write(str(cluster_id2avgnumber[index]))
        clusters_file.write(', varience: ')
        varience = adjacent_varience(nodes, adjacent)
        clusters_file.write(str(varience))
        clusters_file.write('\n(node_id, adjacent number):\n')

        for node_id in nodes:
            ss = ' (' + str(node_id) + ', ' + str(len(adjacent[node_id])) + ')'
            clusters_file.write(ss)
        clusters_file.write('\n\n')
            
        print('.', end='')
        sys.stdout.flush()
    clusters_file.close()
    
# nodes: a set of nodes
def adjacent_varience(nodes, adjacent):
    # compute the varience of adjacent num between nodes
    avg = 0
    for node_id in nodes:
        avg += len(adjacent[node_id])
    avg = avg * 1.0 / len(nodes)
    
    varience = 0.0
    for node_id in nodes:
        varience += sqrt((len(adjacent[node_id]) - avg)**2)
    varience = varience / len(nodes)
    return varience
    
if __name__ == '__main__':
    adjacent_filename = './data/tt.txt'
    clusters_filename = './data/tt.txt.emd.clusters'
    output_pickup_filename = clusters_filename + '.pickup'
    
    clusters = load_clusters(clusters_filename)
    print('load_clusters done.')
    sys.stdout.flush()
    adjacent = load_adjacent(adjacent_filename)
    print('load_adjacent done.')
    sys.stdout.flush()

    cluster_id2avgnumber = count_adjacent(adjacent, clusters)
    print('cluster_id2avgnumber done.')
    save_data(output_pickup_filename, adjacent, clusters, cluster_id2avgnumber)
    print('\ndone. saved to "', output_pickup_filename, '"')
