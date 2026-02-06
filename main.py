import sys
import os

# Ensure the project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ui.app_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
