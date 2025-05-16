import math

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_valid(self):
        return self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def perimeter(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.b

class Trapeze:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def is_valid(self):
        try:
            h = self.height()
            return h > 0
        except:
            return False

    def height(self):
        return math.sqrt(self.c**2 - ((self.b - self.a)**2) / 4)

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        h = self.height()
        return ((self.a + self.b) / 2) * h

class Parallelogram:
    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h

    def perimeter(self):
        return 2 * (self.a + self.b)

    def area(self):
        return self.a * self.h

class Circle:
    def __init__(self, r):
        self.r = r

    def perimeter(self):
        return 2 * math.pi * self.r

    def area(self):
        return math.pi * self.r**2

def read_figures(filename):
    figures = []
    descriptions = []
    try:
        f = open(filename, "r")
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split()
            name = parts[0]
            params = list(map(float, parts[1:]))
            try:
                if name == "Triangle":
                    t = Triangle(*params)
                    if t.is_valid():
                        figures.append(t)
                        descriptions.append((t, name, params))
                elif name == "Rectangle":
                    r = Rectangle(*params)
                    figures.append(r)
                    descriptions.append((r, name, params))
                elif name == "Trapeze":
                    tr = Trapeze(*params)
                    if tr.is_valid():
                        figures.append(tr)
                        descriptions.append((tr, name, params))
                elif name == "Parallelogram":
                    p = Parallelogram(*params)
                    figures.append(p)
                    descriptions.append((p, name, params))
                elif name == "Circle":
                    c = Circle(*params)
                    figures.append(c)
                    descriptions.append((c, name, params))
                else:
                    print("Помилка, неіснуюча фігура")
            except Exception:
                print("Помилка, некоректні параметри")
        f.close()
    except FileNotFoundError:
        print(f"Файл {filename} існує!!!")
    return figures, descriptions

def find_max(figures):
    if not figures:
        return None, None
    max_area = figures[0]
    max_perimeter = figures[0]
    for fig in figures:
        if fig.area() > max_area.area():
            max_area = fig
        if fig.perimeter() > max_perimeter.perimeter():
            max_perimeter = fig
    return max_area, max_perimeter

def main():
    input_file = "input03.txt"
    output_file = "output03.txt"

    figures, descriptions = read_figures(input_file)
    max_area, max_perimeter = find_max(figures)

    try:
        out = open(output_file, "w")

        if max_area and max_perimeter:
            out.write(f"Фігура з найбільшою площею: {type(max_area).__name__}, площа = {max_area.area():.2f}\n")
            out.write(f"Фігура з найбільшим периметром: {type(max_perimeter).__name__}, периметр = {max_perimeter.perimeter():.2f}\n")

        for fig, name, params in descriptions:
            out.write(f"{name} ({', '.join(map(str, params))}) => Площа: {fig.area():.2f}, Периметр: {fig.perimeter():.2f}\n")

        out.close()
        print(f"Результати записано у {output_file}")
    except Exception as e:
        print("Файл не існує!!!", e)


if __name__ == "__main__":
    main()

