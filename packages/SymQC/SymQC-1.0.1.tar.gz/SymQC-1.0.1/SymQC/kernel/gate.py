from math import log2
import sympy
from SymQC.kernel.utils import *


class Gate:
    def __init__(self, mat, ctrl=0):
        self.matrix = sympy.Matrix(mat)
        assert (self.matrix.cols == self.matrix.rows)
        self.n = log2(self.matrix.cols)
        assert (self.n == int(self.n))
        self.n = int(self.n)
        self.ctrl_num = ctrl

    def get_matrix(self, qubit_map=None, ctrl_map=None, n=0):
        if ctrl_map is None:
            ctrl_map = []
        if qubit_map is None:
            qubit_map = []
        qubit_map = list(qubit_map)
        ctrl_map = list(ctrl_map)

        if n == 0:
            n = self.n

        if self.ctrl_num == 0:
            if not qubit_map:
                return self.matrix
        else:
            if ctrl_map == [] and qubit_map == []:
                return self.matrix

        res = sympy.ones(2 ** n, 2 ** n)

        matI = sympy.eye(2)

        for p in range(n):
            if p not in qubit_map:
                mark = get_mark([p], n)
                addr = gen_subset(mark)
                for i in range(matI.rows):
                    for j in range(matI.cols):
                        for si in addr:
                            mi = map_bit(i, si, [p])
                            for sj in addr:
                                mj = map_bit(j, sj, [p])
                                res[mi, mj] = res[mi, mj] * matI[i, j]

        mark = get_mark(qubit_map, n)
        ctrl_mark = get_mark(ctrl_map, 0)
        addr = gen_subset(mark)

        for i in range(self.matrix.rows):
            for j in range(self.matrix.cols):
                for si in addr:
                    mi = map_bit(i, si, qubit_map)
                    for sj in addr:
                        mj = map_bit(j, sj, qubit_map)
                        if ctrl_map:
                            if mi & ctrl_mark and mj & ctrl_mark:
                                res[mi, mj] = res[mi, mj] * self.matrix[i, j]
                            else:
                                res[mi, mj] = res[mi, mj] * (i == j)
                        else:
                            res[mi, mj] = res[mi, mj] * self.matrix[i, j]
        return res


# SingleQubitGate, TwoQubitGate, MultiQubitGate

class ParametersGate(Gate):
    def __init__(self, mat, ctrl=0, parameters=None):
        Gate.__init__(self, mat, ctrl)
        if parameters is None:
            parameters = []
        self.parameters = parameters

    def get_matrix(self, qubit_map=None, ctrl_map=None, n=0, parameters=None):
        if parameters is None:
            parameters = []
        if ctrl_map is None:
            ctrl_map = []
        if qubit_map is None:
            qubit_map = []
        res = Gate.get_matrix(self, qubit_map, ctrl_map, n)
        res = res.subs([(self.parameters[i], parameters[i]) for i in range(len(parameters))])
        return res
