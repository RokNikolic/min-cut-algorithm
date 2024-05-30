# Min cut problem algorithm 2024, github.com/RokNikolic

import os
import time
import random


def read_file(name):
    with open(rf'{name}', 'r') as f:
        return f.read()


def count_connections_between_nodes(node1, node2, edges):
    connections = 0
    for edge in edges:
        vertices = edge.split(" ")
        if vertices[0] in node1 and vertices[1] in node2 \
                or vertices[0] in node2 and vertices[1] in node1:
            connections += 1
    return connections


def min_cut(edges_input):
    edges = edges_input.split("\n")
    if "" in edges:
        edges.remove("")
    num_edges = len(edges)

    vertex_set = set()
    for edge in edges:
        edge_vertex1, edge_vertex2 = edge.split(" ")
        vertex_set.add(edge_vertex1)
        vertex_set.add(edge_vertex2)
    num_of_vertices = len(vertex_set)

    vertex_set_list = [{i} for i in vertex_set]
    while len(vertex_set_list) > 2:
        edge = random.choice(edges)
        # edges.remove(edge)
        vertices = edge.split(" ")
        new_vertex1 = {vertices[0]}
        new_vertex2 = {vertices[1]}

        update = True
        break_count = 0
        # Find vertex in list
        for i in range(len(vertex_set_list) - 1, -1, -1):
            if break_count == 2:
                break
            joint_vertex = vertex_set_list[i]
            if vertices[0] in joint_vertex and vertices[1] in joint_vertex:
                update = False
            if vertices[0] in joint_vertex:
                new_vertex1 = joint_vertex
                break_count += 1
                continue
            if vertices[1] in joint_vertex:
                new_vertex2 = joint_vertex
                break_count += 1
                continue

        if update:
            new_vertex1.update(new_vertex2)
            vertex_set_list.remove(new_vertex2)

    num_of_connections = count_connections_between_nodes(vertex_set_list[0], vertex_set_list[1], edges)
    return num_of_connections


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()

    start = time.perf_counter()
    for graph_name in graph_list:
        print(f"Running algorithm on graph {graph_name}")
        graph = read_file(f'./graphs/{graph_name}')
        num_of_c = min_cut(graph)
        print(num_of_c)

    print(f"All graphs cut in: {time.perf_counter() - start :.3} seconds")
