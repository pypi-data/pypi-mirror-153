import sympy
from SymQC.QCIS.instr import QCISOpCode, QCIS_instr


sigma_x = sympy.Matrix([[0, 1], [1, 0]])
sigma_y = sympy.Matrix([[0, -sympy.I], [sympy.I, 0]])
sigma_z = sympy.Matrix([[1, 0], [0, -1]])


def R(n_head, theta):
    sympy.Matrix([sigma_x, sigma_y, sigma_z])
    n1 = n_head[0]
    n2 = n_head[1]
    n3 = n_head[2]
    sigma = sigma_x * n1 + sigma_y * n2 + sigma_z * n3
    return sympy.exp(-sympy.I * theta * sigma / 2)


def X(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[0, 1], [1, 0]])


def Y(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[0, -sympy.I], [sympy.I, 0]])


def X2P(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, -sympy.I], [-sympy.I, 1]]) * (1 / sympy.sqrt(2))


def X2M(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, sympy.I], [sympy.I, 1]]) * (1 / sympy.sqrt(2))


def Y2P(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, -1], [1, 1]]) * (1 / sympy.sqrt(2))


def Y2M(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 1], [-1, 1]]) * (1 / sympy.sqrt(2))


def XY(*argv):
    if len(argv) != 1:
        print("error argv input")
        exit(1)
    phi = argv[0]
    n_head = sympy.Matrix([sympy.cos(phi), sympy.sin(phi), 0])
    return R(n_head, sympy.pi)


def XY2P(*argv):
    if len(argv) != 1:
        print("error argv input")
        exit(1)
    phi = argv[0]
    n_head = sympy.Matrix([sympy.cos(phi), sympy.sin(phi), 0])
    return R(n_head, sympy.pi / 2)


def XY2M(*argv):
    return XY2P(argv).transpose().conjugate()


def Z(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sigma_z


def S(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0], [0, sympy.I]])


def SD(*argv):
    return S(argv).transpose().conjugate()


def T(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0], [0, sympy.exp(sympy.I * sympy.pi / 4)]])


def TD(*argv):
    return T(argv).transpose().conjugate()


def RZ(*argv):
    if len(argv) != 1:
        print("error argv input")
        exit(1)
    phi = argv[0]
    # sympy.pprint(sympy.exp(-sympy.I * sigma_z * sympy.pi / 2))
    return sympy.exp(-sympy.I * sigma_z * phi / 2)


def CZ(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0], [0, -1]])


def M(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[0, 0], [0, 1]])


def B(*argv):
    exit(len(argv))


def H(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 1], [1, -1]]) * (1 / sympy.sqrt(2))


def RX(*argv):
    if len(argv) != 1:
        print("error argv input")
        exit(1)
    phi = argv[0]
    return sympy.exp(-sympy.pi * sigma_x * phi / 2)


def RY(*argv):
    if len(argv) != 1:
        print("error argv input")
        exit(1)
    phi = argv[0]
    return sympy.exp(-sympy.pi * sigma_y * phi / 2)


def RXY(*argv):
    if len(argv) != 2:
        print("error argv input")
        exit(1)
    theta = argv[0]
    phi = argv[1]
    n_head = sympy.Matrix([sympy.cos(phi), sympy.sin(phi), 0])
    return R(n_head, theta)


def CNOT(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[0, 1], [1, 0]])


def SWP(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 0, 1, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1]])


def SSWP(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, (1 + sympy.I) / 2, (1 - sympy.I) / 2, 0],
                         [0, (1 - sympy.I) / 2, (1 + sympy.I) / 2, 0],
                         [0, 0, 0, 1]])


def ISWP(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 0, sympy.I, 0],
                         [0, sympy.I, 0, 0],
                         [0, 0, 0, 1]])


def SISWP(*argv):
    if len(argv) != 0:
        print("error argv input")
        exit(1)
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 1 / sympy.sqrt(2), sympy.I / sympy.sqrt(2), 0],
                         [0, sympy.I / sympy.sqrt(2), 1 / sympy.sqrt(2), 0],
                         [0, 0, 0, 1]])


def CP(*argv):
    if len(argv) != 1:
        print("error argv input")
        exit(1)
    phi = argv[0]
    return sympy.Matrix([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, sympy.exp(sympy.I * phi)]])


delta_plus = 0
delta_minus = 0
delta_minus_off = 0


def FSIM(*argv):
    if len(argv) != 2:
        print("error argv input")
        exit(1)
    phi = argv[0]
    theta = argv[1]
    return sympy.Matrix([1, 0, 0, 0],
                        [0, sympy.exp(sympy.I * (delta_plus + delta_minus)) * sympy.cos(theta),
                         -sympy.I * sympy.exp(sympy.I * (delta_plus - delta_minus_off)) * sympy.sin(theta), 0],
                        [0, sympy.exp(sympy.I * (delta_plus + delta_minus_off)) * sympy.sin(theta),
                         sympy.exp(sympy.I * (delta_plus - delta_minus)) * sympy.cos(theta), 0],
                        [0, 0, 0, sympy.exp(sympy.I * (2 * delta_plus - phi))])


QCIS_gate = {
    QCISOpCode.X: X,
    QCISOpCode.Y: Y,
    QCISOpCode.X2P: X2P,
    QCISOpCode.X2M: X2M,
    QCISOpCode.Y2P: Y2P,
    QCISOpCode.Y2M: Y2M,
    QCISOpCode.XY: XY,
    QCISOpCode.XY2P: XY2P,
    QCISOpCode.XY2M: XY2M,
    QCISOpCode.Z: Z,
    QCISOpCode.S: S,
    QCISOpCode.SD: SD,
    QCISOpCode.T: T,
    QCISOpCode.TD: TD,
    QCISOpCode.RZ: RZ,
    QCISOpCode.CZ: CZ,
    QCISOpCode.M: M,
    QCISOpCode.B: B,
    QCISOpCode.H: H,
    QCISOpCode.RX: RX,
    QCISOpCode.RY: RY,
    QCISOpCode.RXY: RXY,
    QCISOpCode.CNOT: CNOT,
    QCISOpCode.SWP: SWP,
    QCISOpCode.SSWP: SSWP,
    QCISOpCode.ISWP: ISWP,
    QCISOpCode.SISWP: SISWP,
    QCISOpCode.CP: CP,
    QCISOpCode.FSIM: FSIM
}


def lib_gate(instr: QCIS_instr):
    if instr.op_code == QCISOpCode.RXY:
        return QCIS_gate[instr.op_code](instr.altitude, instr.azimuth)
    elif instr.op_code == QCISOpCode.XY or instr.op_code == QCISOpCode.XY2P or instr.op_code == QCISOpCode.XY2M:
        return QCIS_gate[instr.op_code](instr.azimuth)
    elif instr.op_code == QCISOpCode.RX or instr.op_code == QCISOpCode.RY or instr.op_code == QCISOpCode.RZ:
        return QCIS_gate[instr.op_code](instr.altitude)
    else:
        return QCIS_gate[instr.op_code]()
