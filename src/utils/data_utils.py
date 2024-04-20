"""
Data utils functions for pre-processing and data loading.
#ref: https://github.com/HazyResearch/hgcn/blob/master/utils/data_utils.py#L125
"""
import os
import pickle as pkl
import sys

import networkx as nx
import numpy as np
import scipy.sparse as sp

# 

# def load_data_lp(dataset, use_feats, data_path):
#     if dataset in ['cora', 'pubmed']:
#         adj, features = load_citation_data(dataset, use_feats, data_path)[:2]
#     elif dataset == 'disease_lp':
#         adj, features = load_synthetic_data(dataset, use_feats, data_path)[:2]
#     elif dataset == 'airport':
#         adj, features = load_data_airport(dataset, data_path, return_label=False)
#     else:
#         raise FileNotFoundError('Dataset {} is not supported.'.format(dataset))
#     data = {'adj_train': adj, 'features': features}
#     return data


def load_citation_data(dataset_str, use_feats, data_path, split_seed=None):
    names = ['x', 'y', 'tx', 'ty', 'allx', 'ally', 'graph']
    objects = []
    for i in range(len(names)):
        with open(os.path.join(data_path, "ind.{}.{}".format(dataset_str, names[i])), 'rb') as f:
            if sys.version_info > (3, 0):
                objects.append(pkl.load(f, encoding='latin1'))
            else:
                objects.append(pkl.load(f))

    x, y, tx, ty, allx, ally, graph = tuple(objects)
    test_idx_reorder = parse_index_file(os.path.join(data_path, "ind.{}.test.index".format(dataset_str)))
    test_idx_range = np.sort(test_idx_reorder)

    features = sp.vstack((allx, tx)).tolil()
    features[test_idx_reorder, :] = features[test_idx_range, :]

    labels = np.vstack((ally, ty))
    labels[test_idx_reorder, :] = labels[test_idx_range, :]
    labels = np.argmax(labels, 1)

    idx_test = test_idx_range.tolist()
    idx_train = list(range(len(y)))
    idx_val = range(len(y), len(y) + 500)

    adj = nx.adjacency_matrix(nx.from_dict_of_lists(graph))
    if not use_feats:
        features = sp.eye(adj.shape[0])
    return adj, features, labels, idx_train, idx_val, idx_test


def parse_index_file(filename):
    index = []
    for line in open(filename):
        index.append(int(line.strip()))
    return index


def load_synthetic_data(dataset_str, use_feats, data_path):
    object_to_idx = {}
    idx_counter = 0
    edges = []
    with open(os.path.join(data_path, "{}.edges.csv".format(dataset_str)), 'r') as f:
        all_edges = f.readlines()
    for line in all_edges:
        n1, n2 = line.rstrip().split(',')
        if n1 in object_to_idx:
            i = object_to_idx[n1]
        else:
            i = idx_counter
            object_to_idx[n1] = i
            idx_counter += 1
        if n2 in object_to_idx:
            j = object_to_idx[n2]
        else:
            j = idx_counter
            object_to_idx[n2] = j
            idx_counter += 1
        edges.append((i, j))
    adj = np.zeros((len(object_to_idx), len(object_to_idx)))
    for i, j in edges:
        adj[i, j] = 1.  # comment this line for directed adjacency matrix
        adj[j, i] = 1.
    if use_feats:
        features = sp.load_npz(os.path.join(data_path, "{}.feats.npz".format(dataset_str)))
    else:
        features = sp.eye(adj.shape[0])
    labels = np.load(os.path.join(data_path, "{}.labels.npy".format(dataset_str)))
    return sp.csr_matrix(adj), features, labels


def bin_feat(feat, bins):
    digitized = np.digitize(feat, bins)
    return digitized - digitized.min()


def load_data_airport(data_path, return_label=False):
    """
    三个数据只使用了一个
    graph = pkl.load(open(os.path.join(const.DATA_PATH/'airport/airport.p'), 'rb'))
    node_fe = pkl.load(open(os.path.join(const.DATA_PATH/'airport/airport_alldata.p'), 'rb'))
    具体字段含义见https://old.datahub.io/dataset/open-flights
    """
    graph = pkl.load(open(os.path.join(data_path, 'airport/airport.p'), 'rb'))
    adj = nx.adjacency_matrix(graph)
    features = np.array([graph.nodes[u]['feat'] for u in graph.nodes()])
    # features 包含归一化后的精度，纬度，海拔，国家GDP，国家人口，以人口为lable
    if return_label:
        label_idx = 4
        labels = features[:, label_idx]
        features = features[:, :label_idx]
        labels = bin_feat(labels, bins=[7.0/7, 8.0/7, 9.0/7])
        return graph, sp.csr_matrix(adj), features, labels
    else:
        return graph, sp.csr_matrix(adj), features
    
    

