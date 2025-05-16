import math

class Figure:
    def dimention(self):
        pass
    def perimetr(self):
        return None
    def square(self):
        return None
    def squareSurface(self):
        return None
    def squareBase(self):
        return None
    def height(self):
        return None
    def volume(self):
        pass

class Dim2Figure(Figure):
    def dimention(self):
        return 2
    def volume(self):
        return self.square()

class Dim3Figure(Figure):
    def dimention(self):
        return 3

class Triangle(Dim2Figure):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def perimetr(self):
        return self.a + self.b + self.c
    def square(self):
        if self.a + self.b <= self.c or self.a + self.c <= self.b or self.b + self.c <= self.a:
            raise ValueError("Неможливий трикутник")
        p = self.perimetr() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

class Rectangle(Dim2Figure):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def perimetr(self):
        return 2 * (self.a + self.b)
    def square(self):
        return self.a * self.b

class Trapeze(Dim2Figure):
    def __init__(self, a, b, c, d, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
    def perimetr(self):
        return self.a + self.b + self.c + self.d
    def square(self):
        return (self.a + self.b) * self.h / 2

class Parallelogram(Dim2Figure):
    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h
    def perimetr(self):
        return 2 * (self.a + self.b)
    def square(self):
        return self.a * self.h

class Circle(Dim2Figure):
    def __init__(self, r):
        self.r = r
    def perimetr(self):
        return 2 * math.pi * self.r
    def square(self):
        return math.pi * self.r * self.r

class Ball(Dim3Figure):
    def __init__(self, r):
        self.r = r
    def squareSurface(self):
        return 4 * math.pi * self.r * self.r
    def volume(self):
        return 4 / 3 * math.pi * self.r**3

class TriangularPyramid(Dim3Figure):
    def __init__(self, a, h):
        self.a = a
        self.h = h
    def squareBase(self):
        return math.sqrt(3) / 4 * self.a**2
    def height(self):
        return self.h
    def volume(self):
        return self.squareBase() * self.h / 3

class QuadrangularPyramid(Dim3Figure):
    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h
    def squareBase(self):
        return self.a * self.b
    def height(self):
        return self.h
    def volume(self):
        return self.squareBase() * self.h / 3

class RectangularParallelepiped(Dim3Figure):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def squareSurface(self):
        return 2 * (self.a * self.b + self.a * self.c + self.b * self.c)
    def volume(self):
        return self.a * self.b * self.c

class Cone(Dim3Figure):
    def __init__(self, r, h):
        self.r = r
        self.h = h
    def squareBase(self):
        return math.pi * self.r**2
    def height(self):
        return self.h
    def volume(self):
        return math.pi * self.r**2 * self.h / 3

class TriangularPrism(Dim3Figure):
    def __init__(self, a, b, c, h):
        self.a = a
        self.b = b
        self.c = c
        self.h = h
    def squareBase(self):
        if self.a + self.b <= self.c or self.a + self.c <= self.b or self.b + self.c <= self.a:
            raise ValueError("Неможливий трикутник у основі")
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
    def height(self):
        return self.h
    def volume(self):
        return self.squareBase() * self.h

figures_map = {
    "Triangle": Triangle,
    "Rectangle": Rectangle,
    "Trapeze": Trapeze,
    "Parallelogram": Parallelogram,
    "Circle": Circle,
    "Ball": Ball,
    "TriangularPyramid": TriangularPyramid,
    "QuadrangularPyramid": QuadrangularPyramid,
    "RectangularParallelepiped": RectangularParallelepiped,
    "Cone": Cone,
    "TriangularPrism": TriangularPrism
}

if __name__ == "__main__":
    input_files = ["input11.txt", "input22.txt", "input33.txt"]
    with open("output.txt", "w") as out:
        for fname in input_files:
            max_val = -1
            max_fig = None
            with open(fname) as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.strip().split()
                    name = parts[0].strip()
                    args = list(map(float, parts[1:]))
                    if name in figures_map:
                        try:
                            fig = figures_map[name](*args)
                            val = fig.volume()
                            if val is not None and val > max_val:
                                max_val = val
                                max_fig = (name, args, round(val, 3), fig.dimention())
                        except Exception:
                            continue
            if max_fig:
                name, args, val, dim = max_fig
                out.write(f"{fname}: {name} {args}, розмірність: {dim}, міра: {val}\n")
