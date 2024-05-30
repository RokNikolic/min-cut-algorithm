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
        # edges.remove(edge)  # My implementation is a lot faster when I do not remove any edges
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


def run_testing(graph_path, runs_to_find_opt, runs_to_find_average):
    graph = read_file(f'./graphs/{graph_path}')
    num_edge_vertex = get_vertex_and_edge_num(graph)

    # Find optimal by finding minimal of a lot of runs
    min_found = num_edge_vertex[1]
    for _ in range(runs_to_find_opt):
        num_of_connections = min_cut(graph)
        if num_of_connections < min_found:
            min_found = num_of_connections

    # Find average over some runs of how long it takes to find optimal
    times = []
    for _ in range(runs_to_find_average):
        runs = 0
        while True:
            runs += 1
            num_of_connections = min_cut(graph)
            if num_of_connections <= min_found:
                times.append(runs)
                break
    average_time = sum(times) / len(times)

    return [graph_path, num_edge_vertex, min_found, average_time]


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()

    start = time.perf_counter()
    result_data = []
    for graph_name in graph_list:
        print(f"Running testing on graph {graph_name}")
        result_data.append(run_testing(graph_name, 50, 5))
    end = time.perf_counter()

    col_names = ["Graph name", "(vertex, edge)", "Opt", "Avr for opt"]
    print(tabulate(result_data, headers=col_names))
    print(f"Testing took: {(end - start) / 60 :.4} minutes")
