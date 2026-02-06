import tkinter as tk
from tkinter import ttk, messagebox
from ..backend import service

class CustomersView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Content.TFrame")
        
        # Header
        ttk.Label(self, text="Customer Management", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))

        # Toolbar (Add New)
        toolbar = ttk.Frame(self, style="Content.TFrame")
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="+ Add New Customer", command=self._show_add_dialog).pack(side=tk.LEFT)

        # Table
        columns = ("ID", "Name", "Gender", "Contact", "First Purchase")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        # Heading config
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Verify Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Standard pack separation issue, simple fix:
        # Repack tree and scrollbar in a container if needed, but for now simple pack
        
        self._load_data()

    def _load_data(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        customers = service.get_all_customers()
        for c in customers:
            self.tree.insert("", tk.END, values=(
                c['customer_id'],
                c['name'],
                c['gender'],
                c['contact'] or "N/A",
                c['first_purchase_date']
            ))

    def _show_add_dialog(self):
        # Simple Toplevel Dialog
        dialog = tk.Toplevel(self)
        dialog.title("Add Customer")
        dialog.geometry("400x300")
        
        # Fields
        ttk.Label(dialog, text="Name:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(fill=tk.X, padx=20)
        
        ttk.Label(dialog, text="Gender:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        gender_var = tk.StringVar(value="Unknown")
        ttk.Combobox(dialog, textvariable=gender_var, values=["Male", "Female", "Other", "Unknown"]).pack(fill=tk.X, padx=20)

        ttk.Label(dialog, text="Contact:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        contact_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=contact_var).pack(fill=tk.X, padx=20)
        
        def save():
            if not name_var.get().strip():
                messagebox.showerror("Error", "Name is required", parent=dialog)
                return
            
            try:
                service.add_customer(name_var.get(), gender_var.get(), contact_var.get())
                self._load_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Customer Added!")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(dialog, text="Save", command=save).pack(pady=20)
