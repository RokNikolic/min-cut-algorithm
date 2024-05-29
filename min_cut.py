# An algorithm to find the minimum cut of a graph from its edges

import os
import time
import random


def read_file(name):
    with open(rf'{name}', 'r') as f:
        return f.read()


def min_cut(edges_input):
    edges = edges_input.split("\n")
    if "" in edges:
        edges.remove("")
    num_edges = len(edges)

    vertex_set = set()
    for edge in edges:
        edge_vertex1, edge_vertex2 = map(int, edge.split(" "))
        vertex_set.add(edge_vertex1)
        vertex_set.add(edge_vertex2)
    num_of_vertices = len(vertex_set)

    vertex_set_list = []
    # while len(edges) > 2:
    for _ in edges:
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

        print(len(vertex_set_list))


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()

    start = time.perf_counter()
    for graph_name in graph_list[0:2]:
        print(f"Running algorithm on graph {graph_name}")
        graph = read_file(f'./graphs/{graph_name}')
        min_cut(graph)

    end = time.perf_counter()
    print(f"All graphs cut in: {end - start :.3} seconds")
