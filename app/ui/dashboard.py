import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ..backend import service

class DashboardView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Content.TFrame")
        
        # Header
        header = ttk.Label(self, text="Dashboard", style="Header.TLabel")
        header.pack(anchor=tk.W, pady=(0, 20))

        # KPI Container
        kpi_frame = ttk.Frame(self, style="Content.TFrame")
        kpi_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.stats = service.get_dashboard_stats()
        
        # KPI Cards
        self._create_card(kpi_frame, "Total Income", f"₹{self.stats['total_income']:,.2f}", 0)
        self._create_card(kpi_frame, "Total Expense", f"₹{self.stats['total_expense']:,.2f}", 1)
        self._create_card(kpi_frame, "Net Profit", f"₹{self.stats['net_profit']:,.2f}", 2)
        self._create_card(kpi_frame, "Repeat Cust. %", f"{self.stats['repeat_customer_rate']}%", 3)

        # Charts Area
        charts_frame = ttk.Frame(self, style="Content.TFrame")
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Revenue Trend Chart
        self._create_trend_chart(charts_frame)

    def _create_card(self, parent, title, value, col_idx):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.grid(row=0, column=col_idx, padx=10, sticky=tk.EW)
        
        ttk.Label(card, text=title, style="CardHeader.TLabel").pack(anchor=tk.W)
        ttk.Label(card, text=value, style="CardValue.TLabel").pack(anchor=tk.W, pady=(5, 0))
        
        parent.columnconfigure(col_idx, weight=1)

    def _create_trend_chart(self, parent):
        dates, values = service.get_revenue_trend_data()
        
        # Create Figure without Pyplot's state machine to avoid thread issues
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if dates is not None and len(dates) > 0:
            ax.plot(dates, values, marker='o', linestyle='-', color='#18BC9C', linewidth=2)
            ax.set_title("Revenue Trend", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.5)
            # Format dates nicely if there are many
            fig.autofmt_xdate()
        else:
            ax.text(0.5, 0.5, "No Data Available", horizontalalignment='center', verticalalignment='center')
            ax.set_yticklabels([])
            ax.set_xticklabels([])

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
