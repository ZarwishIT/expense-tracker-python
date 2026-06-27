import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sqlite3

selected_expense_id = None

# Database Functions
def init_db():
    conn = sqlite3.connect("expenses.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL)''')
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

def update_expense_db(eid, title, amount, category, exp_date):
    conn = sqlite3.connect("expenses.db")
    conn.execute("UPDATE expenses SET title=?, amount=?, category=?, date=? WHERE id=?", (title, amount, category, exp_date, eid))
    conn.commit()
    conn.close()

def delete_expense(eid):
    conn = sqlite3.connect("expenses.db")
    conn.execute("DELETE FROM expenses WHERE id=?", (eid,))
    conn.commit()
    conn.close()

def get_total():
    conn = sqlite3.connect("expenses.db")
    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
    conn.close()
    return total or 0

def get_category_totals():
    conn = sqlite3.connect("expenses.db")
    rows = conn.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category").fetchall()
    conn.close()
    return rows

init_db()

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
    global selected_expense_id
    title = entry_title.get().strip()
    amount = entry_amount.get().strip()
    category = cat_var.get()
    exp_date = entry_date.get().strip()
    
    if not title or not amount:
        messagebox.showwarning("Error", "Please fill Title and Amount!")
        return
    try:
        float(amount)
    except ValueError:
        messagebox.showwarning("Error", "Amount must be a number!")
        return
        
    if selected_expense_id is None:
        save_expense(title, float(amount), category, exp_date)
    else:
        update_expense_db(selected_expense_id, title, float(amount), category, exp_date)
        selected_expense_id = None
        btn_save.config(text="💾 Save Expense", bg="#27ae60")
        
    entry_title.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_date.insert(0, str(date.today()))
    load_table()

btn_save = tk.Button(form, text="💾 Save Expense", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", padx=20, pady=5, cursor="hand2", command=handle_save)
btn_save.grid(row=4, column=1, pady=10)

# Table Section
tbl = tk.LabelFrame(root, text=" 📋 All Expenses ", font=("Arial", 11, "bold"), bg="#f5f6fa", fg="#2c3e50")
tbl.pack(padx=25, pady=5, fill="both", expand=True)

cols = ("ID", "Title", "Amount (Rs)", "Category", "Date")
tree = ttk.Treeview(tbl, columns=cols, show="headings", height=7)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", font=("Arial", 10), rowheight=26)

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

def handle_edit_select(event):
    global selected_expense_id
    selected = tree.selection()
    if not selected: return
    values = tree.item(selected[0])["values"]
    
    selected_expense_id = values[0]
    entry_title.delete(0, tk.END)
    entry_title.insert(0, values[1])
    entry_amount.delete(0, tk.END)
    entry_amount.insert(0, values[2])
    cat_var.set(values[3])
    entry_date.delete(0, tk.END)
    entry_date.insert(0, values[4])
    btn_save.config(text="🔄 Update Expense", bg="#2980b9")

tree.bind("<Double-1>", handle_edit_select)

# Action Buttons Frame
btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🗑️ Delete Selected", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", padx=18, pady=6, cursor="hand2", command=handle_delete).pack(side="left", padx=10)

# Summary Section
summary_frame = tk.Frame(root, bg="#2c3e50", pady=8)
summary_frame.pack(fill="x", padx=25, pady=10)

total_label = tk.Label(summary_frame, text="Total Spent: Rs 0", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#2ecc71")
total_label.pack()

cat_label = tk.Label(summary_frame, text="", font=("Arial", 9), bg="#2c3e50", fg="#bdc3c7")
cat_label.pack()

def update_summary():
    total = get_total()
    total_label.config(text=f"Total Spent: Rs {total:,.0f}")
    cats = get_category_totals()
    if cats:
        cat_text = "   |   ".join([f"{c}: Rs {a:,.0f}" for c, a in cats])
    else:
        cat_text = "No expenses yet"
    cat_label.config(text=cat_text)

def load_table():
    for row in tree.get_children(): tree.delete(row)
    for exp in get_expenses(): tree.insert("", tk.END, values=exp)
    update_summary()

load_table()
root.mainloop()