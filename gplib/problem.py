from abc import ABC, abstractmethod
from gplib.solutions.solution import Solution
from gplib.solutions.node import Function
from gplib.solutions import solution


class AbstractProblem(ABC):

    def __init__(self, function_bank_builder):
        if function_bank_builder is not None:
            self._function_bank_builder = function_bank_builder

        self.func_bank = self._function_bank_builder()
        self._eval_cnt = 0
        self._elite_fitness = 0.0

    def fitness(self, target_solution_or_solutions):
        if isinstance(target_solution_or_solutions, Solution):
            fitness = self._cal_fitness(target_solution=target_solution_or_solutions)
            self._eval_cnt += 1
            solution.set_previous_fitness(target_solution_or_solutions, fitness)
            self._elite_fitness = max(self._elite_fitness, fitness)
            return fitness
        elif isinstance(target_solution_or_solutions, list):
            fitness_list = []
            for target_solution in target_solution_or_solutions:
                fitness = self._cal_fitness(target_solution=target_solution)
                solution.set_previous_fitness(target_solution, fitness)
                fitness_list.append(fitness_list)
                self._elite_fitness = max(self._elite_fitness, fitness)
            self._eval_cnt += len(target_solution_or_solutions)
            return fitness_list
        else:
            raise TypeError("target_solution_or_solutions should be Solution object or list of Solution objects.")

    @abstractmethod
    def _cal_fitness(self, target_solution):
        raise NotImplementedError("_cal_fitness should be implemented in {}".format(self.__class__))

    def get_eval_count(self):
        return self._eval_cnt

    def get_elite_fitness(self):
        return self._elite_fitness

    @abstractmethod
    def _function_bank_builder(self):
        raise NotImplementedError('default_function_bank_builder should be implemented in {}'.format(self.__class__))


class FunctionBank(object):

    def __init__(self):
        self._function_list = []
        self.children_dict = {}

    def add_function(self, func):
        if not isinstance(func, Function):
            raise ValueError('func must be Function class, but this func is {}.'.format(type(func)))
        n_children = func.n_children
        func_id = len(self._function_list)
        self._function_list.append(func)

        if n_children not in self.children_dict:
            self.children_dict[n_children] = []
        self.children_dict[n_children].append(func_id)

    def get_function_list(self, n_children=None):
        if n_children is None:
            return self._function_list[:]
        if n_children not in self.children_dict:
            raise KeyError('Key {} is not in children_dict'.format(n_children))
        else:
            return self.children_dict[n_children]

    def get_func(self, func_id):
        return self._function_list[func_id]


def problem_checker(problem):
    if not isinstance(problem, AbstractProblem):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(AbstractProblem, type(problem))
    else:
        return

    raise typ(msg)
