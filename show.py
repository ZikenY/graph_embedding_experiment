#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:51:19 2018

@author: ziken
"""
from numpy import *
import matplotlib.pyplot as plt


def loadpoints(filename):
    result = list()
    datafile = open(filename, 'r')
    datafile.readlines(1) # count
    lines = datafile.readlines(10000000)
    for line in lines:
        point = line.strip(' ').split(' ')
        result.append([int(point[0]), float(point[1]), float(point[2])])
    datafile.close()
    return result

def loadpoints_map(filename):
    result = dict()
    datafile = open(filename, 'r')
    datafile.readlines(1) # count
    lines = datafile.readlines(10000000)
    for line in lines:
        if line.strip(' ') == '':
            break
        point = line.strip(' ').split(' ')
        result[int(point[0])] = [float(point[1]), float(point[2])]
    datafile.close()
    return result
    
# point(id, x, y)
def show_points(points):
    # draw all samples  
    for i in range(len(points)):  
        plt.plot(points[i][1], points[i][2], 'ob')  

    plt.xlabel('X1'); plt.ylabel('X2')  
    plt.show()

def load_clusters(filename):
    result = list()
    datafile = open(filename, 'r')
    lines = datafile.readlines(10000000)
    cluster_flag = 0
    for line in lines:
        if line.strip(' ') == '':
            break
        if cluster_flag == 0:
            cluster_flag = 1
            continue
        point_ids = line.strip(' ').split(' ')
        points = list()
        for id in point_ids:
            points.append(int(id))
        result.append(points)
    datafile.close()
    return result
    
def draw_clusters(clusters, points_map):
    marks = ['^r', 'sg', 'ob', '<c', 'ok', '+r', 'sr', 'dr', '<r', 'pr']
    if len(clusters) > len(marks):
        print('逗我玩咩')
        return
    # draw all samples
    for i in range(len(clusters)):
        mark = marks[i]
        cluster = clusters[i]
        for point_id in cluster:
            point = [points_map[point_id][0], points_map[point_id][1]]
            plt.plot(point[0], point[1], mark)  
    
    plt.xlabel('dim0'); plt.ylabel('dim1')
    plt.show()

if __name__ == "__main__":
    points_map = loadpoints_map('./data/tt.txt.emd')
    clusters = load_clusters('./data/tt.txt.emd.clusters')
    draw_clusters(clusters, points_map)
