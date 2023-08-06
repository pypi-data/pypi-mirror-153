from pathlib import Path

import networkx
from networkx.readwrite import edgelist


def read_graph_edges(filename_path: Path) -> edgelist:
    return networkx.read_edgelist(filename_path)


def get_graph_summary(graph: edgelist) -> str:
    return "V:{}; E:{}".format(graph.number_of_nodes(), graph.number_of_edges())


def get_graph_vertices_at_distance(graph: edgelist, vertex, distance: int):
    vertices = list(networkx.descendants_at_distance(graph, vertex, distance))
    vertices.sort()
    return vertices


def get_graph_vertices_up_to_distance(graph: edgelist, vertex, max_distance: int):
    list = []
    for distance in range(max_distance + 1):
        vertices = get_graph_vertices_at_distance(graph, vertex, distance)
        list.extend(vertices)
    list.sort()
    return list


def get_graph_origin_target_shortest_path(graph: edgelist, origin, target):
    return networkx.shortest_path(graph, origin, target)
