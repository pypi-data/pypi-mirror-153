from sympy import Matrix, latex
from SymQC.kernel.gate import Gate
from SymQC.QCIS.instr import QCIS_instr, QCISOpCode
from SymQC.output.symbol_map import symbol_map


class store:
    def __init__(self, init, mapping: symbol_map, output_list):
        self.instr_save = []
        self.state_save = []
        self.circuit_save = []
        self.gate_save = []
        self.init_state = init.state.copy()
        self.final_state = None
        self.symbol_map = mapping
        self.out_list = output_list

    def save_final(self, state):
        self.final_state = latex(state.transpose())

    def save_instr(self, state: Matrix, instr: QCIS_instr, gate: Gate):
        ins_str = str(instr.op_code).removeprefix("QCISOpCode.")
        if instr.op_code.is_single_qubit_op():
            ins_str += '\t' + str(instr.qubit)
        elif instr.op_code.is_two_qubit_op():
            if instr.op_code == QCISOpCode.CNOT or instr.op_code == QCISOpCode.CZ:
                ins_str += '\t' + str(instr.control_qubit) + '\t' + str(instr.target_qubit)
            else:
                ins_str += '\t' + str(instr.control_qubit) + '\t' + str(instr.target_qubit)
        elif instr.op_code.is_measure_op():
            tmp = '\t'
            ins_str += '\t' + tmp.join([str(qubit) for qubit in instr.qubits_list])

        self.instr_save.append(ins_str)
        self.state_save.append(latex(state.transpose()))
        self.gate_save.append(latex(gate.matrix))

    def write_init(self):
        return self.init_state.transpose()

    def output_markdown(self, qcis_name="test.qcis", name='a.md'):
        file = open(name, 'w')
        file.write("# The ans of %s\n\n" % qcis_name)
        file.write("**Init state** is: \n$$\n%s\n$$\n\n" % latex(self.write_init()))
        for i in range(len(self.instr_save)):
            file.write("```assembly\n%d. %s\n```\n\n" % (self.out_list[i], self.instr_save[i]))
            file.write("$$\n%s\n$$\n" % self.gate_save[i])
            file.write("$$\n%s\n$$\n" % self.state_save[i])

        file.write("**Final state** is: \n$$\n%s\n$$\n\n" % self.final_state)

        if self.symbol_map.use:
            file.write("**symbols** is:\n\n")
            for x, y in self.symbol_map.symbol_table.items():
                file.write("$%s$ : %f\t\t" % (latex(x), y))
        file.close()
