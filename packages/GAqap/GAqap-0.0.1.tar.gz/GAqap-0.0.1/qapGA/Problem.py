from typing import List
import numpy as np
import re

def get_problem_size(problem_path: str) -> int:
    return int(open(problem_path).read().split("\n")[0])

class Problem:
    def __init__(self, problem_path: str):
        self.problem_size = get_problem_size(problem_path)
        self.flow_matrix, self.distance_matrix = self.read_problem(problem_path)

    def read_problem(self, problem_path: str):
        def _form_matrix(data_list: List[str]):
            result_matrix = np.zeros([self.problem_size] * 2, dtype=np.int_)
            for i, row in enumerate(data_list):
                for j, elem in enumerate(re.split(" ", row.strip())):
                    result_matrix[i][j] = int(elem)
            return result_matrix
        with open(problem_path) as f:
            data = f.read().split("\n")
            dist_list = data[1:self.problem_size + 1]
            flow_list = data[self.problem_size + 2:]
        return _form_matrix(flow_list), _form_matrix(dist_list)