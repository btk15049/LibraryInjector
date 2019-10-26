# -*- coding: utf-8 -*-
from injector.algorithm.topological_sort import topological_sort
import unittest


class ArgumentParserTest(unittest.TestCase):
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
