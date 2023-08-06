import tempfile

import ply.yacc as yacc

from SymQC.QCIS.instr import QCISOpCode, QCIS_instr
from SymQC.QCIS.lexer import QCISLexer

OP_CODE_CONVERTER = {
    "MEASURE": QCISOpCode.MEASURE,
    "M": QCISOpCode.M,
    "B": QCISOpCode.B,
    "XY": QCISOpCode.XY,
    "XY2P": QCISOpCode.XY2P,
    "XY2M": QCISOpCode.XY2M,
    "X": QCISOpCode.X,
    "X2P": QCISOpCode.X2P,
    "X2M": QCISOpCode.X2M,
    "Y": QCISOpCode.Y,
    "Y2P": QCISOpCode.Y2P,
    "Y2M": QCISOpCode.Y2M,
    "Z": QCISOpCode.Z,
    "Z2P": QCISOpCode.Z2P,
    "Z2M": QCISOpCode.Z2M,
    "Z4P": QCISOpCode.Z4P,
    "Z4M": QCISOpCode.Z4M,
    "S": QCISOpCode.S,
    "SD": QCISOpCode.SD,
    "T": QCISOpCode.T,
    "TD": QCISOpCode.TD,
    "H": QCISOpCode.H,
    "RX": QCISOpCode.RX,
    "RY": QCISOpCode.RY,
    "RZ": QCISOpCode.RZ,
    "XYARB": QCISOpCode.XYARB,
    "RXY": QCISOpCode.RXY,
    "CZ": QCISOpCode.CZ,
    "CNOT": QCISOpCode.CNOT,
    "SWP": QCISOpCode.SWP,
    "SSWP": QCISOpCode.SSWP,
    "ISWP": QCISOpCode.ISWP,
    "SISWP": QCISOpCode.SISWP,
    "CP": QCISOpCode.CP,
    "FSIM": QCISOpCode.FSIM,
}


class QCISParser(object):
    """QCIS parser"""
    start = "root"

    def __init__(self):
        self.error_list = None
        self.lexer = QCISLexer()
        self.tokens = self.lexer.tokens  # Import all defined tokens in lexer
        self.parse_dir = tempfile.mkdtemp(prefix="sim-test")
        self.parser = yacc.yacc(module=self, debug=False, outputdir=self.parse_dir)
        self.__instructions = []  # To save all instructions extracted from program
        self.__qubit_names = set()  # A set for all qubit names occurred in program

    # As instructions are generated when specific rules are matched, these two method do not need to do any thing!
    def p_root(self, p):
        """root : program"""
        pass

    def p_program(self, p):
        """program : instruction NEWLINE program
        | instruction
        | NEWLINE program
        |
        """
        pass

    def p_instruction_n_qubit(self, p):
        """instruction : MEASURE qlist
        | M qlist
        | B qlist"""
        self.__qubit_names.update(p[2])
        self.__instructions.append(QCIS_instr(OP_CODE_CONVERTER[p[1]], qubits_list=p[2]))

    def p_qlist(self, p):
        """qlist : QREG qlist
        | QREG
        """
        if len(p) == 3:  # Matching rule 1
            # Extending qlist.value (a list, p[2]) with QREG.value (a number, p[1])
            p[0] = [p[1]] + p[2]
        else:  # Matching rule 2
            # Create the starting qubits list for all qubits to be measured
            p[0] = [p[1]]

    def p_instruction_1_qubit_2_param(self, p):
        """instruction : XYARB QREG FLOAT FLOAT
        | RXY QREG FLOAT FLOAT"""
        self.__qubit_names.add(p[2])
        self.__instructions.append(
            QCIS_instr(OP_CODE_CONVERTER[p[1]], qubit=p[2], azimuth=p[3], altitude=p[4])
        )

    def p_instruction_1_qubit_1_altitude(self, p):
        """instruction : RX QREG FLOAT
        | RY QREG FLOAT"""
        self.__qubit_names.add(p[2])
        self.__instructions.append(
            QCIS_instr(OP_CODE_CONVERTER[p[1]], qubit=p[2], altitude=p[3])
        )

    def p_instruction_1_qubit_1_azimuth(self, p):
        """instruction : XY QREG FLOAT
        | XY2P QREG FLOAT
        | XY2M QREG FLOAT
        | RZ QREG FLOAT"""
        self.__qubit_names.add(p[2])
        self.__instructions.append(
            QCIS_instr(OP_CODE_CONVERTER[p[1]], qubit=p[2], azimuth=p[3])
        )

    def p_instruction_1_qubit_0_param(self, p):
        """instruction : X QREG
        | X2P QREG
        | X2M QREG
        | Y QREG
        | Y2P QREG
        | Y2M QREG
        | Z QREG
        | Z2P QREG
        | Z2M QREG
        | Z4P QREG
        | Z4M QREG
        | S QREG
        | SD QREG
        | T QREG
        | TD QREG
        | H QREG"""
        self.__qubit_names.add(p[2])
        self.__instructions.append(QCIS_instr(OP_CODE_CONVERTER[p[1]], qubit=p[2]))

    def p_instruction_2_qubit_0_param(self, p):
        """instruction : CZ QREG QREG
        | CNOT QREG QREG
        | SWP QREG QREG
        | SSWP QREG QREG
        | ISWP QREG QREG
        | SISWP QREG QREG"""
        self.__qubit_names.update({p[2], p[3]})
        self.__instructions.append(
            QCIS_instr(OP_CODE_CONVERTER[p[1]], control_qubit=p[2], target_qubit=p[3])
        )

    def p_instruction_2_qubit_1_param(self, p):
        """instruction : CP QREG QREG FLOAT
        | FSIM QREG QREG FLOAT"""
        self.__qubit_names.update({p[2], p[3]})
        self.__instructions.append(
            QCIS_instr(
                OP_CODE_CONVERTER[p[1]],
                control_qubit=p[2],
                target_qubit=p[3],
                azimuth=p[4],
            )
        )

    def p_error(self, p):
        """Error handling method skipping error-occurred line."""
        if not p:
            error_msg = "Syntax error at the end of program."
            self.error_list.append(error_msg)
            return

        col = self.lexer.find_column(p)
        lines = self.lexer.data.split("\n")
        error_msg = "Syntax error: Found unmatched {0} at ({1}, {2}).\nSkip line {1}: {3}".format(
            p.type, self.lexer.lineno, col, lines[p.lineno - 1]
        )
        self.error_list.append(error_msg)

        # Read ahead looking for a new line
        while True:
            tok = self.lexer.token()  # Get the next token
            if not tok or tok.type == "NEWLINE":
                break
        self.parser.restart()

    def parse(self, data):
        self.__instructions = []  # Clear instructions list
        self.__qubit_names = set()  # Clear qubit names set
        self.error_list = []
        self.lexer = QCISLexer()  # Reset initial lineno of lexer
        self.parser.parse(data, lexer=self.lexer)

        success = True
        if len(self.error_list) > 0:
            error_msgs = "\n".join(self.error_list)
            print("Found errors during parsing QCIS program: {}".format(error_msgs))
            success = False

        qubit_names_list = list(self.__qubit_names)  # Turn the set to a list
        qubit_names_list.sort()  # Sort by alphabetic
        return success, self.__instructions, qubit_names_list

