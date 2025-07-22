import tkinter as tk
import math
import random

# Constants
WIDTH = 800
HEIGHT = 600
GRAVITY = 9.8
BANANA_RADIUS = 5

class GorillasGame:
    def __init__(self, root):
        self.root = root
        self.root.title("GORILLAS.PY")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()
        self.ui_frame = tk.Frame(root)
        self.ui_frame.pack()

        self.angle_label = tk.Label(self.ui_frame, text="Angle:")
        self.angle_label.pack(side="left")
        self.angle_entry = tk.Entry(self.ui_frame, width=5)
        self.angle_entry.pack(side="left")

        self.vel_label = tk.Label(self.ui_frame, text="Velocity:")
        self.vel_label.pack(side="left")
        self.vel_entry = tk.Entry(self.ui_frame, width=5)
        self.vel_entry.pack(side="left")

        self.fire_button = tk.Button(self.ui_frame, text="Throw!", command=self.fire)
        self.fire_button.pack(side="left")

        self.status = tk.Label(self.ui_frame, text="Welcome to GORILLAS!")
        self.status.pack(side="left")

        self.wind = random.uniform(-5, 5)
        self.wind_label = tk.Label(self.ui_frame, text=f"Wind: {self.wind:.1f}")
        self.wind_label.pack(side="left")

        self.buildings = []
        self.gorillas = []
        self.current_player = 0
        self.banana = None
        self.exploding = False

        self.draw_city()
        self.place_gorillas()

    def draw_city(self):
        x = 0
        while x < WIDTH:
            w = random.randint(40, 70)
            h = random.randint(100, 300)
            self.canvas.create_rectangle(x, HEIGHT-h, x+w, HEIGHT, fill="dimgray")
            self.buildings.append((x, x+w, HEIGHT-h))
            x += w

    def place_gorillas(self):
        b1 = self.buildings[2]
        b2 = self.buildings[-3]

        def draw_gorilla(xc, ytop):
            head = self.canvas.create_oval(xc-10, ytop-30, xc+10, ytop-10, fill="orange", outline="black")
            arm = self.canvas.create_line(xc-10, ytop-20, xc+10, ytop-20, width=4)
            return (xc, ytop-20, head, arm)

        x1 = (b1[0] + b1[1]) // 2
        y1 = b1[2]
        self.gorillas.append(draw_gorilla(x1, y1))

        x2 = (b2[0] + b2[1]) // 2
        y2 = b2[2]
        self.gorillas.append(draw_gorilla(x2, y2))

    def fire(self):
        if self.exploding:
            return
        try:
            angle = float(self.angle_entry.get())
            velocity = float(self.vel_entry.get())
        except ValueError:
            self.status.config(text="Enter valid angle/velocity.")
            return

        # Position and velocity setup
        gx, gy, _, _ = self.gorillas[self.current_player]
        angle_rad = math.radians(angle)
        if self.current_player == 1:
            angle_rad = math.pi - angle_rad

        vx = velocity * math.cos(angle_rad) + self.wind
        vy = -velocity * math.sin(angle_rad)
        self.throw_banana(gx + (15 if self.current_player == 0 else -15), gy, vx, vy)

    def throw_banana(self, x, y, vx, vy):
        self.t = 0
        self.banana_path = []
        self.banana_x0 = x
        self.banana_y0 = y
        self.vx = vx
        self.vy = vy
        self.animate_banana()

    def animate_banana(self):
        t = self.t
        x = self.banana_x0 + self.vx * t
        y = self.banana_y0 + self.vy * t + 0.5 * GRAVITY * t**2
        self.t += 0.2

        if self.banana:
            self.canvas.delete(self.banana)

        if x < 0 or x > WIDTH or y > HEIGHT:
            self.next_turn("Missed!")
            return

        self.banana = self.canvas.create_oval(x-BANANA_RADIUS, y-BANANA_RADIUS, x+BANANA_RADIUS, y+BANANA_RADIUS, fill="yellow")
        self.banana_path.append((x, y))

        # Trail
        if len(self.banana_path) % 2 == 0:
            self.canvas.create_oval(x-1, y-1, x+1, y+1, fill="black")

        if self.check_hit(x, y):
            self.explode(x, y)
            return

        self.root.after(30, self.animate_banana)

    def check_hit(self, x, y):
        enemy = 1 - self.current_player
        gx, gy, _, _ = self.gorillas[enemy]
        return abs(x - gx) < 15 and abs(y - gy) < 15

    def explode(self, x, y):
        self.exploding = True
        self.explosion_radius = 1

        def expand():
            if self.explosion_radius > 30:
                self.status.config(text=f"Player {self.current_player + 1} WINS!")
                self.fire_button.config(state="disabled")
                return
            r = self.explosion_radius
            self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="red", width=2)
            self.explosion_radius += 3
            self.root.after(50, expand)

        expand()

    def next_turn(self, msg):
        self.current_player = 1 - self.current_player
        self.status.config(text=f"{msg} Player {self.current_player + 1}'s turn")
        self.wind = random.uniform(-5, 5)
        self.wind_label.config(text=f"Wind: {self.wind:.1f}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GorillasGame(root)
    root.mainloop()
