#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import *
import numpy as np
import re
import matplotlib.pyplot as plt
import sys
import networkx as nx
import matplotlib.pyplot as plt
from itertools import count


def adj_node(adjacent, node_id, adj_id):
    if adjacent.get(node_id) == None:
        adj_set = set()
        adj_set.add(adj_id)
        adjacent[node_id] = adj_set
    else:
        adjacent[node_id].add(adj_id)

# return: dict(key=node_id, val=set(adjacents of node_id))
def load_adjacent(filename):
    G = nx.DiGraph()

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
            
            G.add_edges_from([(str(node_id), str(adj_id))])
            edge_count += 1;
        lines = file.readlines(50000)
        
    node_count = len(adjacent)
    print('Nodes: ', node_count, 'Edges: ', edge_count)
    sys.stdout.flush()
    return adjacent, G

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

def draw_graph(G, node_sets):
    colors = ['lightpink', 'lightgreen', 'lavender', 'lightseagreen', 'lightsalmon', 'lightskyblue', \
              'lightyellow', 'lightsteelblue', 'lightgoldenrodyellow', 'lightcyan', 'lightblue', \
              'blueviolet', 'r', 'teal', 'b', 'm', 'y', 'lightcoral']
    color_map = {}
    for i in range(len(node_sets)):
        node_set = node_sets[i]        
        for node in node_set:
            color_map[str(node)] = colors[i]
            
    # show me the original
    for i in range(24):
        color_map[str(i)] = 'lightsteelblue'
    role_color = {'0':'lightpink','1':'lightpink','2':'lightpink',
                  '21':'lightgoldenrodyellow','22':'lightgoldenrodyellow','23':'lightgoldenrodyellow'}
    for (k, v) in role_color.items():
        color_map[k] = v
    
    node_color = [color_map.get(node, 0.1) for node in G.nodes()]

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
        node_color=node_color, node_size = 500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='g', alpha=0.4, arrows=False)
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.show()

if __name__ == '__main__':
    _, G = load_adjacent('./data/tt.txt')
    node_sets = load_clusters('./data/tt.txt.emd.clusters')
    draw_graph(G, node_sets)