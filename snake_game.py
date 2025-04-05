import tkinter as tk
import random

CELL_SIZE = 20
GRID_SIZE = 30
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        # Center the main window
        window_width = WIDTH
        window_height = HEIGHT + 60
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.high_score = 0
        self.paused = False
        self.loop_id = None

        # Menu frame
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Snake Game", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.menu_frame, text="Choose Speed (1 slow - 20 fast)").pack()

        self.speed_slider = tk.Scale(
            self.menu_frame, from_=1, to=20, orient=tk.HORIZONTAL, length=250
        )
        self.speed_slider.set(10)
        self.speed_slider.pack(pady=5)

        tk.Button(self.menu_frame, text="Start Game", command=self.start_game).pack(pady=10)
        tk.Button(self.menu_frame, text="Exit", command=root.quit).pack(pady=5)

        # Top UI frame
        self.top_frame = tk.Frame(root)
        self.score_label = tk.Label(
            self.top_frame, text="Score: 0    High Score: 0", font=("Arial", 14)
        )
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.settings_button = tk.Button(
            self.top_frame, text="Settings", command=self.open_settings
        )
        self.settings_button.pack(side=tk.RIGHT, padx=10)

        # Canvas for game
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")

    def start_game(self):
        self.menu_frame.pack_forget()
        self.top_frame.pack(fill=tk.X)
        self.canvas.pack()
        self.reset_game()
        self.game_loop()

    def reset_game(self):
        if self.loop_id is not None:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None

        self.canvas.delete("all")
        self.speed = 220 - (self.speed_slider.get() * 10)
        self.direction = "stop"
        self.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.snake_ids = []
        self.food = None
        self.score = 0
        self.paused = False
        self.food_eaten = 0

        # Special food variables
        self.special_food = None
        self.special_food_pos = None
        self.special_timer = 0
        self.special_bar = None

        self.update_score_label()

        self.draw_snake()
        self.spawn_food()

        self.root.bind("<w>", lambda e: self.set_direction("up"))
        self.root.bind("<s>", lambda e: self.set_direction("down"))
        self.root.bind("<a>", lambda e: self.set_direction("left"))
        self.root.bind("<d>", lambda e: self.set_direction("right"))
        self.root.bind("<p>", lambda e: self.toggle_pause())
        self.root.bind("<r>", lambda e: self.restart_game())
        self.root.bind("<Escape>", lambda e: self.root.quit())

    def update_score_label(self):
        self.score_label.config(
            text=f"Score: {self.score}    High Score: {self.high_score}"
        )

    def draw_snake(self):
        for seg in self.snake_ids:
            self.canvas.delete(seg)
        self.snake_ids = []
        for idx, (x, y) in enumerate(self.snake):
            color = "white" if idx == 0 else "#cccccc"
            seg_id = self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
            )
            self.snake_ids.append(seg_id)

    def spawn_food(self):
        while True:
            fx = random.randint(0, GRID_SIZE - 1)
            fy = random.randint(0, GRID_SIZE - 1)
            if (fx, fy) not in self.snake:
                break
        if self.food:
            self.canvas.delete(self.food)
        self.food_pos = (fx, fy)
        self.food = self.canvas.create_oval(
            fx * CELL_SIZE,
            fy * CELL_SIZE,
            (fx + 1) * CELL_SIZE,
            (fy + 1) * CELL_SIZE,
            fill="red",
        )

    def spawn_special_food(self):
        while True:
            fx = random.randint(0, GRID_SIZE - 2)
            fy = random.randint(0, GRID_SIZE - 2)
            if (fx, fy) not in self.snake:
                break
        # Remove old special food if exists
        if self.special_food:
            self.canvas.delete(self.special_food)
        # Remove old timer bar
        if self.special_bar:
            self.canvas.delete(self.special_bar)

        self.special_food_pos = (fx, fy)
        # Draw larger special food (2x2 cells)
        self.special_food = self.canvas.create_oval(
            fx * CELL_SIZE,
            fy * CELL_SIZE,
            (fx + 2) * CELL_SIZE,
            (fy + 2) * CELL_SIZE,
            fill="orange red",
        )
        self.special_timer = 50  # 50 * game loop delay ~5 seconds
        self.update_special_bar()

    def update_special_bar(self):
        if self.special_bar:
            self.canvas.delete(self.special_bar)
        bar_width = int((self.special_timer / 50) * WIDTH)
        self.special_bar = self.canvas.create_rectangle(
            0, 0, bar_width, 10, fill="orange red"
        )

    def set_direction(self, dir):
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if self.direction == "stop" or dir != opposites.get(self.direction):
            self.direction = dir

    def toggle_pause(self):
        self.paused = not self.paused

    def restart_game(self):
        if self.loop_id is not None:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None
        self.canvas.pack_forget()
        self.top_frame.pack_forget()
        self.menu_frame.pack()

    def open_settings(self):
        self.paused = True
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")

        # Center the settings window
        settings_win.update_idletasks()
        w, h = 200, 200
        sw = settings_win.winfo_screenwidth()
        sh = settings_win.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        settings_win.geometry(f"{w}x{h}+{x}+{y}")

        settings_win.transient(self.root)
        settings_win.grab_set()

        def continue_game():
            self.paused = False
            settings_win.destroy()

        def restart():
            settings_win.destroy()
            self.restart_game()

        def exit_game():
            self.root.quit()

        tk.Button(settings_win, text="Continue", width=15, command=continue_game).pack(pady=10)
        tk.Button(settings_win, text="Restart", width=15, command=restart).pack(pady=10)
        tk.Button(settings_win, text="Exit", width=15, command=exit_game).pack(pady=10)

    def show_game_over(self):
        over_win = tk.Toplevel(self.root)
        over_win.title("Game Over")

        over_win.update_idletasks()
        w, h = 250, 200
        sw = over_win.winfo_screenwidth()
        sh = over_win.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        over_win.geometry(f"{w}x{h}+{x}+{y}")

        over_win.transient(self.root)
        over_win.grab_set()

        tk.Label(over_win, text="Game Over!", font=("Arial", 16)).pack(pady=10)
        tk.Label(
            over_win,
            text=f"Your Score: {self.score}\nHigh Score: {self.high_score}",
            font=("Arial", 12),
        ).pack(pady=10)

        def play_again():
            over_win.destroy()
            self.restart_game()

        def exit_game():
            self.root.quit()

        tk.Button(over_win, text="Play Again", width=15, command=play_again).pack(pady=5)
        tk.Button(over_win, text="Exit", width=15, command=exit_game).pack(pady=5)

    def game_loop(self):
        if not self.paused and self.direction != "stop":
            head_x, head_y = self.snake[0]
            if self.direction == "up":
                head_y -= 1
            elif self.direction == "down":
                head_y += 1
            elif self.direction == "left":
                head_x -= 1
            elif self.direction == "right":
                head_x += 1

            head_x %= GRID_SIZE
            head_y %= GRID_SIZE

            new_head = (head_x, head_y)

            # Check collision with self
            if new_head in self.snake:
                if self.score > self.high_score:
                    self.high_score = self.score
                if self.loop_id is not None:
                    self.root.after_cancel(self.loop_id)
                    self.loop_id = None
                self.show_game_over()
                return

            self.snake = [new_head] + self.snake

            # Check normal food
            if new_head == self.food_pos:
                self.score += 10
                self.food_eaten += 1
                self.update_score_label()
                self.spawn_food()

                # After every 5 foods, spawn special food
                if self.food_eaten % 5 == 0:
                    self.spawn_special_food()
            # Check special food
            elif (
                self.special_food_pos
                and self.special_food_pos[0] <= new_head[0] <= self.special_food_pos[0] + 1
                and self.special_food_pos[1] <= new_head[1] <= self.special_food_pos[1] + 1
            ):
                self.score += 100
                self.update_score_label()
                # Remove special food and bar
                if self.special_food:
                    self.canvas.delete(self.special_food)
                    self.special_food = None
                if self.special_bar:
                    self.canvas.delete(self.special_bar)
                    self.special_bar = None
                self.special_food_pos = None
            else:
                self.snake.pop()

            self.draw_snake()

            # Update special food timer
            if self.special_food:
                self.special_timer -= 1
                if self.special_timer <= 0:
                    # Time's up, remove special food and bar
                    self.canvas.delete(self.special_food)
                    self.special_food = None
                    self.special_food_pos = None
                    if self.special_bar:
                        self.canvas.delete(self.special_bar)
                        self.special_bar = None
                else:
                    self.update_special_bar()

        self.loop_id = self.root.after(self.speed, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
