import turtle
from datetime import datetime

class ClockFace:
    def __init__(self, radius=200):
        self.radius = radius
    def draw(self, t):
        t.clear()
        t.penup()
        t.goto(0, -self.radius)
        t.pendown()
        t.circle(self.radius)
        for i in range(12):
            angle = i * 30
            label = 12 if i == 0 else i
            t.penup()
            t.goto(0, 0)
            t.setheading(90 - angle)
            t.forward(self.radius * 0.85)
            t.write(str(label), align="center", font=("Arial", 14, "normal"))

class Hand:
    def __init__(self, length, thickness, color):
        self.length = length
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.t.pensize(thickness)
        self.t.color(color)
    def draw(self, angle):
        self.t.clear()
        self.t.penup()
        self.t.goto(0, 0)
        self.t.setheading(90 - angle)
        self.t.pendown()
        self.t.forward(self.length)

class AnalogWatch:
    def __init__(self, face_radius):
        self.face = ClockFace(face_radius)
        self.face_turtle = turtle.Turtle()
        self.face_turtle.hideturtle()
        self.face_turtle.speed(0)
        self.face.draw(self.face_turtle)
        self.sec_hand  = Hand(face_radius * 0.9, 1, "red")
        self.min_hand  = Hand(face_radius * 0.8, 3, "blue")
        self.hour_hand = Hand(face_radius * 0.6, 6, "black")

    def update(self):
        now = datetime.now()
        sec_ang  = now.second * 6
        min_ang  = now.minute * 6 + now.second * 0.1
        hour_ang = (now.hour % 12) * 30 + now.minute * 0.5
        self.sec_hand.draw(sec_ang)
        self.min_hand.draw(min_ang)
        self.hour_hand.draw(hour_ang)

    def redraw_face(self):
        self.face.draw(self.face_turtle)

class DigitalWatch:
    def __init__(self, use_24_hour=True):
        self.use_24 = use_24_hour
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
    def update(self):
        now = datetime.now()
        self.t.clear()
        fmt = "%H:%M:%S" if self.use_24 else "%I:%M:%S %p"
        time_str = now.strftime(fmt)
        self.t.goto(0, 220)
        self.t.write(time_str, align="center", font=("Arial", 18, "bold"))

class WatchApp:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(600, 600)
        self.screen.title("Turtle Clock")
        self.mode = "analog"
        self.theme = "light"

        self.analog = AnalogWatch(200)
        self.digital = DigitalWatch(use_24_hour=False)

        self.instr = turtle.Turtle()
        self.instr.hideturtle()
        self.instr.penup()
        self.instr.goto(0, -260)
        self.instr.write(
            "Keys: [m] –Змінити годинник   "
            "[t] – темна чи світла тема   "
            "[Space] – 12/24 години",
            align="center", font=("Arial", 12, "normal")
        )

        self.screen.listen()
        self.screen.onkey(self.toggle_mode, "m")
        self.screen.onkey(self.toggle_theme, "t")
        self.screen.onkey(self.switch_24h, "space")

        self.apply_theme()
        self._update_loop()

    def apply_theme(self):
        bg = "lightyellow" if self.theme=="light" else "darkslategray"
        self.screen.bgcolor(bg)

    def toggle_mode(self):
        self.mode = "digital" if self.mode=="analog" else "analog"
        if self.mode == "analog":
            self.analog.redraw_face()

    def switch_24h(self):
        self.digital.use_24 = not self.digital.use_24

    def toggle_theme(self):
        self.theme = "dark" if self.theme=="light" else "light"
        self.apply_theme()

    def _update_loop(self):
        if self.mode == "analog":
            self.digital.t.clear()
            self.analog.update()
        else:
            self.analog.sec_hand.t.clear()
            self.analog.min_hand.t.clear()
            self.analog.hour_hand.t.clear()
            self.digital.update()
        self.screen.ontimer(self._update_loop, 1000)
    def run(self):
        turtle.done()

if __name__ == "__main__":
    WatchApp().run()
