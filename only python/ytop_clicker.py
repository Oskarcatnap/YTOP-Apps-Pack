import tkinter as tk
from tkinter import messagebox

class YtopClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("YTOP Clicker - You Try Open Popcorn")
        self.root.geometry("400x500")
        self.root.configure(bg="#1a1a1a") # Темный хайтек фон
        
        self.popcorn_count = 0
        self.click_power = 1
        
        # Заголовок
        self.label_title = tk.Label(root, text="YTOP CLICKER", font=("Arial", 24, "bold"), fg="#FFD700", bg="#1a1a1a")
        self.label_title.pack(pady=20)
        
        # Счетчик
        self.label_count = tk.Label(root, text="Popcorn: 0", font=("Arial", 18), fg="white", bg="#1a1a1a")
        self.label_count.pack(pady=10)
        
        # Кнопка-Попкорн (Основная механика)
        self.popcorn_btn = tk.Button(
            root, 
            text="🍿", 
            font=("Arial", 60), 
            command=self.click,
            bg="#333", 
            activebackground="#444", 
            fg="white",
            relief="flat",
            bd=0
        )
        self.popcorn_btn.pack(pady=30)
        
        # Кнопка магазина
        self.upgrade_btn = tk.Button(
            root, 
            text="Upgrade (Cost: 10)", 
            command=self.upgrade,
            bg="#FFD700", 
            fg="black",
            font=("Arial", 12, "bold")
        )
        self.upgrade_btn.pack(pady=20)

    def click(self):
        self.popcorn_count += self.click_power
        self.update_ui()

    def upgrade(self):
        cost = 10 * self.click_power
        if self.popcorn_count >= cost:
            self.popcorn_count -= cost
            self.click_power += 1
            self.upgrade_btn.config(text=f"Upgrade (Cost: {10 * self.click_power})")
            self.update_ui()
        else:
            messagebox.showwarning("YTOP System", "Not enough popcorn to open a new pack!")

    def update_ui(self):
        self.label_count.config(text=f"Popcorn: {self.popcorn_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YtopClicker(root)
    root.mainloop()