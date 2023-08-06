import sympy
from SymQC.kernel.utils import *
from SymQC.kernel.gate import Gate, ParametersGate
from SymQC.kernel.gates_lib import lib_gate
from SymQC.QCIS.instr import QCIS_instr, QCISOpCode


class Qsim:
    def __init__(self, n):
        self.state = None
        self.qubits_num = n

        self.global_circuit = None

    def apply(self):
        pass

    def apply_gate(self, gate: Gate, target_qubits: list, parameters=None, extra_optional_control_qubits=None) \
            -> sympy.Matrix:

        if extra_optional_control_qubits is None:
            extra_optional_control_qubits = []
        if parameters is None:
            parameters = []

        qubit_map = target_qubits[gate.ctrl_num:]
        ctrl_map = target_qubits[0: gate.ctrl_num] + extra_optional_control_qubits

        if isinstance(gate, ParametersGate):
            G = gate.get_matrix(get_discrete(qubit_map), parameters=parameters)
        else:
            G = gate.get_matrix(get_discrete(qubit_map))
        # 合并俩操作
        qubit_map.sort()

        marki = get_mark(qubit_map, 0)
        mark = get_mark(qubit_map, self.qubits_num)

        ctrl_mark = get_mark(ctrl_map, 0)

        addr = gen_subset(mark)
        addri = sorted(gen_subset(marki))

        for s in addr:
            if ctrl_mark == 0 or s & ctrl_mark:
                addrs = [(s | i) for i in addri]
                x = sympy.Matrix([self.state[i] for i in addrs])
                x = G * x
                for i, j in zip(addrs, x):
                    self.state[i] = j
        return self.state


class Qsim_state(Qsim):
    def __init__(self, n, name):
        super().__init__(n)
        self.state = sympy.Matrix(sympy.symbols('a:' + "%d" % (1 << n)))

        self.map = {}
        self.in_use = 0
        for qubit in name:
            self.map[qubit] = self.in_use
            self.in_use += 1

    def apply_instr(self, instr: QCIS_instr):
        if instr.op_code.is_single_qubit_op():
            gate = Gate(lib_gate(instr))
            qubit = self.map[instr.qubit]
            self.apply_gate(gate, [qubit])
        elif instr.op_code.is_two_qubit_op():
            if instr.op_code == QCISOpCode.CNOT or instr.op_code == QCISOpCode.CZ:
                gate = Gate(lib_gate(instr), 1)
                qubit = self.map[instr.target_qubit]
                ctrl = self.map[instr.control_qubit]
                self.apply_gate(gate, [ctrl, qubit])
            else:
                gate = Gate(lib_gate(instr))
                qubit = self.map[instr.target_qubit]
                fake_ctrl = self.map[instr.control_qubit]
                self.apply_gate(gate, [qubit, fake_ctrl])
        elif instr.op_code.is_measure_op():
            gate = Gate(lib_gate(instr))
            qubit_list = [self.map[qubit] for qubit in instr.qubits_list]
            for qubit in qubit_list:
                self.apply_gate(gate, [qubit])

        return gate
