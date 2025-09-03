import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILENAME = "expenses.txt"
BUDGET_FILE = "budget.txt"

# ------------------- UTILS -------------------
def format_amount(amount):
    return f"{float(amount):.2f}"

# ------------------- CLASSES -------------------
class Expense:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.description = description

    def __str__(self):
        return f"{self.date},{self.category},{format_amount(self.amount)},{self.description}"

# ------------------- VALIDATION -------------------
def validate_date(date_str):
    if not date_str.strip():
        return False, "Date cannot be empty"
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_obj > datetime.date.today():
            return False, "Date cannot be in the future"
        return True, date_str
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"

def validate_category(category_str):
    if not category_str.strip():
        return False, "Category cannot be empty"
    return True, category_str

def validate_amount(amount_str):
    if not amount_str.strip():
        return False, "Amount cannot be empty"
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be greater than 0"
        return True, amount
    except ValueError:
        return False, "Amount must be a number"

def validate_description(desc_str):
    if not desc_str.strip():
        return False, "Description cannot be empty"
    return True, desc_str

# ------------------- DATA -------------------
expenses = []
budget = 0

def load_expenses():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    expenses.append(Expense(parts[0], parts[1], float(parts[2]), parts[3]))

def save_expenses():
    with open(FILENAME, "w", encoding="utf-8") as file:
        for exp in expenses:
            file.write(str(exp) + "\n")

