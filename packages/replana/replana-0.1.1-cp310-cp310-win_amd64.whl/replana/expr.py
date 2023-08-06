from .replana import Arena
from inspect import signature
import math as m


class Expr:
    arena: Arena
    idx: int

    def __init__(self, idx: int, arena: Arena):
        self.idx = idx
        self.arena = arena

    def inv(self):
        idx = self.arena.inv(self.idx)
        return Expr(idx, self.arena)

    def sqrt(self):
        idx = self.arena.sqrt(self.idx)
        return Expr(idx, self.arena)

    def sin(self):
        idx = self.arena.sin(self.idx)
        return Expr(idx, self.arena)

    def cos(self):
        idx = self.arena.cos(self.idx)
        return Expr(idx, self.arena)

    def tan(self):
        idx = self.arena.tan(self.idx)
        return Expr(idx, self.arena)

    def asin(self):
        idx = self.arena.asin(self.idx)
        return Expr(idx, self.arena)

    def acos(self):
        idx = self.arena.acos(self.idx)
        return Expr(idx, self.arena)

    def atan(self):
        idx = self.arena.atan(self.idx)
        return Expr(idx, self.arena)

    def sinh(self):
        idx = self.arena.sinh(self.idx)
        return Expr(idx, self.arena)

    def cosh(self):
        idx = self.arena.cosh(self.idx)
        return Expr(idx, self.arena)

    def tanh(self):
        idx = self.arena.tanh(self.idx)
        return Expr(idx, self.arena)

    def asinh(self):
        idx = self.arena.asinh(self.idx)
        return Expr(idx, self.arena)

    def acosh(self):
        idx = self.arena.acosh(self.idx)
        return Expr(idx, self.arena)

    def atanh(self):
        idx = self.arena.atanh(self.idx)
        return Expr(idx, self.arena)

    def exp(self):
        idx = self.arena.exp(self.idx)
        return Expr(idx, self.arena)

    def ln(self):
        idx = self.arena.ln(self.idx)
        return Expr(idx, self.arena)

    def log(self):
        idx = self.arena.log(self.idx)
        return Expr(idx, self.arena)

    def __neg__(self):
        idx = self.arena.neg(self.idx)
        return Expr(idx, self.arena)

    def __add__(self, other):
        if type(other) == float:
            idx = self.arena.add_f64(self.idx, other)
            return Expr(idx, self.arena)
        elif type(other) == Expr:
            idx = self.arena.add(self.idx, other.idx)
            return Expr(idx, self.arena)

    def __sub__(self, other):
        if type(other) == float:
            idx = self.arena.sub_f64(self.idx, other)
            return Expr(idx, self.arena)
        elif type(other) == Expr:
            idx = self.arena.sub(self.idx, other.idx)
            return Expr(idx, self.arena)

    def __mul__(self, other):
        if type(other) == float:
            if other == 1.0:
                return self
            else:
                idx = self.arena.mul_f64(self.idx, other)
                return Expr(idx, self.arena)
        elif type(other) == Expr:
            idx = self.arena.mul(self.idx, other.idx)
            return Expr(idx, self.arena)

    def __truediv__(self, other):
        if type(other) == float:
            idx = self.arena.div_f64(self.idx, other)
            return Expr(idx, self.arena)
        elif type(other) == Expr:
            idx = self.arena.div(self.idx, other.idx)
            return Expr(idx, self.arena)

    def __radd__(self, other):
        if type(other) == float:
            idx = self.arena.rev_add_f64(other, self.idx)
            return Expr(idx, self.arena)

    def __rsub__(self, other):
        if type(other) == float:
            idx = self.arena.rev_sub_f64(other, self.idx)
            return Expr(idx, self.arena)

    def __rmul__(self, other):
        if type(other) == float:
            idx = self.arena.rev_mul_f64(other, self.idx)
            return Expr(idx, self.arena)

    def __rtruediv__(self, other):
        if type(other) == float:
            idx = self.arena.rev_div_f64(other, self.idx)
            return Expr(idx, self.arena)

    def __pow__(self, other):
        idx = self.arena.pow(self.idx, float(other))
        return Expr(idx, self.arena)


def sqrt(arg):
    if type(arg) == Expr:
        return arg.sqrt()
    else:
        return m.sqrt(arg)


def sin(arg):
    if type(arg) == Expr:
        return arg.sin()
    else:
        return m.sin(arg)


def cos(arg):
    if type(arg) == Expr:
        return arg.cos()
    else:
        return m.cos(arg)


def tan(arg):
    if type(arg) == Expr:
        return arg.tan()
    else:
        return m.tan(arg)


def asin(arg):
    if type(arg) == Expr:
        return arg.asin()
    else:
        return m.asin(arg)


def acos(arg):
    if type(arg) == Expr:
        return arg.acos()
    else:
        return m.acos(arg)


def atan(arg):
    if type(arg) == Expr:
        return arg.atan()
    else:
        return m.atan(arg)


def sinh(arg):
    if type(arg) == Expr:
        return arg.sinh()
    else:
        return m.sinh(arg)


def cosh(arg):
    if type(arg) == Expr:
        return arg.cosh()
    else:
        return m.cosh(arg)


def tanh(arg):
    if type(arg) == Expr:
        return arg.tanh()
    else:
        return m.tanh(arg)


def asinh(arg):
    if type(arg) == Expr:
        return arg.asinh()
    else:
        return m.asinh(arg)


def acosh(arg):
    if type(arg) == Expr:
        return arg.acosh()
    else:
        return m.acosh(arg)


def atanh(arg):
    if type(arg) == Expr:
        return arg.atanh()
    else:
        return m.atanh(arg)


def exp(arg):
    if type(arg) == Expr:
        return arg.exp()
    else:
        return m.exp(arg)


def ln(arg):
    if type(arg) == Expr:
        return arg.ln()
    else:
        return m.log(arg)


def log(arg):
    if type(arg) == Expr:
        return arg.log()
    else:
        return m.log10(arg)


def rustify(num_args):
    arena = Arena()
    args = [Expr(arena.new_var(), arena) for _ in range(num_args)]
    return arena, args


def exmat(func):
    pars = len(signature(func).parameters)
    arena, args = rustify(pars)
    vec = func(*args)
    csts = set()
    for expr in vec:
        if type(expr) is float or type(expr) is int:
            csts.add(float(expr))
    csts = {cst: arena.new_cst(cst) for cst in csts}
    vec = [expr.idx if type(expr) is Expr else csts[expr] for expr in vec]
    return arena, vec
