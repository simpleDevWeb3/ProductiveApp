import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#--------- File Handling ---------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "expenses.txt")
BUDGET_FILE = os.path.join(BASE_DIR, "budget.txt")


def format_amount(amount):
    return f"{float(amount):.2f}"

#--------- Expense Class and Validation ---------
class Expense:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.description = description

    def __str__(self):
        return f"{self.date},{self.category},{format_amount(self.amount)},{self.description}"

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

#--------- Data Handling ---------
expenses = []
budget = 0

def load_expenses():
    expenses.clear()
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

# --- GUI with Frames ---
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgrey")
        font_big = ("Arial", 14)
        tk.Label(self, text="💰Expense Tracker", bg="lightgrey", fg="orange", font=("Arial", 26, "bold")).pack(pady=30)
        tk.Button(self, text="➕Add Expense", command=lambda: controller.show_frame(AddExpensePage), width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
        tk.Button(self, text="📋Show Expenses", command=lambda: controller.show_frame(ShowExpensesPage), width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
        tk.Button(self, text="🎯Set Budget", command=lambda: controller.show_frame(SetBudgetPage), width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
        tk.Button(self, text="🔍Check Budget", command=lambda: controller.show_frame(CheckBudgetPage), width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)
        tk.Button(self, text="📊Analysis", command=lambda: controller.show_frame(AnalysisPage), width=30, height=2, bg="lightblue", font=font_big).pack(pady=10)

class AddExpensePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgrey")
        font_big = ("Arial", 14)
        tk.Label(self, text="➕Add Expenses", fg="orange", bg="lightgrey", font=("Arial", 22, "bold", "underline")).pack(pady=20)
        frame = tk.Frame(self, bg="lightgrey")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Date (YYYY-MM-DD):", font=font_big, bg="lightgrey").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.date_entry = tk.Entry(frame, font=font_big)
        self.date_entry.grid(row=0, column=1, pady=5)
        self.date_error = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="lightgrey")
        self.date_error.grid(row=1, columnspan=2)

        tk.Label(frame, text="Category:", font=font_big, bg="lightgrey").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.category_combo = ttk.Combobox(frame, values=["Rent & Bills", "Food & Drinks", "Transport", "Entertainment"], font=font_big)
        self.category_combo.grid(row=2, column=1, pady=5)
        self.category_error = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="lightgrey")
        self.category_error.grid(row=3, columnspan=2)

        tk.Label(frame, text="Amount:", font=font_big, bg="lightgrey").grid(row=4, column=0, sticky="e", pady=5, padx=5)
        self.amount_entry = tk.Entry(frame, font=font_big)
        self.amount_entry.grid(row=4, column=1, pady=5)
        self.amount_error = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="lightgrey")
        self.amount_error.grid(row=5, columnspan=2)

        tk.Label(frame, text="Description:", font=font_big, bg="lightgrey").grid(row=6, column=0, sticky="e", pady=5, padx=5)
        self.desc_entry = tk.Entry(frame, font=font_big)
        self.desc_entry.grid(row=6, column=1, pady=5)
        self.desc_error = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="lightgrey")
        self.desc_error.grid(row=7, columnspan=2)

        tk.Button(frame, text="Save", command=self.save_entry, bg="lightgreen", fg="white", font=font_big, width=15, height=2).grid(row=8, columnspan=2, pady=20)

        # Back button fixed at bottom
        back_frame = tk.Frame(self, bg="lightgrey")
        back_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(back_frame, text="Back", command=lambda: controller.show_frame(MainMenu), font=font_big).pack()

    def save_entry(self):
        self.date_error.config(text="")
        self.category_error.config(text="")
        self.amount_error.config(text="")
        self.desc_error.config(text="")

        has_error = False

        valid, result = validate_date(self.date_entry.get())
        if not valid:
            self.date_error.config(text=result)
            has_error = True
        else:
            date = result

        category_value = self.category_combo.get()
        valid, result = validate_category(category_value)
        if not valid:
            self.category_error.config(text=result)
            has_error = True
        else:
            category = result

        valid, result = validate_amount(self.amount_entry.get())
        if not valid:
            self.amount_error.config(text=result)
            has_error = True
        else:
            amount = result

        valid, result = validate_description(self.desc_entry.get())
        if not valid:
            self.desc_error.config(text=result)
            has_error = True
        else:
            description = result

        if has_error:
            return

        exp = Expense(date, category, amount, description)
        expenses.append(exp)
        save_expenses()
        messagebox.showinfo("Success", "Expense added!")
        self.date_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

class ShowExpensesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgrey")
        font_big = ("Arial", 14)

        # Title
        tk.Label(
            self,
            text="📋Show Expenses",
            fg="dark orange",
            bg="lightgrey",
            font=("Arial", 22, "bold", "underline"),
        ).pack(pady=20)

        # Frame for Treeview
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(
            frame,
            height=15,
            columns=("Date", "Category", "Amount", "Description"),
            show="headings",
        )
        self.sort_desc = True  # start descending

        # Headings
        self.tree.heading("Date", text="Date ↓", command=self.sort_by_date)
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        # Columns center align
        self.tree.column("Date", anchor="center")
        self.tree.column("Category", anchor="center")
        self.tree.column("Amount", anchor="center")
        self.tree.column("Description", anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill="both")

        # Buttons
        tk.Button(
            self,
            text="Delete Selected",
            command=self.delete_selected,
            bg="red",
            fg="white",
            font=font_big,
            width=20,
        ).pack(pady=10)

        tk.Button(
            self,
            text="Delete All",
            command=self.delete_all,
            bg="red",
            fg="white",
            font=font_big,
            width=20,
        ).pack(pady=10)

        # Back button
        back_frame = tk.Frame(self, bg="lightgrey")
        back_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(
            back_frame,
            text="Back",
            command=lambda: controller.show_frame(MainMenu),
            font=font_big,
        ).pack()

        # Fill table
        self.refresh_tree()

    # ----------------- Refresh Tree -----------------
    def refresh_tree(self, sort_by_date=False):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Sort if needed
        if sort_by_date:
            sorted_exp = sorted(
                expenses,
                key=lambda e: datetime.datetime.strptime(e.date, "%Y-%m-%d"),
                reverse=self.sort_desc,
            )
        else:
            sorted_exp = expenses

        for exp in sorted_exp:
            self.tree.insert(
                "",
                "end",
                values=(exp.date, exp.category, format_amount(exp.amount), exp.description),
            )



    # ----------------- Delete Selected -----------------
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No expense selected.")
            return

        # Get values of selected rows
        to_delete = []
        for item in selected:
            values = self.tree.item(item, "values")
            to_delete.append(values)

        # Remove from expenses list
        for values in to_delete:
            for exp in expenses:
                if (
                    exp.date == values[0]
                    and exp.category == values[1]
                    and format_amount(exp.amount) == values[2]
                    and exp.description == values[3]
                ):
                    expenses.remove(exp)
                    break

        # Update UI + file
        self.refresh_tree(sort_by_date=True)
        save_expenses()
        messagebox.showinfo("Success", "Selected expense(s) deleted.")

    # ----------------- Delete All -----------------
    def delete_all(self):
        if not expenses:
            messagebox.showwarning("Warning", "No expenses to delete.")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete ALL expenses?"):
            expenses.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            save_expenses()
            messagebox.showinfo("Success", "All expenses deleted.")

    # ----------------- Sort by Date -----------------
    def sort_by_date(self):
        self.sort_desc = not self.sort_desc
        self.refresh_tree(sort_by_date=True)

        # Update arrow in heading
        arrow = "↓" if self.sort_desc else "↑"
        self.tree.heading("Date", text=f"Date {arrow}", command=self.sort_by_date)


class SetBudgetPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgrey")
        font_big = ("Arial", 14)
        tk.Label(self, text="🎯Set Budget", fg="dark orange", bg="lightgrey", font=("Arial", 22, "bold", "underline")).pack(pady=20)
        frame = tk.Frame(self, bg="lightgrey")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="Enter budget: RM", font=font_big, bg="lightgrey").pack(pady=10)
        preset_amounts = ["100", "200", "500", "1000", "2000"]
        self.budget_entry = ttk.Combobox(frame, values=preset_amounts, font=font_big, width=23)
        self.budget_entry.pack(pady=10)
        tk.Button(frame, text="Save", command=self.save_budget, font=font_big, width=15, height=2, bg="lightgreen").pack(pady=10)

        # Back button fixed at bottom
        back_frame = tk.Frame(self, bg="lightgrey")
        back_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(back_frame, text="Back", command=lambda: controller.show_frame(MainMenu), font=font_big).pack()

    def save_budget(self):
        try:
            value = float(self.budget_entry.get())
            if value <= 0:
                raise ValueError
            global budget
            budget = value
            save_budget_to_file()
            messagebox.showinfo("Success", f"Budget set to RM {format_amount(budget)}")
            self.budget_entry.set("")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive number")

class CheckBudgetPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgrey")
        font_big = ("Arial", 14)
        tk.Label(self, text="🔍Check Budget", fg="dark orange", bg="lightgrey", font=("Arial", 22, "bold", "underline")).pack(pady=20)
        self.budget_label = tk.Label(self, bg="lightgrey", font=font_big)
        self.spent_label = tk.Label(self, bg="lightgrey", font=font_big)
        self.status_label = tk.Label(self, bg="lightgrey", font=font_big)
        self.budget_label.pack(pady=10)
        self.spent_label.pack(pady=10)
        self.status_label.pack(pady=10)

        # Back button fixed at bottom
        back_frame = tk.Frame(self, bg="lightgrey")
        back_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(back_frame, text="Back", command=lambda: controller.show_frame(MainMenu), font=font_big).pack()

        self.update_labels()

    def update_labels(self):
        total_spent = sum(exp.amount for exp in expenses)
        self.budget_label.config(text=f"Budget: RM {format_amount(budget)}")
        self.spent_label.config(text=f"Total Spent: RM {format_amount(total_spent)}")
        if budget > 0:
            if total_spent > budget:
                self.status_label.config(text="⚠ You have exceeded your budget!", fg="red")
            else:
                self.status_label.config(text="✅ You are within your budget.", fg="green")
        else:
            self.status_label.config(text="No budget set yet.", fg="blue")

class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightgrey")
        font_big = ("Arial", 14)
        tk.Label(self, text="📊Expense Analysis", fg="orange", bg="lightgrey", font=("Arial", 22, "bold", "underline")).pack(pady=20)
        self.total_label = tk.Label(self, bg="lightgrey", font=font_big)
        self.budget_label = tk.Label(self, bg="lightgrey", font=font_big)
        self.status_label = tk.Label(self, bg="lightgrey", font=font_big)
        self.total_label.pack(pady=10)
        self.budget_label.pack(pady=10)
        self.status_label.pack()
        self.canvas = None

        # Back button fixed at bottom
        back_frame = tk.Frame(self, bg="lightgrey")
        back_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(back_frame, text="Back", command=lambda: controller.show_frame(MainMenu), font=font_big).pack()

        self.update_analysis()

    def update_analysis(self):
        total_spent = sum(exp.amount for exp in expenses)
        self.total_label.config(text=f"Total Spent: RM {format_amount(total_spent)}")
        if budget > 0:
            self.budget_label.config(text=f"Budget: RM {format_amount(budget)}")
            if total_spent > budget:
                self.status_label.config(text="You have exceeded your budget!", fg="red")
            else:
                self.status_label.config(text="You are within your budget.", fg="green")
        else:
            self.budget_label.config(text="")
            self.status_label.config(text="No budget set yet.", fg="blue")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        category_totals = {}
        for exp in expenses:
            category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

        if category_totals:
            fig, ax = plt.subplots(figsize=(5, 5))
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title("Expenses by Category")
            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=20)

#--------- Main Application ---------
class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("900x650")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for Page in (MainMenu, AddExpensePage, ShowExpensesPage, SetBudgetPage, CheckBudgetPage, AnalysisPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

    def show_frame(self, page):
        frame = self.frames[page]
        if isinstance(frame, ShowExpensesPage):
            frame.refresh_tree()
        elif isinstance(frame, CheckBudgetPage):
            frame.update_labels()
        elif isinstance(frame, AnalysisPage):
            frame.update_analysis()
        frame.tkraise()
        
#--------- Run Application ---------
if __name__ == "__main__":
    load_expenses()
    load_budget()
    app = ExpenseApp()
    app.mainloop()

