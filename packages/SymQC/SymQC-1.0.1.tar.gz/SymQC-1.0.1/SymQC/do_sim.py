from argparse import ArgumentParser
from pathlib import Path
from sympy import init_printing
from SymQC.QCIS.parser import QCISParser, QCISOpCode
from SymQC.kernel.qubit import Qsim_state
from SymQC.kernel.ket.qubit import Qsim_ket
from SymQC.kernel.ket.store import store_ket
from SymQC.output.store import store
from SymQC.output.symbol_map import symbol_map

"""
The main programme
"""


def compiler(_prog):
    """"""
    _parser = QCISParser()
    success, instructions, name = _parser.parse(data=_prog)
    if not success:
        print(_parser.error_list)
        raise ValueError(
            "QCIS parser failed to compile the given QCIS program.")

    return instructions, name


# 1. Argument parsing
my_parser = ArgumentParser(description='QCIS simulator system based on symbolic operation')

my_parser.add_argument('input', type=str, help='the name of the input QCIS file')

my_parser.add_argument('-l', '--output_list', required=False, nargs='+', type=int, default=[],
                       help='the index of the instr we need the ans.')

my_parser.add_argument('-o', '--obj_name', required=False, type=str, default="a.md",
                       help='the filename of Markdown file.')

my_parser.add_argument('-N', required=False, type=int, help='the number of qubits in the symbolic simulator')

my_parser.add_argument("-s", "--symbol", help="use the symbol args", action="store_true")

my_parser.add_argument("-k", "--ket", help="Use the ket present", action="store_true")

args = my_parser.parse_args()

qcis_fn = Path(args.input).resolve()

if qcis_fn.suffix != '.qcis':
    raise ValueError(
        "Error: the input file name should end with the suffix '.qcis'.")

if not qcis_fn.exists():
    raise ValueError("cannot find the given file: {}".format(qcis_fn))

# 2. Read the QCIS file
prog = qcis_fn.open('r').read()

job_arr, names = compiler(prog)


max_q = len(names)
if args.N is not None and args.N > max_q:
    max_q = args.N

# 3. Start simulating
maps = symbol_map()

if args.symbol:
    for instr in job_arr:
        if instr.op_code == QCISOpCode.RXY:
            instr.altitude = maps.store_symbol("theta", instr.altitude)
            instr.azimuth = maps.store_symbol("phi", instr.azimuth)
        elif instr.op_code == QCISOpCode.XY or instr.op_code == QCISOpCode.XY2P or instr.op_code == QCISOpCode.XY2M:
            instr.azimuth = maps.store_symbol("phi", instr.azimuth)
        elif instr.op_code == QCISOpCode.RX or instr.op_code == QCISOpCode.RY or instr.op_code == QCISOpCode.RZ:
            instr.altitude = maps.store_symbol("theta", instr.azimuth)

if args.ket:
    Q = Qsim_ket(max_q, names, maps)
    save = store_ket(Q, maps, args.output_list)
else:
    Q = Qsim_state(max_q, names)
    save = store(Q, maps, args.output_list)


init_printing()
idx = 1
for instr in job_arr:
    gate = Q.apply_instr(instr)
    if idx in save.out_list:
        save.save_instr(Q.state, instr, gate)
    idx += 1
save.save_final(Q.state)
save.output_markdown(args.input, args.obj_name)
