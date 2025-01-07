import customtkinter as tk
from interface import Interface

def main():
    root = tk.CTk()
    interface = Interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# TODO: Data is squished
# TODO: Open chart in full screen
# TODO: When visualising, make prices only be whole numbers
# TODO: Refactor Code and remove unnecessary parts