# python implementation of the above approach.
import math
import unittest

from algs.sorting import selection_sort


class Matrix:
    def __init__(self, arr, order):
        self._matrix = arr
        self.order: int = order

    def copy(self):
        return Matrix(self._matrix.copy(), self.order)

    def flat(self):
        return self._matrix

    def to_flat_index(self, i, j):
        return self.order * i + j

    def add_to_row(self, row_index, value):
        for j in range(0, self.order):
            self.add(row_index, j, value)

    def add_to_col(self, col_index, value):
        for i in range(0, self.order):
            self.add(i, col_index, value)

    def get_row(self, i):
        return self._matrix[self.to_flat_index(i, 0):self.to_flat_index(i, self.order)]

    def get_col(self, j):
        return [self.get(i, j) for i in range(self.order)]

    def get(self, i, j):
        self._raise_invalid_index(i, j)
        return self._matrix[self.to_flat_index(i, j)]

    def set(self, i, j, value):
        self._raise_invalid_index(i, j)
        self._matrix[self.to_flat_index(i, j)] = value

    def add(self, i, j, value):
        entry = self.get(i, j)
        self.set(i, j, entry + value)

    def _raise_invalid_index(self, i, j):
        if i >= self.order or j >= self.order or i < 0 or j < 0:
            raise Exception("Index Out Of Bound!")

    def __eq__(self, other):
        _this_flat = self.flat()
        _other_flat = other.flat()
        if len(_this_flat) != len(_other_flat):
            return False

        for i in range(len(_this_flat)):
            if _this_flat[i] != _other_flat[i]:
                return False

        return True

    def __str__(self):
        s = ""
        for i in range(self.order):
            s += f"{self.get_row(i)}\n"
        return s


class MatrixEntry:
    value = None
    row: int
    col: int

    def empty(self) -> bool:
        return self.value is None

    def update(self, value, i, j):
        self.value = value
        self.row = i
        self.col = j

    def __str__(self):
        return f"({self.value}, {self.row}, {self.col})"


class CostMatrix(Matrix):
    def subtract_the_smallest_entry_in_each_row(self):
        for i in range(self.order):
            min_entry = min(self.get_row(i))
            self.add_to_row(i, -min_entry)

    def subtract_the_smallest_entry_in_each_col(self):
        for j in range(self.order):
            min_entry = min(self.get_col(j))
            self.add_to_col(j, -min_entry)


def is_zero(v):
    return abs(float(v)) < 0.0000001


def count_zeros(arr):
    counter = 0
    for v in arr:
        if is_zero(v):
            counter += 1
    return counter


class MatrixCrossOut:
    _has_covered_map = {}
    _col_covered_map = {}
    _row_covered_map = {}

    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.reset_cover()

    def reset_cover(self):
        self._has_covered_map = {}
        self._col_covered_map = {}
        self._row_covered_map = {}

    def _has_covered(self, i, j):
        return self._has_covered_map.get(self.matrix.to_flat_index(i, j)) is True

    def _cover_row(self, i):
        for j in range(self.matrix.order):
            self._has_covered_map[self.matrix.to_flat_index(i, j)] = True
        self._row_covered_map[i] = True

    def _cover_col(self, j):
        for i in range(self.matrix.order):
            self._has_covered_map[self.matrix.to_flat_index(i, j)] = True
        self._col_covered_map[j] = True

    def _cover_line(self, i, j):
        if not self._has_covered(i, j):
            r = count_zeros(self.matrix.get_row(i))
            c = count_zeros(self.matrix.get_col(j))
            if c > r:
                self._cover_col(j)
            else:
                self._cover_row(i)

    def _get_lines_covered(self):
        return len(self._col_covered_map) + len(self._row_covered_map)

    def draw_fewest_possible_lines(self) -> int:
        order = self.matrix.order
        self.reset_cover()
        for i in range(order):
            for j in range(order):
                value = self.matrix.get(i, j)
                if is_zero(value) or float(value) < 0.0:
                    self._cover_line(i, j)
        return self._get_lines_covered()

    def find_smallest_entry_not_covered(self):
        smallest_entry = MatrixEntry()
        for i in range(self.matrix.order):
            row = self.matrix.get_row(i)
            for j in range(self.matrix.order):
                if not self._has_covered(i, j) and (smallest_entry.empty() or row[j] < smallest_entry.value):
                    smallest_entry.update(row[j], i, j)
        return smallest_entry

    def added_to_crossed_out_cols(self, value):
        for j in range(self.matrix.order):
            if self._col_covered_map.get(j):
                for i in range(self.matrix.order):
                    self.matrix.add(i, j, value)

    def subtract_row_not_crossed_out(self, value):
        for i in range(self.matrix.order):
            if not self._row_covered_map.get(i):
                for j in range(self.matrix.order):
                    self.matrix.add(i, j, -value)

    def find_optimal_assignment(self) -> []:
        zeros = []

        for i in range(self.matrix.order):
            row = self.matrix.get_row(i)
            zeros.append(count_zeros(row))

        _, indexes = selection_sort(zeros.copy())

        assignment_result = []
        used_cols = []
        for i in indexes:
            for j in range(self.matrix.order):
                if is_zero(self.matrix.get(i, j)) and j not in used_cols:
                    used_cols.append(j)
                    assignment_result.append((i, j))
                    break

        return assignment_result


