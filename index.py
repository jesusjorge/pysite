import tkinter as tk
import math
import random

WIDTH = 800
HEIGHT = 600
GRAVITY = 9.8

class GorillaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("GORILLAS.PY")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.wind = random.randint(-10, 10)
        self.players = ["Player 1", "Player 2"]
        self.current_player = 0

        self.angle_entry = tk.Entry(root, width=5)
        self.angle_entry.pack(side="left")
        self.angle_entry.insert(0, "45")

        self.velocity_entry = tk.Entry(root, width=5)
        self.velocity_entry.pack(side="left")
        self.velocity_entry.insert(0, "50")

        self.throw_button = tk.Button(root, text="Throw", command=self.throw_banana)
        self.throw_button.pack(side="left")

        self.status = tk.Label(root, text=f"{self.players[0]}'s turn | Wind: {self.wind}")
        self.status.pack(side="left")

        self.buildings = []
        self.gorillas = []

        self.generate_city()
        self.place_gorillas()

    def generate_city(self):
        x = 0
        while x < WIDTH:
            w = random.randint(40, 70)
            h = random.randint(100, 300)
            building = self.canvas.create_rectangle(x, HEIGHT - h, x + w, HEIGHT, fill="gray")
            self.buildings.append((x, x + w, HEIGHT - h))
            x += w

    def place_gorillas(self):
        b1 = self.buildings[2]
        b2 = self.buildings[-3]

        def draw_gorilla(x, y):
            return self.canvas.create_oval(x - 10, y - 30, x + 10, y - 10, fill="orange")

        x1 = (b1[0] + b1[1]) // 2
        y1 = b1[2]
        g1 = draw_gorilla(x1, y1)

        x2 = (b2[0] + b2[1]) // 2
        y2 = b2[2]
        g2 = draw_gorilla(x2, y2)

        self.gorillas = [(x1, y1 - 20), (x2, y2 - 20)]

    def throw_banana(self):
        try:
            angle = float(self.angle_entry.get())
            velocity = float(self.velocity_entry.get())
        except ValueError:
            self.status.config(text="Invalid input")
            return

        x0, y0 = self.gorillas[self.current_player]
        angle_rad = math.radians(angle)
        if self.current_player == 1:
            angle_rad = math.pi - angle_rad

        vx = velocity * math.cos(angle_rad) + self.wind
        vy = -velocity * math.sin(angle_rad)

        self.t = 0
        self.banana_start = (x0, y0)
        self.vx = vx
        self.vy = vy
        self.animate_banana()

    def animate_banana(self):
        t = self.t
        x0, y0 = self.banana_start
        x = x0 + self.vx * t
        y = y0 + self.vy * t + 0.5 * GRAVITY * t ** 2
        self.t += 0.2

        if hasattr(self, 'banana') and self.banana:
            self.canvas.delete(self.banana)

        if x < 0 or x > WIDTH or y > HEIGHT:
            self.switch_turn("Missed!")
            return

        self.banana = self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="yellow")

        if self.check_hit(x, y):
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f"{self.players[self.current_player]} wins!", font=("Courier", 24), fill="red")
            self.throw_button.config(state="disabled")
            return

        self.root.after(30, self.animate_banana)

    def check_hit(self, x, y):
        gx, gy = self.gorillas[1 - self.current_player]
        return abs(x - gx) < 15 and abs(y - gy) < 15

    def switch_turn(self, msg):
        self.current_player = 1 - self.current_player
        self.status.config(text=f"{msg} {self.players[self.current_player]}'s turn | Wind: {self.wind}")

if __name__ == "__main__":
    root = tk.Tk()
    GorillaGame(root)
    root.mainloop()
