import ply.lex as lex


class QCISLexer(object):
    """QCIS lexer"""

    def __init__(self):
        """Create a ply lexer."""
        self.data = None
        self.lexer = lex.lex(module=self, debug=False, errorlog=lex.NullLogger())
        self.lineno = 1

    def input(self, data):
        """Set the input text data."""
        self.data = data
        self.lexer.input(data)

    def token(self):
        """Return the next token."""
        ret = self.lexer.token()
        return ret

    reserved = {
        # ---Basic Operations---
        "CZ": "CZ",
        "MEASURE": "MEASURE",  # Deprecated measurement, use `M`
        "M": "M",  # Recommended measurement
        "RZ": "RZ",
        "XYARB": "XYARB",  # Deprecated arbitrary xy-plane axis rotation, use `RXY`
        "XY": "XY",
        "XY2P": "XY2P",
        "XY2M": "XY2M",
        "X": "X",
        "X2P": "X2P",
        "X2M": "X2M",
        "Y": "Y",
        "Y2P": "Y2P",
        "Y2M": "Y2M",
        "Z": "Z",
        "Z2P": "Z2P",  # Deprecated z-axis rotation, use `S`
        "Z2M": "Z2M",  # Deprecated z-axis rotation, use `SD`
        "Z4P": "Z4P",  # Deprecated z-axis rotation, use `T`
        "Z4M": "Z4M",  # Deprecated z-axis rotation , use `TD`
        "S": "S",
        "SD": "SD",
        "T": "T",
        "TD": "TD",
        "B": "B",  # Time barrier for two qubits (useless in simulator)
        # ---Extended Operations---
        "H": "H",
        "RX": "RX",
        "RY": "RY",
        "RXY": "RXY",
        "CNOT": "CNOT",
        "SWP": "SWP",
        "SSWP": "SSWP",
        "ISWP": "ISWP",
        "SISWP": "SISWP",
        "CP": "CP",
        "FSIM": "FSIM",
        # ---Advanced Operations---
        # ! Note: Not supported now!
        # "SET": "SET",
        # "CMT": "CMT",
        # "I": "I",
        # "X12": "X12",
        # "X23": "X23",
        # "AXY": "AXY",
        # "DTN": "DTN",
        # "PLS": "PLS",
        # "PLSXY": "PLSXY",
        # "SWD": "SWD",
        # "SWA": "SWA",
        # "MOV": "MOV",
    }

    tokens = ["FLOAT", "QREG", "NEWLINE"] + list(reserved.values())

    def t_FLOAT(self, t):
        r"""[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)?"""
        # r"[-]?\d+(\.\d+)?"
        t.value = float(t.value)

        return t

    def t_QREG(self, t):
        r"""[a-zA-Z_][\.a-zA-Z_0-9]*"""
        # If it is an identifier but not a reserved word, then it must be QREG
        t.type = self.reserved.get(t.value, "QREG")
        return t

    def t_NEWLINE(self, t):
        r"""\n"""
        self.lineno += len(t.value)
        t.lexer.lineno = self.lineno
        return t

    t_ignore = " \t"
    # Note that `.` can not match \n
    t_ignore_COMMENT = r"\#.*"

    def find_column(self, t):
        """Compute the column of the token t."""
        if t is None:
            return 0
        last_line_end = self.data.rfind("\n", 0, t.lexpos)
        column = t.lexpos - last_line_end
        return column

    def t_error(self, t):
        # When a token has no matching rule, `t.value` will contain the rest of input.
        # Thus we usually only report the string before the first space, \n or \t.
        raise ValueError(
            "Give string ({}) at (line {}, col {}) cannot match any QCIS token rule".format(
                t.value.split(" ")[0].split("\n")[0].split("\t")[0],
                t.lexer.lineno,
                self.find_column(t),
            )
        )

    def get_all_token(self):
        return [tok for tok in self.lexer]

    def get_all_token_info(self):
        return [(tok.type, tok.value, tok.lineno, tok.lexpos) for tok in self.lexer]
