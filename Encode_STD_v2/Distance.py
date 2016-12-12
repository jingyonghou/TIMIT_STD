import sys
import numpy as np


def KLdivergence(matrix_a, matrix_b, symmetrized=1):
    height = matrix_a.shape[0]
    width = matrix_b.shape[0]
    matrix_a_log = np.log(matrix_a)
    matrix_b_log = np.log(matrix_b)

    vector_a_log_a = np.zeros([height, 1]);
    vector_b_log_b = np.zeros([width, 1]);

    for i in range(height):
        vector_a_log_a[i, 0] = np.dot(np.array([matrix_a[i, :]]), np.array([matrix_a_log[i, :]]).T)[0][0]

    for i in range(width):
        vector_b_log_b[i, 0] = np.dot(np.array([matrix_b[i, :]]), np.array([matrix_b_log[i, :]]).T)[0][0]
    matrix_a_log_b = np.dot(matrix_a, matrix_b_log.T)
    matrix_b_log_a = np.dot(matrix_b, matrix_a_log.T)

    if symmetrized==1:
        distance_matrix = 0.5 * (vector_a_log_a - matrix_a_log_b) + 0.5 * (vector_b_log_b.T - matrix_b_log_a.T)
    else:
        distance_matrix = vector_a_log_a - matrix_a_log_b
    return distance_matrix

def innerProduct(matrix_a, matrix_b):
    distance_matrix = np.dot(matrix_a, matrix_b.T)
    return 1 - distance_matrix

distance_function={"KL-divergence":KLdivergence, "cosine":innerProduct, "inner-product":innerProduct}

def distance(matrix_a, matrix_b, distance_type, sub_num=40):
    height = matrix_a.shape[0]
    width = matrix_b.shape[0]
    dim = matrix_a.shape[1]

    distance_matrix = np.zeros([height, width])

    if dim%sub_num != 0:
        print("Error: dimmension error!\n")
        exit(1)
    else:
        encode_num = dim//sub_num
        for i in range(encode_num):
            mydistance=distance_function[distance_type]
            distance_matrix = distance_matrix + mydistance(matrix_a[:, i*sub_num:(i+1)*sub_num], matrix_b[:, i*sub_num:(i+1)*sub_num])
    return distance_matrix/encode_num
