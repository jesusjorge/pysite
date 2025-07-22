import tkinter as tk
import math
import random

WIDTH = 800
HEIGHT = 600
GRAVITY = 9.8

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
        , fill="gray")

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
        self.banana = None
        self.exploding = False

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
            self.canvas.create_rectangle(x, HEIGHT - h, x + w, HEIGHT, fill="dimgray")
            self.buildings.append((x, x + w, HEIGHT - h))
            x += w

        self.canvas.create_oval(650, 50, 750, 150, fill="yellow", outline="orange", width=3)
        self.canvas.create_oval(675, 75, 685, 85, fill="black")
        self.canvas.create_oval(715, 75, 725, 85, fill="black")
        self.canvas.create_arc(675, 95, 725, 125, start=0, extent=-180, style=tk.ARC, width=2)

    def place_gorillas(self):
        self.gorillas.clear()
        b1 = self.buildings[2]
        b2 = self.buildings[-3]

        def draw_gorilla(xc, top):
            # Draw more realistic gorilla: head, body, legs, and arms
            body = self.canvas.create_oval(xc - 12, top - 40, xc + 12, top - 10, fill="saddlebrown", outline="black")
            head = self.canvas.create_oval(xc - 8, top - 55, xc + 8, top - 40, fill="chocolate", outline="black")
            left_leg = self.canvas.create_line(xc - 8, top - 10, xc - 8, top + 10, width=4, fill="black")
            right_leg = self.canvas.create_line(xc + 8, top - 10, xc + 8, top + 10, width=4, fill="black")
            left_arm = self.canvas.create_line(xc - 12, top - 30, xc - 25, top - 45, width=4, fill="black")
            right_arm = self.canvas.create_line(xc + 12, top - 30, xc + 25, top - 45, width=4, fill="black")
            return (xc, top - 40, body, head)

        x1 = (b1[0] + b1[1]) // 2
        y1 = b1[2]
        self.gorillas.append(draw_gorilla(x1, y1))

        x2 = (b2[0] + b2[1]) // 2
        y2 = b2[2]
        self.gorillas.append(draw_gorilla(x2, y2))

    def throw_banana(self):
        if self.exploding:
            return
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

        self.t = 0
        self.banana_start = (gx + (15 if self.current_player == 0 else -15), gy)
        self.vx = vx
        self.vy = vy
        self.animate_banana()

    def animate_banana(self):
        t = self.t
        x0, y0 = self.banana_start
        x = x0 + self.vx * t
        y = y0 + self.vy * t + 0.5 * GRAVITY * t ** 2
        self.t += 0.2

        if self.banana:
            self.canvas.delete(self.banana)

        if x < 0 or x > WIDTH or y > HEIGHT:
            self.next_turn("Missed!")
            return

        self.banana = self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="yellow")

        if int(self.t * 10) % 3 == 0:
            self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black")

        if self.check_building_collision(x, y):
            self.explode(x, y, win=False)
            return

        if self.check_gorilla_hit(x, y):
            self.explode(x, y, win=True)
            return

        self.root.after(30, self.animate_banana)

    def check_building_collision(self, x, y):
        for x1, x2, top in self.buildings:
            if x1 <= x <= x2 and y >= top:
                return True
        return False

    def check_gorilla_hit(self, x, y):
        gx, gy, *_ = self.gorillas[1 - self.current_player]
        return abs(x - gx) < 15 and abs(y - gy) < 15

    def explode(self, x, y, win):
        self.exploding = True
        self.explosion_radius = 1

        def animate_explosion():
            if self.explosion_radius > 30:
                if win:
                    self.status_label.config(text=f"Player {self.current_player + 1} WINS!")
                    self.throw_button.config(state="disabled")
                    self.show_restart_button()
                else:
                    self.next_turn("BOOM! Missed.")
                return
            r = self.explosion_radius
            self.canvas.create_oval(x - r, y - r, x + r, y + r, outline="red", width=2)
            self.explosion_radius += 3
            self.root.after(50, animate_explosion)

        animate_explosion()

    def show_restart_button(self):
        self.restart_button = tk.Button(self.ui_frame, text="Play Again", command=self.restart_game)
        self.restart_button.pack(side="left")

    def restart_game(self):
        self.canvas.delete("all")
        self.buildings.clear()
        self.gorillas.clear()
        self.exploding = False
        self.current_player = 0
        self.status_label.config(text="Player 1's turn")
        self.throw_button.config(state="normal")
        self.wind = random.uniform(-5, 5)
        self.wind_label.config(text=f"Wind: {self.wind:.1f}")
        self.restart_button.destroy()
        self.setup_game()

    def next_turn(self, msg):
        self.exploding = False
        self.current_player = 1 - self.current_player
        self.status_label.config(text=f"{msg} Player {self.current_player + 1}'s turn")
        self.wind = random.uniform(-5, 5)
        self.wind_label.config(text=f"Wind: {self.wind:.1f}")

        if self.current_player == 1:
            self.root.after(1000, self.ai_turn)

    def ai_turn(self):
        target_x, target_y, *_ = self.gorillas[0]
        origin_x, origin_y, *_ = self.gorillas[1]

        best_angle = 45
        best_velocity = 50
        min_error = float('inf')

        for angle in range(20, 80, 5):
            for velocity in range(30, 90, 5):
                angle_rad = math.radians(180 - angle)
                vx = velocity * math.cos(angle_rad) + self.wind
                vy = -velocity * math.sin(angle_rad)

                t = 0
                x, y = origin_x, origin_y
                while 0 <= x <= WIDTH and y <= HEIGHT:
                    x = origin_x + vx * t
                    y = origin_y + vy * t + 0.5 * GRAVITY * t**2
                    if y > HEIGHT: break
                    t += 0.2
                error = abs(x - target_x)
                if error < min_error:
                    min_error = error
                    best_angle = angle
                    best_velocity = velocity
                if error < 10:
                    break

        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, str(best_angle))
        self.vel_entry.delete(0, tk.END)
        self.vel_entry.insert(0, str(best_velocity))
        self.throw_banana()

if __name__ == "__main__":
    root = tk.Tk()
    GorillasIntro(root)
    root.mainloop()
