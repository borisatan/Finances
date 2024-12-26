import customtkinter as tk
from interface import Interface

def main():
    root = tk.CTk()
    interface = Interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# TODO: display by category, line graph per category
# TODO: shop and transactions in category