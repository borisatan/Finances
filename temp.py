import customtkinter as ctk

class MultiSelectCombobox(ctk.CTkFrame):
    def __init__(self, master=None, options=None, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_values = []
        self.options = options if options else []

        # Create a combobox-like button

        self.button = ctk.CTkButton(self, text="Select", command=self.show_dropdown)
        self.button.pack(fill="x", padx=5, pady=5)

    def show_dropdown(self):
        # Create a dropdown window
        dropdown = ctk.CTkToplevel(self)
        dropdown.title("Select Options")
        dropdown.transient(self)

        # Position dropdown relative to the parent
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        dropdown.geometry(f"+{x}+{y}")

        # Add checkboxes for options
        self.check_vars = {}
        for option in self.options:
            var = ctk.BooleanVar(value=option in self.selected_values)
            chk = ctk.CTkCheckBox(dropdown, text=option, variable=var, 
                                  command=lambda opt=option, v=var: self.toggle_option(opt, v))
            chk.pack(anchor="w", padx=5, pady=2)
            self.check_vars[option] = var

        # Close button
        close_button = ctk.CTkButton(dropdown, text="Done", command=dropdown.destroy)
        close_button.pack(pady=5)

    def toggle_option(self, option, var):
        if var.get():
            if option not in self.selected_values:
                self.selected_values.append(option)
        else:
            if option in self.selected_values:
                self.selected_values.remove(option)

        # Update the displayed text
        if self.selected_values:
            self.display_var.set(", ".join(self.selected_values))
        else:
            self.display_var.set("Select options")


# Main application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-select Combobox")
        self.geometry("300x200")

        # Create and pack the custom combobox
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        multi_select_combobox = MultiSelectCombobox(self, options=options)
        multi_select_combobox.pack(pady=20)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
    app = App()
    app.mainloop()
