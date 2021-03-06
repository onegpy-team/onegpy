# -*- coding: utf-8 -*-
import unittest

from onegpy.operators import RandomInitializer
from onegpy.problem import AbstractProblem, FunctionBank
from onegpy.solutions import node, solution


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.Function(n_children, print_non_terminal)


def f_terminal():
    def print_terminal(x):
        print('terminal')

    return node.Function(0, print_terminal)


class DummyProblem(AbstractProblem):
    def __init__(self):
        super(DummyProblem, self).__init__(function_bank_builder=None)

    def _cal_fitness(self, target_solution):
        return target_solution.root.func_id

    def _function_bank_builder(self):
        func_bank = FunctionBank()
        for i in range(3):
            func_bank.add_function(f_non_terminal())
            func_bank.add_function(f_terminal())
        return func_bank


class TestInitializer(unittest.TestCase):
    def setUp(self):
        self.max_depth = 3
        self.problem = DummyProblem()

    def test_initialize(self):
        t_prob = 0
        initializer = RandomInitializer(t_prob, self.max_depth, self.problem)
        s = initializer()
        solution.set_solution_depth(s)
        self.assertEqual(s.depth, self.max_depth)
        self.assertEqual(node.nodes_checker(node.get_all_node(s.root)), None)

        t_prob = 1
        initializer = RandomInitializer(t_prob, self.max_depth, self.problem)
        s = initializer()
        solution.set_solution_depth(s)
        self.assertEqual(s.depth, 0)


if __name__ == '__main__':
    unittest.main()
