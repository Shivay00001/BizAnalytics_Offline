import tkinter as tk
from tkinter import ttk

# -- Color Palette --
# clean, professional, "business" colors
PRIMARY_COLOR = "#2C3E50"    # Dark Blue/Slate
SECONDARY_COLOR = "#18BC9C"  # Teal/Success
ACCENT_COLOR = "#E74C3C"     # Red/Expense
BG_COLOR = "#ECF0F1"         # Light Gray
SIDEBAR_BG = "#34495E"       # Darker Slate
TEXT_COLOR = "#2C3E50"
WHITE = "#FFFFFF"

# -- Font Settings --
HEADER_FONT = ("Segoe UI", 16, "bold")
SUBHEADER_FONT = ("Segoe UI", 12, "bold")
NORMAL_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)

def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")  # 'clam' allows more customizability than 'vista'

    # Configure General TFrame
    style.configure("TFrame", background=BG_COLOR)
    
    # Configure Sidebar
    style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
    
    # Configure Content Area
    style.configure("Content.TFrame", background=BG_COLOR)

    # Configure Card (White box)
    style.configure("Card.TFrame", background=WHITE, relief="groove")

    # Configure Label
    style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=NORMAL_FONT)
    style.configure("Sidebar.TLabel", background=SIDEBAR_BG, foreground=WHITE, font=SUBHEADER_FONT)
    style.configure("Header.TLabel", font=HEADER_FONT, background=BG_COLOR)
    style.configure("CardHeader.TLabel", font=SUBHEADER_FONT, background=WHITE, foreground=PRIMARY_COLOR)
    style.configure("CardValue.TLabel", font=("Segoe UI", 20, "bold"), background=WHITE, foreground=TEXT_COLOR)
    
    # Configure Button
    style.configure("TButton", 
                    font=NORMAL_FONT, 
                    background=PRIMARY_COLOR, 
                    foreground=WHITE, 
                    borderwidth=0, 
                    focuscolor=SECONDARY_COLOR)
    style.map("TButton", 
              background=[('active', SECONDARY_COLOR), ('pressed', '#16A085')])

    # Configure Entry
    style.configure("TEntry", fieldbackground=WHITE, font=NORMAL_FONT, padding=5)

    # Configure Sidebar Button (Custom style usually requires more work, but we'll try simple first)
    style.configure("Sidebar.TButton", 
                    font=SUBHEADER_FONT,
                    background=SIDEBAR_BG,
                    foreground=WHITE,
                    anchor="w",
                    padding=10,
                    borderwidth=0)
    style.map("Sidebar.TButton",
              background=[('active', '#2C3E50')])

    # Treeview (List)
    style.configure("Treeview", 
                    background=WHITE,
                    foreground=TEXT_COLOR,
                    fieldbackground=WHITE,
                    font=NORMAL_FONT,
                    rowheight=25)
    style.configure("Treeview.Heading", 
                    font=SUBHEADER_FONT, 
                    background=PRIMARY_COLOR, 
                    foreground=WHITE)
