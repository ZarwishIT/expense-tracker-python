import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sqlite3

selected_expense_id = None

# Database Functions (Database setup + Get + Delete added)
def init_db():
    conn = sqlite3.connect("expenses.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_expense(title, amount, category, exp_date):
    conn = sqlite3.connect("expenses.db")
    conn.execute("INSERT INTO expenses (title,amount,category,date) VALUES (?,?,?,?)", (title, amount, category, exp_date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect("expenses.db")
    rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    return rows

def delete_expense(eid):
    conn = sqlite3.connect("expenses.db")
    conn.execute("DELETE FROM expenses WHERE id=?", (eid,))
    conn.commit()
    conn.close()

init_db()

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x700")
root.configure(bg="#f5f6fa")

# Header
header = tk.Frame(root, bg="#2c3e50", height=70)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="💰 Expense Tracker", font=("Arial", 22, "bold"), bg="#2c3e50", fg="white").pack(pady=18)

# Form Section
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

def handle_save():
    title = entry_title.get().strip()
    amount = entry_amount.get().strip()
    category = cat_var.get()
    exp_date = entry_date.get().strip()
    if not title or not amount: return
    save_expense(title, float(amount), category, exp_date)
    entry_title.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    load_table()

btn_save = tk.Button(form, text="💾 Save Expense", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", padx=20, pady=5, command=handle_save)
btn_save.grid(row=4, column=1, pady=10)

# Table Section
tbl = tk.LabelFrame(root, text=" 📋 All Expenses ", font=("Arial", 11, "bold"), bg="#f5f6fa", fg="#2c3e50")
tbl.pack(padx=25, pady=5, fill="both", expand=True)

cols = ("ID", "Title", "Amount (Rs)", "Category", "Date")
tree = ttk.Treeview(tbl, columns=cols, show="headings", height=7)

for col, w in zip(cols, [40, 200, 120, 130, 120]):
    tree.heading(col, text=col)
    tree.column(col, width=w, anchor="center")

sb = ttk.Scrollbar(tbl, orient="vertical", command=tree.yview)
tree.configure(yscroll=sb.set)
sb.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

def handle_delete():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a row first!")
        return
    eid = tree.item(selected[0])["values"][0]
    if messagebox.askyesno("Confirm", "Are you sure you want to delete?"):
        delete_expense(eid)
        load_table()

# Action Buttons
btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🗑️ Delete Selected", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", padx=18, pady=6, command=handle_delete).pack(side="left", padx=10)

def load_table():
    for row in tree.get_children(): tree.delete(row)
    for exp in get_expenses(): tree.insert("", tk.END, values=exp)

load_table()
root.mainloop()