class HungarianLpSolution:
    def __init__(self, cost_matrix: CostMatrix, cross_out: MatrixCrossOut):
        self._original_matrix = cost_matrix.copy()
        self.cost_matrix = cost_matrix
        self.cross_out = cross_out

    def calculate(self) -> int:
        self.subtract_the_smallest_entry_in_each_row()
        self.subtract_the_smallest_entry_in_each_col()

        lines_drawn = self.draw_fewest_possible_lines()
        while not self.check_if_optimal_found(lines_drawn):
            smallest_entry = self.find_smallest_entry_not_covered()
            self.subtract_row_not_crossed_out(smallest_entry.value)
            self.added_to_crossed_out_cols(smallest_entry.value)
            lines_drawn = self.draw_fewest_possible_lines()

        return self.calculate_optimal_cost()

    def draw_fewest_possible_lines(self):
        return self.cross_out.draw_fewest_possible_lines()

    def check_if_optimal_found(self, lines_draw) -> bool:
        return lines_draw == self.cost_matrix.order

    def subtract_the_smallest_entry_in_each_row(self):
        self.cost_matrix.subtract_the_smallest_entry_in_each_row()

    def subtract_the_smallest_entry_in_each_col(self):
        self.cost_matrix.subtract_the_smallest_entry_in_each_col()

    def find_smallest_entry_not_covered(self):
        return self.cross_out.find_smallest_entry_not_covered()

    def added_to_crossed_out_cols(self, value):
        return self.cross_out.added_to_crossed_out_cols(value)

    def subtract_row_not_crossed_out(self, value):
        return self.cross_out.subtract_row_not_crossed_out(value)

    def calculate_optimal_cost(self):
        assignments = self.cross_out.find_optimal_assignment()

        _sum = 0
        for (i, j) in assignments:
            _sum += self._original_matrix.get(i, j)
        return _sum


def create_hlp(data: [int], order: int) -> HungarianLpSolution:
    if len(data) != order * order:
        got_order = int(math.sqrt(len(data)))
        raise Exception("Matrix Order Not Matched: Require %i, Got %i", order, got_order)
    cost_matrix = CostMatrix(data, order)
    cross_out = MatrixCrossOut(cost_matrix)
    return HungarianLpSolution(cost_matrix, cross_out)


class TestHungarianSolutions(unittest.TestCase):
    def test_hungarian_using_adjacency_matrix(self):
        cost_matrix_order = 3
        cost_array = [108, 125, 150, 150, 135, 175, 122, 148, 250]
        hlp = create_hlp(cost_array, cost_matrix_order)
        result = hlp.calculate()

        matrix = Matrix([0, 15, 0, 17, 0, 0, 0, 24, 86], 3)

        self.assertEqual(matrix, hlp.cost_matrix)
        self.assertEqual(407, result)

    def test_hungarian_using_adjacency_matrix2(self):
        cost_matrix_order = 3
        cost_array = [1500, 4000, 4500, 2000, 6000, 3500, 2000, 4000, 2500]
        hlp = create_hlp(cost_array, cost_matrix_order)
        self.assertEqual(8500, hlp.calculate())

    def test_draw_fewest_possible_lines(self):
        cost_matrix_order = 3
        cost_array = [0, 17, 2, 15, 0, 0, 0, 26, 88]
        hlp = create_hlp(cost_array, cost_matrix_order)
        lines_drawn = hlp.draw_fewest_possible_lines()

        self.assertEqual(2, lines_drawn)

    def test_check_if_optimal_found(self):
        cost_matrix_order = 3
        cost_array = [0, 15, 0, 17, 0, 0, 0, 24, 86]
        hlp = create_hlp(cost_array, cost_matrix_order)
        lines_drawn = hlp.draw_fewest_possible_lines()

        self.assertEqual(True, hlp.check_if_optimal_found(lines_drawn))

    def test_find_smallest_entry_not_covered(self):
        cost_matrix_order = 3
        cost_array = [0, 17, 2, 15, 0, 0, 0, 26, 88]
        hlp = create_hlp(cost_array, cost_matrix_order)
        hlp.draw_fewest_possible_lines()
        smallest_entry = hlp.find_smallest_entry_not_covered()

        self.assertEqual(2, smallest_entry.value)
        self.assertEqual(0, smallest_entry.row)
        self.assertEqual(2, smallest_entry.col)

    def test_subtract_row_not_crossed_out(self):
        cost_matrix_order = 3
        cost_array = [0, 17, 2, 15, 0, 0, 0, 26, 88]
        hlp = create_hlp(cost_array, cost_matrix_order)
        hlp.draw_fewest_possible_lines()
        smallest_entry = hlp.find_smallest_entry_not_covered()
        hlp.subtract_row_not_crossed_out(smallest_entry.value)
        matrix = Matrix([-2, 15, 0, 15, 0, 0, -2, 24, 86], 3)

        self.assertEqual(True, matrix == hlp.cost_matrix)

    def test_added_to_crossed_out_cols(self):
        cost_matrix_order = 3
        cost_array = [0, 17, 2, 15, 0, 0, 0, 26, 88]
        hlp = create_hlp(cost_array, cost_matrix_order)
        hlp.draw_fewest_possible_lines()
        smallest_entry = hlp.find_smallest_entry_not_covered()
        hlp.subtract_row_not_crossed_out(smallest_entry.value)

        self.assertEqual(2, smallest_entry.value)

        hlp.added_to_crossed_out_cols(2)
        matrix = Matrix([0, 15, 0, 17, 0, 0, 0, 24, 86], 3)

        self.assertEqual(True, matrix == hlp.cost_matrix)


if __name__ == "__main__":
    pass
