# An algorithm to find the minimum cut of a graph from its edges

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
        edges.remove(edge)
        vertices = edge.split(" ")
        new_vertex1 = {vertices[0]}
        new_vertex2 = {vertices[1]}

        for joint_vertex in vertex_set_list:
            if vertices[0] in joint_vertex:
                new_vertex1 = joint_vertex
                vertex_set_list.remove(joint_vertex)
        for joint_vertex in vertex_set_list:
            if vertices[1] in joint_vertex:
                new_vertex2 = joint_vertex
                vertex_set_list.remove(joint_vertex)

        new_vertex = new_vertex1 | new_vertex2
        vertex_set_list.append(new_vertex)

        print(vertex_set_list)

    num_of_connections = count_connections_between_nodes(vertex_set_list[0], vertex_set_list[1], edges)
    print(num_of_connections)


def min_cut_dict(edges_input):
    edges = edges_input.split("\n")
    if "" in edges:
        edges.remove("")

    vertex_dict = {}
    for _ in edges:
        edge = random.choice(edges)
        edges.remove(edge)
        vertices = edge.split(" ")


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()

    start = time.perf_counter()
    for graph_name in graph_list[0:1]:
        print(f"Running algorithm on graph {graph_name}")
        graph = read_file(f'./graphs/{graph_name}')
        min_cut(graph)

    end = time.perf_counter()
    print(f"All graphs cut in: {end - start :.3} seconds")
