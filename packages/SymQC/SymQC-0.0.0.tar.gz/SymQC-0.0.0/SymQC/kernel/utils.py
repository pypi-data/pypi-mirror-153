from sympy import Matrix, pprint, latex, Abs, im, re


def find_main(state, qubit):
    p0 = 0
    p1 = 0
    for i in range(len(state)):
        num = re(Abs(state[i], evaluate=True).evalf())
        # num = Abs(state[i], evaluate=True).evalf()
        cal = num * num
        if (i >> qubit) & 0x1:
            p1 += cal
        else:
            p0 += cal
    # print(p0, p1)
    return p0, p1


def kron(A, B):
    """Return the Kronecker product of matrix A and matrix B"""
    return Matrix(
        [[A.row(i // B.rows)[j // B.cols] * B.row(i % B.rows)[j % B.cols]
          for j in range(A.cols * B.cols)]
         for i in range(A.rows * B.rows)]
    )


def gen_subset(s):
    res = []
    now = s
    while now:
        res.append(now)
        now = (now - 1) & s
    res.append(now)
    return res


def map_bit(x, s, mapp):
    for i in range(len(mapp)):
        s |= ((x >> i) & 1) << mapp[i]
    return s


def get_mark(num, l):
    """
    
    """
    mark = 0
    for i in num:
        mark |= 1 << i
    if l != 0:
        mark = (~mark) & ((1 << l) - 1)
    return mark


def get_discrete(x):
    rx = sorted([(i, j) for i, j in zip(x, range(len(x)))])
    res = [0] * len(x)
    for i in range(len(rx)):
        res[rx[i][1]] = i
    return res


def str_bin(x, n):
    s = bin(x)[2:]
    return "0" * (n - len(s)) + s


def make_bin(x, n, keys):
    s = str_bin(x, n)
    return "".join(["%s_{%s}" % (i, j) for i, j in zip(s, keys)])


def make_ket(keys: list):
    keys.reverse()
    n = len(keys)
    return [make_bin(i, n, keys) for i in range(1 << n)]
