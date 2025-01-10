import customtkinter as tk
from interface import Interface

def main():
    root = tk.CTk()
    interface = Interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# TODO: Make chart close when root closes
# TODO: Make the table prettier
# TODO Change everything to CamelCase