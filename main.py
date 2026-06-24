import tkinter as tk

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x600")
root.configure(bg="#f5f6fa")
root.resizable(False, False)

# Header
header = tk.Frame(root, bg="#2c3e50", height=70)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="💰 Expense Tracker",
         font=("Arial", 22, "bold"),
         bg="#2c3e50", fg="white").pack(pady=18)

root.mainloop()