# ------------------- GUI PAGES -------------------
def gui_add_expense():
    def save_entry():
        date_error.config(text="")
        category_error.config(text="")
        amount_error.config(text="")
        desc_error.config(text="")

        has_error = False

        valid, result = validate_date(date_entry.get())
        if not valid:
            date_error.config(text=result)
            has_error = True
        else:
            date = result

        category_value = category_combo.get()
        valid, result = validate_category(category_value)
        if not valid:
            category_error.config(text=result)
            has_error = True
        else:
            category = result

        valid, result = validate_amount(amount_entry.get())
        if not valid:
            amount_error.config(text=result)
            has_error = True
        else:
            amount = result

        valid, result = validate_description(desc_entry.get())
        if not valid:
            desc_error.config(text=result)
            has_error = True
        else:
            description = result

        if has_error:
            return

        exp = Expense(date, category, amount, description)
        expenses.append(exp)
        save_expenses()
        messagebox.showinfo("Success", "Expense added!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("➕Add Expense")
    add_window.configure(bg="lightgrey")
    add_window.geometry("700x600")

    tk.Label(add_window, text="➕Add Expenses", fg="orange",bg="lightgrey",font=("Arial", 22, "bold", "underline")).pack(pady=20)

    frame = tk.Frame(add_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    font_big = ("Arial", 14)

    tk.Label(frame, text="Date (YYYY-MM-DD):", font=font_big).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    date_entry = tk.Entry(frame, font=font_big)
    date_entry.grid(row=0, column=1, pady=5)
    date_error = tk.Label(frame, text="", fg="red", font=("Arial", 12))
    date_error.grid(row=1, columnspan=2)

    tk.Label(frame, text="Category:", font=font_big).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    category_combo = ttk.Combobox(frame, values=["Rent & Bills", "Food & Drinks", "Transport", "Entertainment"], font=font_big)
    category_combo.grid(row=2, column=1, pady=5)
    category_error = tk.Label(frame, text="", fg="red", font=("Arial", 12))
    category_error.grid(row=3, columnspan=2)

    tk.Label(frame, text="Amount:", font=font_big).grid(row=4, column=0, sticky="e", pady=5, padx=5)
    amount_entry = tk.Entry(frame, font=font_big)
    amount_entry.grid(row=4, column=1, pady=5)
    amount_error = tk.Label(frame, text="", fg="red", font=("Arial", 12))
    amount_error.grid(row=5, columnspan=2)

    tk.Label(frame, text="Description:", font=font_big).grid(row=6, column=0, sticky="e", pady=5, padx=5)
    desc_entry = tk.Entry(frame, font=font_big)
    desc_entry.grid(row=6, column=1, pady=5)
    desc_error = tk.Label(frame, text="", fg="red", font=("Arial", 12))
    desc_error.grid(row=7, columnspan=2)

    tk.Button(frame, text="Save", command=save_entry, bg="lightgreen",fg="white", font=font_big, width=15, height=2).grid(row=8, columnspan=2, pady=20)

def gui_show_expenses():
    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No expense selected.")
            return
        idxs = [tree.index(item) for item in selected]
        for item in selected:
            tree.delete(item)
        for idx in sorted(idxs, reverse=True):
            del expenses[idx]
        save_expenses()
        messagebox.showinfo("Success", "Selected expense(s) deleted.")

    def delete_all():
        if not expenses:
            messagebox.showwarning("Warning", "No expenses to delete.")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete ALL expenses?"):
            expenses.clear()
            for item in tree.get_children():
                tree.delete(item)
            save_expenses()
            messagebox.showinfo("Success", "All expenses deleted.")

    def sort_by_date():
        nonlocal sort_desc
        # Sort expenses and treeview
        sorted_expenses = sorted(
            enumerate(expenses),
            key=lambda x: datetime.datetime.strptime(x[1].date, "%Y-%m-%d"),
            reverse=sort_desc
        )
        # Rearrange expenses list
        new_expenses = [expenses[i] for i, _ in sorted_expenses]
        expenses.clear()
        expenses.extend(new_expenses)
        # Clear and re-insert treeview
        for item in tree.get_children():
            tree.delete(item)
        for exp in expenses:
            tree.insert("", "end", values=(exp.date, exp.category, format_amount(exp.amount), exp.description))
        # Toggle sort order
        sort_desc = not sort_desc
        # Update arrow
        arrow = "↓" if sort_desc else "↑"
        tree.heading("Date", text=f"Date {arrow}", command=sort_by_date)

    win = tk.Toplevel(root)
    win.title("Expenses")
    win.geometry("900x600")
    win.configure(bg="lightgrey")
    

    tk.Label(win, text="📋Show Expenses", fg="dark orange",bg="lightgrey",font=("Arial", 22, "bold", "underline")).pack(pady=20)

    frame = tk.Frame(win)
    frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(frame, columns=("Date", "Category", "Amount", "Description"), show="headings")
    sort_desc = True  # Start with latest date first

    tree.heading("Date", text="Date ↓", command=sort_by_date)
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.heading("Description", text="Description")

    tree.column("Date", anchor="center")
    tree.column("Category", anchor="center")
    tree.column("Amount", anchor="center")
    tree.column("Description", anchor="center")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(expand=True, fill="both")

    # Insert expenses sorted by latest date first
    for exp in sorted(expenses, key=lambda e: datetime.datetime.strptime(e.date, "%Y-%m-%d"), reverse=True):
        tree.insert("", "end", values=(exp.date, exp.category, format_amount(exp.amount), exp.description))

    tk.Button(win, text="Delete Selected", command=delete_selected, bg="red", fg="white", font=("Arial", 14), width=20).pack(pady=10)
    tk.Button(win, text="Delete All", command=delete_all, bg="red", fg="white", font=("Arial", 14), width=20).pack(pady=10)



def load_budget():
    global budget
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r", encoding="utf-8") as f:
                budget = float(f.read().strip())
        except Exception:
            budget = 0

def save_budget_to_file():
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        f.write(str(budget))

def gui_set_budget():
    def save_budget():
        try:
            value = float(budget_entry.get())
            if value <= 0:
                raise ValueError
            global budget
            budget = value
            save_budget_to_file()
            messagebox.showinfo("Success", f"Budget set to RM {format_amount(budget)}")
            budget_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number")

    budget_window = tk.Toplevel(root)
    budget_window.title("Set Budget")
    budget_window.geometry("500x400")
    budget_window.configure(bg="lightgrey")

    tk.Label(budget_window, text="🎯Set Budget",fg="dark orange",bg="lightgrey", font=("Arial", 22, "bold", "underline")).pack(pady=20)

    frame = tk.Frame(budget_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    font_big = ("Arial", 14)
    tk.Label(frame, text="Enter monthly budget: RM", font=font_big).pack(pady=10)
    preset_amounts = ["100", "200", "500", "1000", "2000"]
    budget_entry = ttk.Combobox(frame, values=preset_amounts, font=font_big, width=23)
    budget_entry.pack(pady=10)

    tk.Button(frame, text="Save", command=save_budget, font=font_big, width=15, height=2, bg="lightgreen").pack(pady=10)

def gui_check_budget():
    total_spent = sum(exp.amount for exp in expenses)
    win = tk.Toplevel(root)
    win.title("Check Budget")
    win.geometry("500x400")
    win.configure(bg="lightgrey")

    tk.Label(win, text="🔍Check Budget", fg="dark orange",bg="lightgrey",font=("Arial", 22, "bold", "underline")).pack(pady=20)

    font_big = ("Arial", 14)
    tk.Label(win, text=f"Budget: RM {format_amount(budget)}",bg="lightgrey", font=font_big).pack(pady=10)
    tk.Label(win, text=f"Total Spent: RM {format_amount(total_spent)}",bg="lightgrey", font=font_big).pack(pady=10)

    if budget > 0:
        if total_spent > budget:
            tk.Label(win, text="⚠ You have exceeded your budget!", fg="red",bg="lightgrey", font=font_big).pack(pady=10)
        else:
            tk.Label(win, text="✅ You are within your budget.", fg="green",bg="lightgrey", font=font_big).pack(pady=10)
    else:
        tk.Label(win, text="No budget set yet.", fg="blue", font=font_big).pack(pady=10)



def gui_analysis():
    analysis_window = tk.Toplevel(root)
    analysis_window.title("📊Expenses Analysis")
    analysis_window.configure(bg="lightgrey")
    analysis_window.geometry("700x600")

    tk.Label(analysis_window, text="📊Expense Analysis", fg="orange",bg="lightgrey", font=("Arial", 22, "bold", "underline")).pack(pady=20)

    font_big = ("Arial", 14)
    total_spent = sum(exp.amount for exp in expenses)

    tk.Label(analysis_window, text=f"Total Spent: RM {format_amount(total_spent)}",bg="lightgrey", font=font_big).pack(pady=10)
    if budget > 0:
        tk.Label(analysis_window, text=f"Budget: RM {format_amount(budget)}",bg="lightgrey", font=font_big).pack(pady=10)
        if total_spent > budget:
            tk.Label(analysis_window, text="You have exceeded your budget!", fg="red",bg="lightgrey", font=font_big).pack()
        else:
            tk.Label(analysis_window, text="You are within your budget.", fg="green",bg="lightgrey", font=font_big).pack()

    # Pie chart for category breakdown
    category_totals = {}
    for exp in expenses:
        category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

    if category_totals:
        fig, ax = plt.subplots(figsize=(5, 5))
        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title("Expenses by Category")

        canvas = FigureCanvasTkAgg(fig, master=analysis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
    else:
        tk.Label(analysis_window, text="No expenses to analyze.", font=font_big).pack(pady=20)

# ------------------- MAIN -------------------
class ExpenseApp(tk):
    root = tk.Tk()
    root.configure(bg="lightgrey")
    root.title("💰Expense Tracker")
    root.geometry("1200x800")

    load_expenses()
    # Call load_budget() at startup (add this after load_expenses())
    load_budget()

    font_big = ("Arial", 14)
    tk.Label(root, text="💰" "Expense Tracker",bg="lightgrey",fg="orange", font=("Arial", 26, "bold")).pack(pady=30)

    tk.Button(root, text="➕Add Expense", command=gui_add_expense, width=30, height=2,bg="lightblue", font=font_big).pack(pady=10)
    tk.Button(root, text="📋Show Expenses", command=gui_show_expenses, width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
    tk.Button(root, text="🎯Set Budget", command=gui_set_budget, width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
    tk.Button(root, text="🔍Check Budget", command=gui_check_budget, width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
    tk.Button(root, text="📊Analysis", command=gui_analysis, width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)

    root.mainloop()

    #create function to run program  