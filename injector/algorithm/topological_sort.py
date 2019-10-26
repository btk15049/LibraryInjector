# -*- coding: utf-8 -*-


def topological_sort(nodes, edges) -> []:
    visited = set()
    result = []

    def dfs(v):
        if v not in visited:
            visited.add(v)
            for u in edges[v]:
                dfs(u)
            result.append(v)

    for s in nodes:
        dfs(s)

    return result
