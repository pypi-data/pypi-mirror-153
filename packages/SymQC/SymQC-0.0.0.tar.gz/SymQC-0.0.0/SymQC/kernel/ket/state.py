from sympy import Matrix, symbols, pprint

from SymQC.kernel.utils import kron, make_ket


class Qutensor:
    def __init__(self, qubit, vec):
        self.size = 1
        self.state = vec
        self.map = {qubit: 0}
        self.ket = Matrix([symbols("\\ket{0_{%s}}" % qubit), symbols("\\ket{1_{%s}}" % qubit)])
        self.pre = sum([i * i for i in self.state])
        self.now = sum([i * i for i in self.state])

    def reset(self, qubit, vec):
        self.size = 1
        self.state = vec
        self.map = {qubit: 0}
        self.ket = Matrix([symbols("\\ket{0_{%s}}" % qubit), symbols("\\ket{1_{%s}}" % qubit)])
        self.pre = sum([i * i for i in self.state])
        self.now = sum([i * i for i in self.state])

    def insert_tensor(self, tensor):
        self.state = kron(tensor.state, self.state)
        for key in tensor.map.keys():
            tensor.map[key] += self.size
        self.size += tensor.size
        self.map.update(tensor.map)
        self.update_ket()
        self.pre = sum([i * i for i in self.state])
        self.now = sum([i * i for i in self.state])

    def insert_qubit(self, qubit, vec):
        self.map[qubit] = self.size
        self.size += 1
        self.state = kron(vec, self.state)

    def clear_zero(self, state, qubit, height):
        s = []
        for i in range(len(self.state)):
            if ((i >> state) & 0x1) == height:
                s.append(self.state[i])
        self.state = Matrix(s)
        pre = self.now
        now = sum([i * i for i in self.state])
        if self.size == 1:
            if height:
                self.reset(qubit, Matrix([0, 1]))
            else:
                self.reset(qubit, Matrix([1, 0]))
            return pre, now, False
        self.size -= 1

        for key in self.map.keys():
            if self.map[key] > self.map[qubit]:
                self.map[key] -= 1
        del self.map[qubit]
        self.update_ket()
        return pre, now, True

    def update_ket(self):
        l = list(self.map.keys())
        x = make_ket(l)
        self.ket = Matrix([symbols("\\ket{%s}" % s) for s in x])


class State:
    def __init__(self, names):
        self.tensor = [Qutensor(qubit, Matrix([symbols("\\alpha_{%s}" % qubit), symbols("\\beta_{%s}" % qubit)]))
                       for qubit in names]
        self.symbols = [(symbols("\\alpha_{%s}" % Q), symbols("\\beta_{%s}" % Q)) for Q in names]
        self.size = len(names)
        self.map = dict([(qubit, i) for qubit, i in zip(names, range(self.size))])
        self.empty = set()

    def merge(self, qubit1, qubit2):
        tensor1, state1 = self.get_pos(qubit1)
        tensor2, state2 = self.get_pos(qubit2)

        if tensor1 == tensor2:
            return tensor1, state1, state2

        if qubit1 < qubit2:
            for key in self.tensor[tensor2].map.keys():
                self.map[key] = tensor1

            self.tensor[tensor1].insert_tensor(self.tensor[tensor2])
            self.tensor[tensor2] = None
            self.empty.add(tensor2)
            self.size -= 1

            return tensor1, self.tensor[tensor1].map[qubit1], self.tensor[tensor1].map[qubit2]
        else:
            for key in self.tensor[tensor1].map.keys():
                self.map[key] = tensor2
            self.tensor[tensor2].insert_tensor(self.tensor[tensor1])
            self.tensor[tensor1] = None
            self.empty.add(tensor1)
            self.size -= 1

            return tensor2, self.tensor[tensor2].map[qubit1], self.tensor[tensor2].map[qubit2]

    def measure(self, tensor, state, qubit, height):
        pre, now, flag = self.tensor[tensor].clear_zero(state, qubit, height)
        if not flag:
            self.tensor[tensor].pre = pre
            self.tensor[tensor].now = now
            return
        index = self.empty.pop()
        if height:
            self.tensor[index] = Qutensor(qubit, Matrix([0, 1]))
        else:
            self.tensor[index] = Qutensor(qubit, Matrix([1, 0]))

        self.tensor[tensor].pre = now
        self.tensor[tensor].now = now

        self.tensor[index].pre = pre
        self.tensor[index].now = now
        self.map[qubit] = index

    def split(self, qubit1, qubit2):
        pass

    def judge(self, qubit1, qubit2):
        pass

    def get_pos(self, qubit):
        tensor = self.map[qubit]
        state = self.tensor[tensor].map[qubit]
        return tensor, state

    def check_single(self):
        for tensor in self.tensor:
            if tensor.state[0] != 1 and tensor.state[0] != 0:
                return False
        return True
