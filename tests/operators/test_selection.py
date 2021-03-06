# -*- coding: utf-8 -*-
import unittest

from onegpy.operators.selection import RandomSelection, TournamentSelection, EliteSelection,\
    reduce_population
from onegpy.solutions import node, solution
from onegpy.solutions.solution import Solution
from tests.test_problem import EmptyProblem


class ExampleSolutions(object):
    def __init__(self):
        self.population = []
        self.n_set = 2
        for i in range(self.n_set):
            s1 = self.create_tree_type1()
            s2 = self.create_tree_type2()
            s3 = self.create_tree_type3()
            solution.set_previous_fitness(s1, 1)
            solution.set_previous_fitness(s2, 2)
            solution.set_previous_fitness(s3, 3)

            self.population.append(s1)
            self.population.append(s2)
            self.population.append(s3)
        self.population = self.population * 2

    @staticmethod
    def create_tree_type1():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2, n3])
        node.set_children(n2, [n4, n5])

        return Solution(n1)

    @staticmethod
    def create_tree_type2():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2])
        node.set_children(n2, [n3, n4, n5])

        return Solution(n1)

    @staticmethod
    def create_tree_type3():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2, n3, n4])
        node.set_children(n2, [n5])

        return Solution(n1)


class TestRandomSelection(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.k = 3
        self.problem = EmptyProblem()

    def test__call__with_replacement(self):
        selection = RandomSelection(self.k,  replacement=True)
        chosen = selection.__call__(self.population)
        self.assertEqual(len(chosen), self.k)

    def test__call__without_replacement(self):
        selection = RandomSelection(self.k, replacement=False)
        chosen = selection.__call__(self.population)
        self.assertEqual(self.k, len(chosen))


class TestEliteSelection(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.k = 3
        self.problem = EmptyProblem()

    def test__call__(self):
        selection = EliteSelection(self.k, self.problem)
        chosen = selection.__call__(self.population)
        self.assertEqual(len(chosen), self.k)


class TestTournamentSelection(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.tournament_size = 2
        self.k = 3
        self.problem = EmptyProblem()

    def test__call__with_replacement(self):
        selection = TournamentSelection(None, self.tournament_size, self.problem, replacement=True)
        chosen = selection.__call__(self.population)
        self.assertEqual(len(self.population), len(chosen))

        selection = TournamentSelection(self.k, self.tournament_size, self.problem, replacement=True)
        chosen = selection.__call__(self.population)
        self.assertEqual(self.k, len(chosen))

    def test__call__without_replacement(self):
        selection = TournamentSelection(self.k, self.tournament_size, self.problem, replacement=False)
        chosen = selection.__call__(self.population)
        self.assertEqual(self.k, len(chosen))

        msg = 'If replacement is False, selection_size must be set.'
        with self.assertRaises(TypeError, msg=msg):
            TournamentSelection(self.tournament_size, self.problem, replacement=False)


class TestSelectionFunctions(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)

    def test_reduce_population(self):
        self.assertEqual(len(reduce_population(self.population)), 3)


if __name__ == '__main__':
    unittest.main()
