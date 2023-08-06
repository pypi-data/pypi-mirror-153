from typing import List, Tuple, NamedTuple, Dict, Set, Callable
from math import nan


def lines(nodes):
    [n0, n1, n2] = nodes
    return (n0, n1), (n0, n2), (n1, n2)


class Edge(NamedTuple):
    pow: int
    adj_list: Set[int]


class Cell(NamedTuple):
    nodes: List[int]
    pow: int


class Group:
    id: int
    nodes: Set[int]
    edges: Set[Tuple[int, int]]
    cells: Set[int]

    def __init__(self, id, nodes, edges, cells):
        self.id, self.nodes, self.edges, self.cells = id, nodes, edges, cells

    def plot_group(self, mesh) -> Tuple[List[float], List[float], List[float]]:
        x, y, z = [], [], []
        for [n0, n1] in self.edges:
            [x0, y0], [x1, y1] = mesh.pts[n0], mesh.pts[n1]
            x.extend([x0, x1, nan])
            y.extend([y0, y1, nan])
            z.extend([0., 0., nan])
        return x, y, z


class Mesh:
    pts: List[Tuple[float, float]]
    edges: Dict[Tuple[int, int], Edge]
    cells: List[Cell]
    groups: int

    def __init__(self, pts: List[Tuple[float, float]], triangles: List[List[int]], pow: int, rcm: bool = False):
        if rcm:
            graph = rcm_graph(len(pts), triangles)
            pts = [pts[node] for node in graph]
            triangles = [[graph[n0], graph[n1], graph[n2]] for n0, n1, n2 in triangles]
        cells = []
        edges = {}
        for idx, nodes in enumerate(triangles):
            nodes.sort()
            for line in lines(nodes):
                if line not in edges:
                    edges[line] = Edge(pow, set())
                edges[line].adj_list.add(idx)
            cells.append(Cell(nodes, pow))
        cells.sort(key=lambda cell: cell[0])
        self.pts, self.edges, self.cells, self.groups = pts, edges, cells, 0

    def def_group(self, cond: Callable[[float, float], bool]):
        self.groups += 1
        id, nodes, edges, cells = self.groups, set(), set(), set()
        for ver, [x, y] in enumerate(self.pts):
            if cond(x, y):
                nodes.add(ver)
        for (n0, n1) in self.edges:
            if n0 in nodes and n1 in nodes:
                edges.add((n0, n1))
        for idx, ((n0, n1, n2), _) in enumerate(self.cells):
            if n0 in nodes and n1 in nodes and n2 in nodes:
                cells.add(idx)
        return Group(id, nodes, edges, cells)

    def def_outer(self) -> Group:
        self.groups += 1
        vers, edges = set(), set()
        for (nodes, edge) in self.edges.items():
            if len(edge.adj_list) < 2:
                for node in nodes:
                    vers.add(node)
                edges.add(nodes)
        return Group(self.groups, vers, edges, set())

    def plot_sys(self, group: Group = None) -> Tuple[List[float], List[float], List[float]]:
        x, y, z = [], [], []
        if group is None:
            for (n0, n1) in self.edges:
                [x0, y0], [x1, y1] = self.pts[n0], self.pts[n1]
                x.extend([x0, x1, nan])
                y.extend([y0, y1, nan])
                z.extend([0., 0., nan])
        else:
            for (n0, n1) in group.edges:
                [x0, y0], [x1, y1] = self.pts[n0], self.pts[n1]
                x.extend([x0, x1, nan])
                y.extend([y0, y1, nan])
                z.extend([0., 0., nan])
        return x, y, z


def rcm_graph(size: int, cells: List[List[int]]) -> Dict[int, int]:
    adj_list = {}
    for nodes in cells:
        for node in nodes:
            if node not in adj_list:
                adj_list[node] = set()
            for adj_node in nodes:
                if adj_node != node:
                    adj_list[node].add(adj_node)
    start = min([(len(adj_nodes), node) for node, adj_nodes in adj_list.items()])[1]
    graph = [start]
    used = {start}
    for idx in range(0, size):
        node = graph[idx]
        next_nodes = [(len(adj_list[n]), n) for n in adj_list[node]]
        next_nodes.sort()
        for (_, n) in next_nodes:
            if n not in used:
                graph.append(n)
                used.add(n)
    graph.reverse()
    return {node: idx for idx, node in enumerate(graph)}
