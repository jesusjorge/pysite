import tkinter as tk
import math
import random

WIDTH = 800
HEIGHT = 600
GRAVITY = 9.8

class GorillasGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Gorillas")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.buildings = []
        self.gorillas = []
        self.current_player = 0  # 0 or 1
        self.banana = None

        self.generate_city()
        self.place_gorillas()

        self.angle_entry = tk.Entry(root, width=5)
        self.angle_entry.pack(side="left")
        self.angle_entry.insert(0, "45")

        self.vel_entry = tk.Entry(root, width=5)
        self.vel_entry.pack(side="left")
        self.vel_entry.insert(0, "50")

        self.fire_button = tk.Button(root, text="Fire!", command=self.fire)
        self.fire_button.pack(side="left")

        self.status = tk.Label(root, text="Player 1's turn")
        self.status.pack(side="left")

    def generate_city(self):
        x = 0
        while x < WIDTH:
            w = random.randint(40, 80)
            h = random.randint(100, 300)
            b = self.canvas.create_rectangle(x, HEIGHT-h, x+w, HEIGHT, fill="gray")
            self.buildings.append((x, x+w, HEIGHT-h, b))
            x += w

    def place_gorillas(self):
        left_building = self.buildings[2]
        right_building = self.buildings[-3]

        x1 = (left_building[0] + left_building[1]) // 2
        y1 = left_building[2]
        g1 = self.canvas.create_oval(x1-10, y1-30, x1+10, y1-10, fill="orange")

        x2 = (right_building[0] + right_building[1]) // 2
        y2 = right_building[2]
        g2 = self.canvas.create_oval(x2-10, y2-30, x2+10, y2-10, fill="orange")

        self.gorillas = [(x1, y1-20, g1), (x2, y2-20, g2)]

    def fire(self):
        try:
            angle = float(self.angle_entry.get())
            velocity = float(self.vel_entry.get())
        except:
            self.status.config(text="Invalid input!")
            return

        if self.banana:
            self.canvas.delete(self.banana)

        x0, y0, _ = self.gorillas[self.current_player]
        angle_rad = math.radians(angle)

        # Adjust angle for player 2 (reverse shot)
        if self.current_player == 1:
            angle_rad = math.pi - angle_rad

        vx = velocity * math.cos(angle_rad)
        vy = -velocity * math.sin(angle_rad)

        # Offset banana from gorilla so it doesn't trigger instant hit
        x0 += 15 if self.current_player == 0 else -15

        self.animate_banana(x0, y0, vx, vy, 0)

    def animate_banana(self, x, y, vx, vy, t):
        if self.banana:
            self.canvas.delete(self.banana)

        xt = x + vx * t
        yt = y + vy * t + 0.5 * GRAVITY * t**2

        if xt < 0 or xt > WIDTH or yt > HEIGHT:
            self.status.config(text="Missed! Switching turn...")
            self.current_player = 1 - self.current_player
            self.status.config(text=f"Player {self.current_player + 1}'s turn")
            return

        self.banana = self.canvas.create_oval(xt-5, yt-5, xt+5, yt+5, fill="yellow")

        # Check for collision with opponent
        enemy_index = 1 - self.current_player
        gx, gy, _ = self.gorillas[enemy_index]
        if abs(xt - gx) < 15 and abs(yt - gy) < 15:
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f"Player {self.current_player + 1} Wins!", font=("Arial", 24), fill="red")
            return

        self.root.after(30, lambda: self.animate_banana(x, y, vx, vy, t + 0.3))

if __name__ == "__main__":
    root = tk.Tk()
    game = GorillasGame(root)
    root.mainloop()
