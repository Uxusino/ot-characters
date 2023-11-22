from tkinter import Tk
from ui.ui import UI #pylint: disable=E0401

def main():
    window = Tk()
    window.title("OT-characters")

    ui = UI(window)
    ui.start()

    window.mainloop()

if __name__ == "__main__":
    main()
