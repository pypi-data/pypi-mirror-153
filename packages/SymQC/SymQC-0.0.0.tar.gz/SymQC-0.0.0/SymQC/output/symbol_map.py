from sympy import symbols


class symbol_map:
    def __init__(self):
        self.symbol_table = {}
        self.theta = 0
        self.phi = 0
        self.use = False

    def store_symbol(self, type, val) -> symbols:
        self.use = True
        if type == 'theta':
            symbol = symbols('theta' + str(self.theta))
            self.theta += 1
            self.symbol_table[symbol] = val
            return symbol
        elif type == 'phi':
            symbol = symbols('phi' + str(self.phi))
            self.phi += 1
            self.symbol_table[symbol] = val
            return symbol

    def get_symbol(self, symbol: symbols):
        return self.symbol_table[symbol]
