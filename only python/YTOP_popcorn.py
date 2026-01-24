import tkinter as tk
import random

class YtopSnapFixed:
    def __init__(self, root):
        self.root = root
        self.root.title("YTOP Popcorn - v1.0")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=600, bg="#0a0a0c", highlightthickness=0)
        self.canvas.pack()

        # Свет
        self.canvas.create_polygon(0, 150, 300, 600, 0, 600, fill="#121225")
        self.canvas.create_rectangle(0, 80, 15, 220, fill="#5dade2", outline="")

        # Физика
        self.bx, self.by = 400.0, 500.0
        self.b_vx, self.b_vy = 0.0, 0.0
        self.is_grabbed = False
        self.lid_state = 0 # 0-закрыто, 1-щель, 2-отлетела
        self.lx, self.ly = 400.0, 445.0
        self.l_vx, self.l_vy = 0.0, 0.0

        self.last_y = 500.0
        self.active_popcorns = []

        # Графика
        self.shadow = self.canvas.create_oval(0, 0, 0, 0, fill="#050505", outline="")
        self.inner = self.canvas.create_polygon(0,0,0,0, fill="#8e1e14", state='hidden')
        self.bucket = self.canvas.create_polygon(0,0,0,0, fill="#e74c3c", outline="#c0392b", width=2)
        self.highlight = self.canvas.create_polygon(0,0,0,0, fill="#ff5e4d", outline="")
        self.label = self.canvas.create_text(0, 0, text="YTOP", fill="white", font=("Verdana", 12, "bold"))
        self.lid = self.canvas.create_rectangle(0, 0, 0, 0, fill="#c0392b", outline="#ffffff", width=2)

        self.canvas.bind("<ButtonPress-1>", self.on_grab)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<space>", self.open_gap)
        
        self.physics_loop()

    def open_gap(self, _):
        if self.lid_state == 0:
            self.lid_state = 1
            self.canvas.itemconfig(self.inner, state='normal')

    def on_grab(self, event):
        if abs(event.x - self.bx) < 60 and abs(event.y - self.by) < 60:
            self.is_grabbed = True
            self.last_y = event.y

    def on_release(self, event):
        if self.is_grabbed:
            self.is_grabbed = False
            # b_vy здесь уже рассчитана в on_drag

    def on_drag(self, event):
        if self.is_grabbed:
            nx, ny = max(50, min(750, event.x)), max(50, min(550, event.y))
            
            # РАССЧЕТ СКОРОСТИ РЫВКА
            self.b_vx = (nx - self.bx)
            self.b_vy = (ny - self.last_y)
            
            # ФИКС: Если крышка приоткрыта и мы РЕЗКО дернули вверх
            # Чем меньше число (например -10), тем легче сорвать
            if self.lid_state == 1 and self.b_vy < -10:
                self.lid_state = 2
                self.l_vx = self.b_vx * 0.5
                self.l_vy = self.b_vy - 5
                self.lx, self.ly = self.bx, self.by - 65

            # Обычный вылет попкорна
            if self.lid_state > 0 and (abs(self.b_vx) > 15 or abs(self.b_vy) > 15):
                chance = 0.1 if self.lid_state == 1 else 0.4
                if random.random() < chance:
                    self.spawn_popcorn(self.b_vx, self.b_vy)

            self.bx, self.by = nx, ny
            self.last_y = ny
            self.update_graphics()

    def spawn_popcorn(self, vx, vy):
        parts = []
        mx, my = self.bx + random.uniform(-10, 10), self.by - 55
        for _ in range(random.randint(3, 4)):
            pid = self.canvas.create_oval(0,0,0,0, fill="#ffffff", outline="#d4ac0d")
            parts.append({'id': pid, 'ox': random.uniform(-6, 6), 'oy': random.uniform(-6, 6), 'r': random.randint(6, 10)})
        self.active_popcorns.append({"parts": parts, "x": mx, "y": my, "vx": vx*0.3 + random.uniform(-2, 2), "vy": vy*0.3 + random.uniform(-5, -2)})

    def physics_loop(self):
        # Если не держим — ведро падает само
        if not self.is_grabbed:
            self.b_vy += 0.8
            self.bx += self.b_vx * 0.5
            self.by += self.b_vy
            
            if self.by > 500:
                self.by = 500
                self.b_vy *= -0.4
                self.b_vx *= 0.8
            if self.bx < 50 or self.bx > 750: self.b_vx *= -0.6

        # Физика летящей крышки
        if self.lid_state == 2:
            self.l_vy += 0.7
            self.lx += self.l_vx
            self.ly += self.l_vy
            if self.ly > 540:
                self.ly = 540
                self.l_vy *= -0.3
                self.l_vx *= 0.7
        elif self.lid_state == 1:
            self.lx, self.ly = self.bx, self.by - 65
        else:
            self.lx, self.ly = self.bx, self.by - 52

        # Попкорн
        to_del = []
        for p in self.active_popcorns:
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.6
            for pt in p["parts"]:
                x, y, r = p["x"] + pt['ox'], p["y"] + pt['oy'], pt['r']
                self.canvas.coords(pt["id"], x-r, y-r, x+r, y+r)
            if p["y"] > 620:
                for pt in p["parts"]: self.canvas.delete(pt["id"])
                to_del.append(p)
        for p in to_del: self.active_popcorns.remove(p)

        self.update_graphics()
        self.root.after(16, self.physics_loop)

    def update_graphics(self):
        self.canvas.coords(self.shadow, self.bx-45, 545, self.bx+45, 555)
        self.canvas.coords(self.bucket, self.bx-50, self.by-50, self.bx+50, self.by-50, self.bx+35, self.by+50, self.bx-35, self.by+50)
        self.canvas.coords(self.inner, self.bx-50, self.by-50, self.bx+50, self.by-50, self.bx+40, self.by-42, self.bx-40, self.by-42)
        self.canvas.coords(self.highlight, self.bx-45, self.by-50, self.bx-25, self.by-50, self.bx-15, self.by+50, self.bx-30, self.by+50)
        self.canvas.coords(self.label, self.bx, self.by)
        self.canvas.coords(self.lid, self.lx-55, self.ly-8, self.lx+55, self.ly+8)

root = tk.Tk()
YtopSnapFixed(root)
root.mainloop()