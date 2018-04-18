class Solution(object):
    def __init__(self, root):
        self.root = root
        self.previous_fitness = None


def get_depth(solution):

    d_list = []

    def cal_depth(c_node, depth):
        if c_node.children is not None:
            for c in c_node.children:
                cal_depth(c, depth+1)
        else:
            d_list.append(depth)

    cal_depth(solution.root, 0)

    return max(d_list)
