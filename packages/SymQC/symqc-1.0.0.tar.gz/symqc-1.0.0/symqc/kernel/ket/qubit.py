from SymQC.QCIS.instr import QCIS_instr, QCISOpCode
from SymQC.kernel.gate import Gate
from SymQC.kernel.gates_lib import lib_gate
from SymQC.kernel.ket.state import State
from SymQC.kernel.qubit import Qsim
from SymQC.kernel.utils import find_main
from SymQC.output.symbol_map import symbol_map
from random import random
from sympy import Matrix, pprint


class Qsim_ket(Qsim):
    def __init__(self, n, name, sym_map:symbol_map=None):
        super().__init__(n)
        self.ket_state = State(name)
        f = 1
        for ten in self.ket_state.tensor:
            f *= ten.state.transpose() * ten.ket
        self.state = f
        self.symbol_table = sym_map

    def apply_instr(self, instr: QCIS_instr):
        if instr.op_code.is_single_qubit_op():
            gate = Gate(lib_gate(instr))
            tensor, qubit = self.ket_state.get_pos(instr.qubit)
            self.state = self.ket_state.tensor[tensor].state
            self.qubits_num = self.ket_state.tensor[tensor].size
            self.ket_state.tensor[tensor].state = self.apply_gate(gate, [qubit])
        elif instr.op_code.is_two_qubit_op():
            if instr.op_code == QCISOpCode.CNOT or instr.op_code == QCISOpCode.CZ:
                gate = Gate(lib_gate(instr), 1)
                tensor, qubit, ctrl = self.ket_state.merge(instr.target_qubit, instr.control_qubit)
                self.state = self.ket_state.tensor[tensor].state
                self.qubits_num = self.ket_state.tensor[tensor].size
                self.ket_state.tensor[tensor].state = self.apply_gate(gate, [ctrl, qubit])
            else:
                gate = Gate(lib_gate(instr))
                tensor, qubit, fake_ctrl = self.ket_state.merge(instr.target_qubit, instr.control_qubit)
                self.state = self.ket_state.tensor[tensor].state
                self.qubits_num = self.ket_state.tensor[tensor].size
                self.ket_state.tensor[tensor].state = self.apply_gate(gate, [qubit, fake_ctrl])
        elif instr.op_code.is_measure_op():
            gate = Gate(lib_gate(instr))
            qubit_list = [self.ket_state.get_pos(qubit) for qubit in instr.qubits_list]
            for (tensor, state), qubit in zip(qubit_list, instr.qubits_list):

                self.state = self.ket_state.tensor[tensor].state
                self.qubits_num = self.ket_state.tensor[tensor].size
                tmp = self.state
                for a, b in self.ket_state.symbols:
                    tmp = tmp.subs(a, 1)
                    tmp = tmp.subs(b, 0)
                for sym, val in self.symbol_table.symbol_table.items():
                    tmp = tmp.subs(sym, val)
                p0, p1 = find_main(tmp, state)
                k = random()
                w = p0 / (p0 + p1)
                if k < p0 / (p0 + p1):
                    self.ket_state.tensor[tensor].state = self.apply_gate(Gate(Matrix([[1, 0], [0, 0]])), [state])
                    self.ket_state.measure(tensor, state, qubit, 0)
                else:
                    self.ket_state.tensor[tensor].state = self.apply_gate(Gate(Matrix([[0, 0], [0, 1]])), [state])
                    self.ket_state.measure(tensor, state, qubit, 1)

        self.state = self.ket_state

        return gate
