
import tkinter as tk
from gui import link_engineering_interface as gui

def main():
    root = tk.Tk()
    app = gui.LinkEngineeringInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
