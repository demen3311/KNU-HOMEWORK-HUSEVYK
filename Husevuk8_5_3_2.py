import re
from math import gcd

class Rational:
    def __init__(self, a, b=None):
        if b is None:
            if isinstance(a, Rational):
                self.n, self.d = a.n, a.d
            elif isinstance(a, str):
                if '/' in a:
                    n, d = map(int, a.split('/'))
                    self.n, self.d = n, d
                else:
                    self.n, self.d = int(a), 1
            else:
                raise ValueError("Очікується Rational або рядок із числом")
        else:
            self.n, self.d = int(a), int(b)

        if self.d == 0:
            raise ZeroDivisionError("Знаменник не може бути нуль")
        g = gcd(self.n, self.d)
        self.n //= g; self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    def __str__(self):
        return f"{self.n}/{self.d}"

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == 'n': return self.n
        if key == 'd': return self.d
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
        g = gcd(self.n, self.d)
        self.n //= g; self.d //= g
        if self.d < 0:
            self.n, self.d = -self.n, -self.d

    def _to_rat(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other, 1)
        raise TypeError("Непідтримуваний тип для арифметичної операції")

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


class RationalList:
    def __init__(self):
        self.data = []

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = self._to_rational(value)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        result = RationalList()
        result.data = self.data[:]
        if isinstance(other, RationalList):
            result.data += other.data
        else:
            result.data.append(self._to_rational(other))
        return result

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            self.data += other.data
        else:
            self.data.append(self._to_rational(other))
        return self

    def append(self, value):
        self.data.append(self._to_rational(value))

    def _to_rational(self, value):
        if isinstance(value, Rational):
            return value
        if isinstance(value, int):
            return Rational(value, 1)
        if isinstance(value, str):
            return Rational(value)
        raise TypeError("Можна додавати тільки Rational, int або рядок-запис дробу")

    def sum(self):
        total = Rational(0, 1)
        for r in self.data:
            total += r
        return total

def process_list_file(filename):
    rl = RationalList()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            for tok in re.findall(r'-?\d+/\d+|-?\d+', line):
                rl.append(tok)
    return rl.sum()


def main():
    input_files = ["input001.txt", "input002.txt", "input003.txt"]
    with open("output_list.txt", "w", encoding="utf-8") as fout:
        for fname in input_files:
            try:
                s = process_list_file(fname)
                fout.write(f"{fname}: сума = {s} ≈ {s():.6f}\n")
            except FileNotFoundError:
                fout.write(f"{fname}: файл не знайдено\n")
if __name__ == "__main__":
    main()