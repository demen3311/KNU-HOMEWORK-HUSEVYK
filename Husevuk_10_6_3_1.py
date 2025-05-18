import re
from math import gcd
import glob

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
                raise ValueError("ValueError")
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

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, Rational) and self.n == other.n and self.d == other.d

    def __hash__(self):
        return hash((self.n, self.d))

class RationalList:
    def __init__(self):
        self.data = []

    def append(self, value):
        if isinstance(value, Rational):
            r = value
        elif isinstance(value, str):
            r = Rational(value)
        elif isinstance(value, int):
            r = Rational(value, 1)
        else:
            raise TypeError("ValueError")
        self.data.append(r)

    def __iter__(self):
        sorted_list = sorted(self.data, key=lambda r: (-r.d, -r.n))
        seen = set()
        for r in sorted_list:
            if r not in seen:
                seen.add(r)
                yield r

def process_list_file(filename):
    rl = RationalList()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            for tok in re.findall(r'-?\d+/\d+|-?\d+', line):
                rl.append(tok)
    return rl

def iterations(output_file):
    files = sorted(glob.glob("input00[1-3].txt"))
    with open(output_file, 'w', encoding='utf-8') as fout:
        for fname in files:
            fout.write(f"=== {fname} ===\n")
            for r in process_list_file(fname):
                fout.write(f"{r}\n")
            fout.write("\n")


if __name__ == "__main__":
    iterations("output_iter.txt")