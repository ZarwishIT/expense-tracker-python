import tkinter as tk
from tkinter import ttk
from datetime import date

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x700")
root.configure(bg="#f5f6fa")
root.resizable(False, False)

# Header
header = tk.Frame(root, bg="#2c3e50", height=70)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="💰 Expense Tracker", font=("Arial", 22, "bold"), bg="#2c3e50", fg="white").pack(pady=18)

# Form Section with Input Fields
form = tk.LabelFrame(root, text=" Add / Update Expense ", font=("Arial", 11, "bold"), bg="#f5f6fa", fg="#2c3e50", padx=15, pady=10)
form.pack(padx=25, pady=10, fill="x")

tk.Label(form, text="Title:", font=("Arial", 10), bg="#f5f6fa").grid(row=0, column=0, sticky="w", pady=5)
entry_title = tk.Entry(form, font=("Arial", 10), width=28)
entry_title.grid(row=0, column=1, padx=15, pady=5)

tk.Label(form, text="Amount (Rs):", font=("Arial", 10), bg="#f5f6fa").grid(row=1, column=0, sticky="w", pady=5)
entry_amount = tk.Entry(form, font=("Arial", 10), width=28)
entry_amount.grid(row=1, column=1, padx=15, pady=5)

tk.Label(form, text="Category:", font=("Arial", 10), bg="#f5f6fa").grid(row=2, column=0, sticky="w", pady=5)
cat_var = tk.StringVar(value="Food")
combo_cat = ttk.Combobox(form, textvariable=cat_var, width=25, values=["Food", "Transport", "Shopping", "Bills", "Health", "Other"])
combo_cat.grid(row=2, column=1, padx=15, pady=5)

tk.Label(form, text="Date:", font=("Arial", 10), bg="#f5f6fa").grid(row=3, column=0, sticky="w", pady=5)
entry_date = tk.Entry(form, font=("Arial", 10), width=28)
entry_date.insert(0, str(date.today()))
entry_date.grid(row=3, column=1, padx=15, pady=5)

# Save Button
btn_save = tk.Button(form, text="💾 Save Expense", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", padx=20, pady=5, cursor="hand2")
btn_save.grid(row=4, column=1, pady=10)

root.mainloop()