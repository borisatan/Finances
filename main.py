import customtkinter as tk
from interface import Interface

def main():
    root = tk.CTk()
    interface = Interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# TODO: Fix horizontal scrolling / description wrapping?
# TODO: Add space between each row to make them more readable