import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from ..backend import service

class ReportsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Content.TFrame")
        
        ttk.Label(self, text="Reports & Export", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))

        # Controls
        ctrl_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        ctrl_frame.pack(fill=tk.X)

        ttk.Label(ctrl_frame, text="Export All Transactions").pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(ctrl_frame, style="Card.TFrame")
        btn_frame.pack(anchor=tk.W, pady=10)

        ttk.Button(btn_frame, text="Export to CSV", command=self._export_csv).pack(side=tk.LEFT, padx=10)
        
        pdf_btn = ttk.Button(btn_frame, text="Export as PDF (Pro)", command=self._export_pdf)
        pdf_btn.pack(side=tk.LEFT, padx=10)
        
        if not service.IS_PRO_VERSION:
            pdf_btn.configure(state="disabled")

        # Future: Date Range Picker for filtered reports

    def _export_csv(self):
        df = service.analytics.get_transactions_df()
        if df.empty:
            messagebox.showwarning("No Data", "No transactions to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if path:
            try:
                df.to_csv(path, index=False)
                messagebox.showinfo("Success", f"Exported to {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    def _export_pdf(self):
        df = service.analytics.get_transactions_df()
        if df.empty:
            messagebox.showwarning("No Data", "No transactions to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if path:
            try:
                self._generate_pdf(df, path)
                messagebox.showinfo("Success", f"PDF Report Saved: {path}")
            except Exception as e:
                messagebox.showerror("Error", f"PDF Export failed: {e}")

    def _generate_pdf(self, df, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Business Finance Report", ln=1, align="C")
        pdf.cell(200, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1, align="C")
        pdf.ln(10)

        # Summary
        stats = service.get_dashboard_stats()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Total Income: {stats['total_income']}", ln=1)
        pdf.cell(0, 10, f"Total Expense: {stats['total_expense']}", ln=1)
        pdf.cell(0, 10, f"Net Profit: {stats['net_profit']}", ln=1)
        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", 'B', 10)
        cols = ["Date", "Type", "Category", "Amount", "Method"]
        col_widths = [30, 20, 40, 30, 40]
        
        for i, col in enumerate(cols):
            pdf.cell(col_widths[i], 10, col, 1)
        pdf.ln()

        # Table Rows
        pdf.set_font("Arial", size=10)
        # Limit rows for PDF simple version
        for _, row in df.head(50).iterrows():
            pdf.cell(col_widths[0], 10, str(row['txn_date'])[:10], 1)
            pdf.cell(col_widths[1], 10, str(row['txn_type']), 1)
            pdf.cell(col_widths[2], 10, str(row['category'])[:20], 1) # truncate
            pdf.cell(col_widths[3], 10, str(row['amount']), 1)
            pdf.cell(col_widths[4], 10, str(row['payment_method']), 1)
            pdf.ln()

        pdf.output(filename)
