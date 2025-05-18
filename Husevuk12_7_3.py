import re, glob
from math import gcd

class RationalError(ZeroDivisionError):
    """Кидається, коли при створенні Rational знаменник = 0."""
    def __init__(self, message="Знаменник не може бути нуль"):
        print(f"[RationalError] {message}")
        super().__init__(message)

class RationalValueError(ValueError):
    """Кидається при некоректних даних у конструкторі або при операціях."""
    def __init__(self, message="Некоректні дані для Rational"):
        print(f"[RationalValueError] {message}")
        super().__init__(message)

class Rational:
    def __init__(self, a, b=None):
        if b is None:
            if isinstance(a, Rational):
                self.n, self.d = a.n, a.d
            elif isinstance(a, (str, int)):
                s = str(a)
                if '/' in s:
                    parts = s.split('/')
                    if len(parts) != 2:
                        raise RationalValueError(f"Не вдалося розпарсити '{s}' як n/d")
                    n, d = parts
                    self.n, self.d = int(n), int(d)
                else:
                    self.n, self.d = int(s), 1
            else:
                raise RationalValueError(f"Непідтримуваний тип {type(a)} у конструкторі")
        else:
            self.n, self.d = int(a), int(b)
        if self.d == 0:
            raise RationalError()
        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    def __str__(self):
        return f"{self.n}/{self.d}"

    def __call__(self):
        return self.n / self.d

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
                raise RationalError("Знаменник 0")
            self.d = int(value)
        else:
            raise KeyError("Ключ має бути 'n' або 'd'")

        g = gcd(self.n, self.d)
        self.n //= g; self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    def _to_rat(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other, 1)
        raise RationalValueError(f"Непідтримуваний операнд типу {type(other)}")

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
            raise RationalError("Ділення на нуль")
        return Rational(self.n*o.d, self.d*o.n)

class RationalList:
    def __init__(self):
        self.data = []

    def append(self, value):
        try:
            if isinstance(value, Rational):
                r = value
            else:
                r = Rational(value)
        except (RationalError, RationalValueError) as e:
            raise RationalValueError(f"Не вдалось додати '{value}': {e}")
        else:
            self.data.append(r)

    def __iter__(self):
        seen = set()
        for r in sorted(self.data, key=lambda x: (-x.d, -x.n)):
            key = (r.n, r.d)
            if key not in seen:
                seen.add(key)
                yield r

def process_file(fname, fout):
    rl = RationalList()
    with open(fname, 'r', encoding='utf-8') as f:
        for line in f:
            for tok in re.findall(r'-?\d+/\d+|-?\d+', line):
                try:
                    rl.append(tok)
                except RationalValueError as e:
                    fout.write(f"{fname}: помилка додавання {tok} – {e}\n")
    fout.write(f"=== {fname} ===\n")
    for r in rl:
        fout.write(str(r) + "\n")
    fout.write("\n")

def main():
    files = sorted(glob.glob("input00[1-3].txt"))
    with open("output12.txt", "w", encoding='utf-8') as fout:
        for fname in files:
            process_file(fname, fout)

if __name__ == "__main__":
    main()
