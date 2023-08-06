import sympy
from SymQC.kernel.utils import gen_subset, get_mark, map_bit

"""
The implementation of class Circuit
"""


class Circuit:
    def __init__(self, n):
        self.n = n  # the number of qubits
        self.gates = []
        self.matrix = sympy.eye(2 ** n)

    def add_gates(self, gates: list, init=0):
        """Add gates to the circuit"""
        if self.matrix == sympy.eye(2 ** self.n):
            self.matrix = Circuit.combine_gates(gates, self.n)
        else:
            self.matrix = Circuit.combine_gates(gates, self.n) * self.matrix
        self.gates.append(gates)

    @staticmethod
    def make_from_gates_sequence(gates_sequence: list, n=0):
        """Make a circuit from a sequence of gates"""
        if n == 0:
            for gates in gates_sequence:
                for gate in gates:
                    n = max(n, max(gate[1] + gate[2]))

        res = Circuit(n)
        for gates in gates_sequence:
            res.add_gates(gates)

        return res

    @staticmethod
    def combine_gates(gates: list, n):
        """Build the utility matrix of these gates"""
        vis = [0] * n
        mark = 0
        res = sympy.ones(2 ** n, 2 ** n)
        blnk = []

        for g, opt_list, ctrl_list in gates:
            mark = 0
            for i in opt_list:
                vis[i] = 1
            for i in ctrl_list:
                vis[i] = 1

        blnk = [i for i in range(len(vis)) if vis[i] == 0]
        vis = [i for i in range(len(vis)) if vis[i] != 0]

        matI = sympy.eye(2)

        for p in blnk:

            addr = gen_subset(get_mark([p], n))
            for i in range(matI.rows):
                for j in range(matI.cols):
                    for si in addr:
                        mi = map_bit(i, si, [p])
                        for sj in addr:
                            mj = map_bit(j, sj, [p])
                            res[mi, mj] = res[mi, mj] * matI[i, j]

        for g, opt_list, ctrl_list in gates:
            bits = opt_list + ctrl_list

            mark = get_mark(bits, n)
            addr = gen_subset(mark)
            mat = g.get_matrix(range(g.n), range(g.n, g.n + g.ctrl_num), g.n + g.ctrl_num)

            for i in range(mat.rows):
                for j in range(mat.cols):
                    for si in addr:
                        mi = map_bit(i, si, bits)
                        for sj in addr:
                            mj = map_bit(j, sj, bits)
                            res[mi, mj] = res[mi, mj] * mat[i, j]

        return res
