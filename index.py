import tkinter as tk
import math
import random

WIDTH = 800
HEIGHT = 600
GRAVITY = 9.8

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

        self.throw_button = tk.Button(self.ui_frame, text="Throw Banana", command=self.throw_banana)
        self.throw_button.pack(side="left")

        self.wind = random.uniform(-5, 5)
        self.wind_label = tk.Label(self.ui_frame, text=f"Wind: {self.wind:.1f}")
        self.wind_label.pack(side="left")

        self.status_label = tk.Label(self.ui_frame, text="Player 1's turn")
        self.status_label.pack(side="left")

        self.buildings = []
        self.gorillas = []
        self.current_player = 0

        self.setup_game()

    def setup_game(self):
        self.generate_city()
        self.place_gorillas()

    def generate_city(self):
        self.buildings.clear()
        self.canvas.delete("all")

        x = 0
        while x < WIDTH:
            w = random.randint(40, 70)
            h = random.randint(100, 300)
            rect = self.canvas.create_rectangle(x, HEIGHT - h, x + w, HEIGHT, fill="dimgray")
            self.buildings.append((x, x + w, HEIGHT - h))  # (x1, x2, top)
            x += w

        # Add the sun again for flavor
        self.canvas.create_oval(650, 50, 750, 150, fill="yellow", outline="orange", width=3)
        self.canvas.create_oval(675, 75, 685, 85, fill="black")
        self.canvas.create_oval(715, 75, 725, 85, fill="black")
        self.canvas.create_arc(675, 95, 725, 125, start=0, extent=-180, style=tk.ARC, width=2)

    def place_gorillas(self):
        self.gorillas.clear()
        left_building = self.buildings[2]
        right_building = self.buildings[-3]

        def draw_gorilla(xc, top):
            body = self.canvas.create_oval(xc - 10, top - 30, xc + 10, top - 10, fill="orange")
            arm = self.canvas.create_line(xc - 10, top - 20, xc + 10, top - 20, width=4)
            return (xc, top - 20, body, arm)

        x1 = (left_building[0] + left_building[1]) // 2
        y1 = left_building[2]
        self.gorillas.append(draw_gorilla(x1, y1))

        x2 = (right_building[0] + right_building[1]) // 2
        y2 = right_building[2]
        self.gorillas.append(draw_gorilla(x2, y2))

    def throw_banana(self):
        try:
            angle = float(self.angle_entry.get())
            velocity = float(self.vel_entry.get())
        except ValueError:
            self.status_label.config(text="Invalid angle or velocity!")
            return

        gx, gy, _, _ = self.gorillas[self.current_player]
        angle_rad = math.radians(angle)
        if self.current_player == 1:
            angle_rad = math.pi - angle_rad

        vx = velocity * math.cos(angle_rad) + self.wind
        vy = -velocity * math.sin(angle_rad)
        self.status_label.config(text=f"Player {self.current_player + 1} threw!")

        # Placeholder for banana animation
        self.canvas.create_oval(gx - 3, gy - 3, gx + 3, gy + 3, fill="yellow")

        self.current_player = 1 - self.current_player
        self.status_label.config(text=f"Player {self.current_player + 1}'s turn")


# Intro screen + game transition
class GorillasIntro:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.sun = self.canvas.create_oval(650, 50, 750, 150, fill="yellow", outline="orange", width=3)
        self.eye1 = self.canvas.create_oval(675, 75, 685, 85, fill="black")
        self.eye2 = self.canvas.create_oval(715, 75, 725, 85, fill="black")
        self.mouth = self.canvas.create_arc(675, 95, 725, 125, start=0, extent=-180, style=tk.ARC, width=2)

        self.canvas.create_text(WIDTH // 2, 100, text="GORILLAS.PY", font=("Courier", 36, "bold"), fill="darkred")
        self.canvas.create_text(WIDTH // 2, 150, text="A faithful remake of the QBasic classic", font=("Courier", 16), fill="black")
        self.canvas.create_text(WIDTH // 2, 180, text="Remake by ChatGPT", font=("Courier", 12), fill="gray")

        self.start_btn = tk.Button(root, text="Start Game", font=("Courier", 14), command=self.start_game)
        self.start_btn_window = self.canvas.create_window(WIDTH // 2, 250, window=self.start_btn)

        self.sun_angle = 0
        self.animate_sun()

    def animate_sun(self):
        self.sun_angle += 0.1
        offset = math.sin(self.sun_angle) * 3
        self.canvas.move(self.eye1, 0, offset)
        self.canvas.move(self.eye2, 0, offset)
        self.canvas.after(100, self.animate_sun)

    def start_game(self):
        self.start_btn.destroy()
        self.canvas.destroy()
        GorillasGame(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = GorillasIntro(root)
    root.mainloop()
