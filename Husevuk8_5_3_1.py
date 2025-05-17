import re
from math import gcd

class Rational:
    def __init__(self, a, b=None):
        if b is None:
            if isinstance(a, Rational):
                self.n, self.d = a.n, a.d
            elif isinstance(a, str) and '/' in a:
                n, d = map(int, a.split('/'))
                self.n, self.d = n, d
            else:
                raise ValueError("Очікується Rational, 'n/d' або два цілих")
        else:
            self.n, self.d = int(a), int(b)
        if self.d == 0:
            raise ZeroDivisionError("Знаменник не може бути нуль")
        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    def __str__(self):
        return f"{self.n}/{self.d}"

    # виклик у дужках → float
    def __call__(self):
        return self.n / self.d

    # доступ за ключем
    def __getitem__(self, key):
        if key == 'n':
            return self.n
        if key == 'd':
            return self.d
        raise KeyError("Ключ має бути 'n' або 'd'")

    def __setitem__(self, key, value):
        if key == 'n':
            self.n = int(value)
        elif key == 'd':
            if int(value) == 0:
                raise ZeroDivisionError("Знаменник не може бути нуль")
            self.d = int(value)
        else:
            raise KeyError("Ключ має бути 'n' або 'd'")
        # після зміни – скоротити
        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    # допоміжний
    def _to_rat(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other, 1)
        raise TypeError("Операція з цим типом не підтримується")

    def __add__(self, other):
        o = self._to_rat(other)
        return Rational(self.n*o.d + o.n*self.d, self.d*o.d)

    def __sub__(self, other):
        o = self._to_rat(other)
        return Rational(self.n*o.d - o.n*self.d, self.d*o.d)

    def __mul__(self, other):
        o = self._to_rat(other)
        return Rational(self.n*o.n, self.d*o.d)

    def __truediv__(self, other):
        o = self._to_rat(other)
        if o.n == 0:
            raise ZeroDivisionError("Ділення на нуль")
        return Rational(self.n*o.d, self.d*o.n)

def eval_expr(line):
    tokens = re.findall(r'\d+/\d+|\d+|[+\-*/]', line)
    if '/' in tokens[0]:
        res = Rational(tokens[0])
    else:
        res = Rational(int(tokens[0]), 1)
    i = 1
    while i < len(tokens):
        op = tokens[i]
        tok = tokens[i+1]
        cur = Rational(tok) if '/' in tok else Rational(int(tok), 1)
        if op == '+':
            res = res + cur
        elif op == '-':
            res = res - cur
        elif op == '*':
            res = res * cur
        elif op == '/':
            res = res / cur
        i += 2
    return res

def main():
    with open("input111.txt", "r", encoding="utf-8") as fin, \
         open("output111.txt", "w", encoding="utf-8") as fout:

        for line in fin:
            expr = line.strip()
            if not expr:
                continue
            try:
                r = eval_expr(expr)
                fout.write(f"{expr} = {r} ≈ {r():.6f}\n")
            except Exception as e:
                fout.write(f"{expr} -> Error: {e}\n")

if __name__ == "__main__":
    main()
