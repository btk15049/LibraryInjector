# -*- coding: utf-8 -*-
from injector.algorithm.topological_sort import topological_sort
import unittest


class TopologicalSortTest(unittest.TestCase):
    def test_topological_sort_with_list(self):
        nodes = [0, 1, 2]
        edges = [[1, 2], [], [1]]
        expected = [1, 2, 0]
        self.assertListEqual(topological_sort(nodes, edges), expected)

    def test_topological_sort_with_dict(self):
        nodes = ['a', 'b', 'c', 'd']
        edges = {'a': ['d'], 'b': ['c', 'a'], 'c': ['a'], 'd': []}
        expected = ['d', 'a', 'c', 'b']
        self.assertListEqual(topological_sort(nodes, edges), expected)


def aoj_system_test():
    V, E = map(int, input().split())
    nodes = []
    edges = []
    for i in range(V):
        nodes.append(i)
        edges.append([])
    for _ in range(E):
        a, b = map(int, input().split())
        edges[b].append(a)
    ret = topological_sort(nodes, edges)
    for v in ret:
        print(v)


def aoj_system_test_judge():
    V, E = map(int, input().split())
    pos = [-1] * V
    edges = []
    for _ in range(E):
        edges.append(map(int, input().split()))
    for i in range(V):
        v = int(input())
        assert 0 <= v < V
        pos[v] = i
    for a, b in edges:
        assert(pos[a] < pos[b])


if __name__ == '__main__':
    unittest.main()
