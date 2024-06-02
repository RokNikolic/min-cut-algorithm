# Min cut problem with Karger’s algorithm 2024, github.com/RokNikolic

import os
import time
import random
from tabulate import tabulate


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


def get_vertex_and_edge_num(edges_input):
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

    return num_of_vertices, num_edges


def min_cut(edges_input):
    """
    :param edges_input: the edges of a graph in the form of a list of connections
    :return: the minimum number of connections cut found using Karger’s algorithm
    """
    edges = edges_input.split("\n")
    if "" in edges:
        edges.remove("")

    vertex_set = set()
    for edge in edges:
        edge_vertex1, edge_vertex2 = edge.split(" ")
        vertex_set.add(edge_vertex1)
        vertex_set.add(edge_vertex2)

    vertex_set_list = [{i} for i in vertex_set]
    while len(vertex_set_list) > 2:
        edge = random.choice(edges)
        # edges.remove(edge)
        # The algorithm states to remove edges to self but in python it's a lot faster when you do not remove
        # any edges but just ignore them, as it is slow to remove a random item in a list
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


def run_algorithm(graph, num_of_runs=20):
    """
    :param graph: a graph represented by a list of edges between vertices
    :param num_of_runs: the number of runs over which you want to find the minimum cut
    :return: the minimum cut of a graph
    The min_cut algorithm has an about 15% success rate, so running it 20x time is a good start
    """
    min_found = float('inf')
    for _ in range(num_of_runs):
        num_of_connections = min_cut(graph)
        if num_of_connections < min_found:
            min_found = num_of_connections

    return min_found


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()

    start = time.perf_counter()
    result_data = []
    for graph_name in graph_list:
        print(f"Running algorithm on graph {graph_name}")
        input_graph = read_file(f'./graphs/{graph_name}')
        num_edge_vertex = get_vertex_and_edge_num(input_graph)
        result = run_algorithm(input_graph, 20)
        result_data.append([graph_name, num_edge_vertex, result])
    end = time.perf_counter()

    col_names = ["Graph name", "(vertex, edge)", "Opt"]
    print(tabulate(result_data, headers=col_names))
    print(f"Testing took: {(end - start) / 60 :.4} minutes")
