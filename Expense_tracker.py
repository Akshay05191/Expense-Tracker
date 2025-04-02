import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import json
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Akshay S")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")
        
        # Custom styling
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0f2f5")
        self.style.configure('TLabel', background="#f0f2f5", font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        
        # Data file
        self.data_file = "expenses.json"
        self.categories = [
            "Food", "Transport", "Entertainment", 
            "Utilities", "Shopping", "Healthcare", 
            "Education", "Other"
        ]
        
        # Initialize data
        self.expenses = []
        self.load_data()
        
        # Create UI
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            self.header_frame, 
            text="Personal Expense Tracker", 
            style="Header.TLabel"
        ).pack(side=tk.LEFT)
        
        # Add expense button
        ttk.Button(
            self.header_frame, 
            text="+ Add Expense", 
            command=self.open_add_expense_dialog,
            style="TButton"
        ).pack(side=tk.RIGHT)
        
        # Content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Form and expenses list
        self.left_panel = ttk.Frame(self.content_frame, width=400)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20))
        
        # Expenses list
        self.expense_list_frame = ttk.LabelFrame(self.left_panel, text="Recent Expenses", padding=10)
        self.expense_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            self.expense_list_frame, 
            columns=("date", "category", "amount", "description"), 
            show="headings",
            selectmode="browse"
        )
        
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("description", text="Description")
        
        self.tree.column("date", width=100)
        self.tree.column("category", width=120)
        self.tree.column("amount", width=80)
        self.tree.column("description", width=200)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Delete button
        ttk.Button(
            self.left_panel, 
            text="Delete Selected", 
            command=self.delete_expense,
            style="TButton"
        ).pack(pady=(10, 0))
        
        # Right panel - Statistics and charts
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Summary frame
        self.summary_frame = ttk.LabelFrame(self.right_panel, text="Summary", padding=10)
        self.summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.summary_labels = {}
        summary_items = [
            ("Total Expenses", "total"),
            ("This Month", "month"),
            ("Most Spent Category", "top_category"),
            ("Average Daily", "daily_avg")
        ]
        
        for i, (text, key) in enumerate(summary_items):
            frame = ttk.Frame(self.summary_frame)
            frame.grid(row=i//2, column=i%2, sticky="we", padx=5, pady=5)
            
            ttk.Label(frame, text=text+":", font=('Helvetica', 10, 'bold')).pack(anchor="w")
            self.summary_labels[key] = ttk.Label(frame, text="", font=('Helvetica', 10))
            self.summary_labels[key].pack(anchor="w")
        
        # Charts frame
        self.charts_frame = ttk.LabelFrame(self.right_panel, text="Visualization", padding=10)
        self.charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.fig.set_facecolor("#f0f2f5")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.expenses = json.load(f)
        else:
            self.expenses = []
    
    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.expenses, f, indent=2)
    
    def open_add_expense_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Expense")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Amount:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        amount_var = tk.DoubleVar()
        ttk.Entry(dialog, textvariable=amount_var).grid(row=0, column=1, padx=10, pady=10, sticky="we")
        
        ttk.Label(dialog, text="Category:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(dialog, textvariable=category_var, values=self.categories)
        category_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        category_combobox.current(0)
        
        ttk.Label(dialog, text="Date:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(dialog, textvariable=date_var).grid(row=2, column=1, padx=10, pady=10, sticky="we")
        
        ttk.Label(dialog, text="Description:").grid(row=3, column=0, padx=10, pady=10, sticky="ne")
        description_var = tk.StringVar()
        description_entry = tk.Text(dialog, height=5, width=30)
        description_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        
        def add_expense():
            try:
                amount = amount_var.get()
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                date = date_var.get()
                datetime.strptime(date, "%Y-%m-%d")  # Validate date format
                
                expense = {
                    "amount": amount,
                    "category": category_var.get(),
                    "date": date,
                    "description": description_entry.get("1.0", tk.END).strip()
                }
                
                self.expenses.append(expense)
                self.save_data()
                self.update_display()
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            dialog, 
            text="Add Expense", 
            command=add_expense,
            style="TButton"
        ).grid(row=4, column=1, padx=10, pady=10, sticky="e")
        
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected expense?"):
            index = self.tree.index(selected[0])
            del self.expenses[index]
            self.save_data()
            self.update_display()
    
    def update_display(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add expenses to treeview (sorted by date, newest first)
        sorted_expenses = sorted(
            self.expenses, 
            key=lambda x: x["date"], 
            reverse=True
        )
        
        for expense in sorted_expenses:
            self.tree.insert("", "end", values=(
                expense["date"],
                expense["category"],
                f"${expense['amount']:.2f}",
                expense["description"]
            ))
        
        # Update summary
        self.update_summary()
        
        # Update charts
        self.update_charts()
    
    def update_summary(self):
        if not self.expenses:
            self.summary_labels["total"].config(text="$0.00")
            self.summary_labels["month"].config(text="$0.00")
            self.summary_labels["top_category"].config(text="N/A")
            self.summary_labels["daily_avg"].config(text="$0.00")
            return
        
        # Total expenses
        total = sum(expense["amount"] for expense in self.expenses)
        self.summary_labels["total"].config(text=f"${total:.2f}")
        
        # This month's expenses
        current_month = datetime.now().strftime("%Y-%m")
        month_expenses = [
            exp["amount"] for exp in self.expenses 
            if exp["date"].startswith(current_month)
        ]
        month_total = sum(month_expenses) if month_expenses else 0
        self.summary_labels["month"].config(text=f"${month_total:.2f}")
        
        # Most spent category
        category_totals = {}
        for exp in self.expenses:
            category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + exp["amount"]
        
        if category_totals:
            top_category = max(category_totals.items(), key=lambda x: x[1])
            self.summary_labels["top_category"].config(
                text=f"{top_category[0]} (${top_category[1]:.2f})"
            )
        else:
            self.summary_labels["top_category"].config(text="N/A")
        
        # Average daily expense
        if self.expenses:
            dates = [datetime.strptime(exp["date"], "%Y-%m-%d") for exp in self.expenses]
            min_date = min(dates)
            max_date = max(dates)
            days = (max_date - min_date).days + 1  # Avoid division by zero
            daily_avg = total / days
            self.summary_labels["daily_avg"].config(text=f"${daily_avg:.2f}")
        else:
            self.summary_labels["daily_avg"].config(text="$0.00")
    
    def update_charts(self):
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        if not self.expenses:
            self.ax1.text(0.5, 0.5, 'No data available', 
                         ha='center', va='center', fontsize=12)
            self.ax2.text(0.5, 0.5, 'No data available', 
                         ha='center', va='center', fontsize=12)
            self.canvas.draw()
            return
        
        # Prepare data for charts
        categories = {}
        monthly = {}
        
        for exp in self.expenses:
            # Category breakdown
            categories[exp["category"]] = categories.get(exp["category"], 0) + exp["amount"]
            
            # Monthly expenses
            month = exp["date"][:7]  # YYYY-MM
            monthly[month] = monthly.get(month, 0) + exp["amount"]
        
        # Category pie chart
        if categories:
            labels = list(categories.keys())
            sizes = list(categories.values())
            
            self.ax1.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%',
                startangle=90,
                colors=plt.cm.Pastel1.colors,
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
            )
            self.ax1.set_title('Expense by Category')
            self.ax1.axis('equal')
        
        # Monthly bar chart
        if monthly:
            months = sorted(monthly.keys())
            amounts = [monthly[m] for m in months]
            
            bars = self.ax2.bar(
                months, 
                amounts, 
                color=plt.cm.Pastel2.colors
            )
            self.ax2.set_title('Monthly Expenses')
            self.ax2.set_ylabel('Amount ($)')
            self.ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                self.ax2.text(
                    bar.get_x() + bar.get_width()/2., 
                    height,
                    f'${height:.0f}',
                    ha='center', 
                    va='bottom'
                )
        
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
