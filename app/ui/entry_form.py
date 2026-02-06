import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # Might need to recommend installing this or use standard Entry
from datetime import datetime
from ..backend import service

# Fallback if tkcalendar is not installed (though strictly we didn't list it in requirements,
# standard Entry with YYYY-MM-DD validation is safer for "zero dependencies" request, but 
# DateEntry is much better UX. I'll stick to Entry for strict compliance or recommend it. 
# Plan: Use simple date entry with default = today for simplicity as requirement was "No paid APIs, etc", 
# but user didn't ban pip packages. I'll stick to standard Entry to reduce dependency risk.)

class EntryFormView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Content.TFrame")
        
        # Header
        ttk.Label(self, text="Add New Transaction", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))

        # Form Container
        form_frame = ttk.Frame(self, style="Card.TFrame", padding=30)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50) # Centered-ish

        # -- Fields --
        
        # Type (Income/Expense)
        ttk.Label(form_frame, text="Transaction Type", style="TLabel").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.txn_type_var = tk.StringVar(value="Income")
        type_cb = ttk.Combobox(form_frame, textvariable=self.txn_type_var, values=["Income", "Expense"], state="readonly")
        type_cb.grid(row=0, column=1, sticky=tk.EW, pady=10)
        type_cb.bind("<<ComboboxSelected>>", self._on_type_change)

        # Amount
        ttk.Label(form_frame, text="Amount (₹)", style="TLabel").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(form_frame, textvariable=self.amount_var).grid(row=1, column=1, sticky=tk.EW, pady=10)

        # Category
        ttk.Label(form_frame, text="Category", style="TLabel").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.category_var = tk.StringVar()
        self.cat_cb = ttk.Combobox(form_frame, textvariable=self.category_var) # Editable
        self.cat_cb.grid(row=2, column=1, sticky=tk.EW, pady=10)
        self._update_categories()

        # Date (YYYY-MM-DD)
        ttk.Label(form_frame, text="Date (YYYY-MM-DD)", style="TLabel").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=self.date_var).grid(row=3, column=1, sticky=tk.EW, pady=10)

        # Payment Method
        ttk.Label(form_frame, text="Payment Method", style="TLabel").grid(row=4, column=0, sticky=tk.W, pady=10)
        self.pay_method_var = tk.StringVar(value="Cash")
        ttk.Combobox(form_frame, textvariable=self.pay_method_var, values=["Cash", "UPI", "Bank Transfer", "Cheque", "Card"], state="readonly").grid(row=4, column=1, sticky=tk.EW, pady=10)

        # Customer (Only if Income)
        self.cust_lbl = ttk.Label(form_frame, text="Customer", style="TLabel")
        self.cust_lbl.grid(row=5, column=0, sticky=tk.W, pady=10)
        
        self.customer_var = tk.StringVar()
        self.cust_cb = ttk.Combobox(form_frame, textvariable=self.customer_var)
        self.cust_cb.grid(row=5, column=1, sticky=tk.EW, pady=10)
        self._refresh_customers()

        # Reason/Notes
        ttk.Label(form_frame, text="Reason/Notes", style="TLabel").grid(row=6, column=0, sticky=tk.W, pady=10)
        self.reason_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.reason_var).grid(row=6, column=1, sticky=tk.EW, pady=10)

        # Buttons
        btn_frame = ttk.Frame(form_frame, style="Card.TFrame") # Match bg
        btn_frame.grid(row=7, column=0, columnspan=2, pady=30)
        
        ttk.Button(btn_frame, text="Save Transaction", command=self._save_transaction).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Clear", command=self._clear_form).pack(side=tk.LEFT, padx=10)

        form_frame.columnconfigure(1, weight=1)

    def _on_type_change(self, event=None):
        self._update_categories()
        # Hide customer if Expense? Usually expenses don't have "customers" but "vendors". 
        # For simplicity, we keep it visible but maybe optional for expense.
        # User requirement: "Group entries by customer if Income".

    def _update_categories(self):
        txn_type = self.txn_type_var.get()
        if txn_type == "Income":
            values = ["Sales", "Service", "Consulting", "Other"]
        else:
            values = ["Rent", "Salaries", "Utilities", "Inventory", "Marketing", "Other"]
        self.cat_cb['values'] = values
        self.cat_cb.current(0)

    def _refresh_customers(self):
        customers = service.get_all_customers()
        # Storing ID mapping could be done, but for now names are unique enough for MVP or we parse
        # Implementing a simple "Name (ID)" format or just Name.
        # For a truly robust app, we'd use a hidden ID mapping.
        self.cust_dict = {c['name']: c['customer_id'] for c in customers}
        self.cust_cb['values'] = list(self.cust_dict.keys())

    def _save_transaction(self):
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            
            cust_name = self.customer_var.get().strip()
            # Logic: If Income and Customer name provided but not in list -> Create new customer automatically?
            # Or ask user. "Simple and fast" logic -> Auto create if new.
            customer_id = None
            if cust_name:
                if cust_name in self.cust_dict:
                    customer_id = self.cust_dict[cust_name]
                else:
                    # Auto-create new customer
                    # Minimal info for now
                    customer_id = service.add_customer(cust_name, "Unknown", None)
                    self._refresh_customers()
            
            service.add_transaction(
                customer_id=customer_id,
                amount=amount,
                txn_type=self.txn_type_var.get(),
                category=self.category_var.get(),
                reason=self.reason_var.get(),
                payment_method=self.pay_method_var.get(),
                txn_date=self.date_var.get()
            )
            
            messagebox.showinfo("Success", "Transaction Saved!")
            self._clear_form()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def _clear_form(self):
        self.amount_var.set(0.0)
        self.reason_var.set("")
        self.customer_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
