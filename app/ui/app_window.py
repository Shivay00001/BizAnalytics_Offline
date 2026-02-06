import tkinter as tk
from tkinter import ttk
from .styles import apply_styles, BG_COLOR, SIDEBAR_BG, WHITE

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("BizAnalytics Offline - Pro")
        self.geometry("1100x700")
        self.state('zoomed') # Start maximized
        self.configure(bg=BG_COLOR)
        
        # Apply Styles
        apply_styles(self)
        
        # Main Layout: Sidebar (Left) + Content (Right)
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = ttk.Frame(self.main_container, style="Sidebar.TFrame", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False) # Force width

        self.content_area = ttk.Frame(self.main_container, style="Content.TFrame")
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.current_frame = None

        self._build_sidebar()
        self._init_placeholder_view()

    def _build_sidebar(self):
        # App Title in Sidebar
        title_lbl = ttk.Label(self.sidebar, text="BizAnalytics", style="Sidebar.TLabel", padding=20)
        title_lbl.pack(fill=tk.X)
        
        # Navigation Buttons
        # We will use simple styles for now
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Add Entry", self.show_entry_form),
            ("Customers", self.show_customers),
            ("Reports", self.show_reports),
        ]
        
        for text, command in nav_items:
            btn = ttk.Button(self.sidebar, text=text, command=command, style="Sidebar.TButton")
            btn.pack(fill=tk.X, pady=2, padx=5)

        # Version Info
        ver_lbl = ttk.Label(self.sidebar, text="v1.0 (Offline)", background=SIDEBAR_BG, foreground="#bdc3c7", padding=20)
        ver_lbl.pack(side=tk.BOTTOM)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with new one."""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self.content_area)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # --- Navigation Stubs ---
    def _init_placeholder_view(self):
        self.show_dashboard()

    def show_dashboard(self):
        from .dashboard import DashboardView
        self.switch_frame(DashboardView)

    def show_entry_form(self):
        from .entry_form import EntryFormView
        self.switch_frame(EntryFormView)

    def show_customers(self):
        from .customers import CustomersView
        self.switch_frame(CustomersView)

    def show_reports(self):
        from .reports import ReportsView
        self.switch_frame(ReportsView)

    def _show_temp_label(self, text):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.content_area)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        lbl = ttk.Label(self.current_frame, text=text, font=("Segoe UI", 24))
        lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
