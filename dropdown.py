import customtkinter as ctk

class DropdownMenu:
    def __init__(self, master=None, options=None, displayText="Select Options"):
        self.master = master
        self.selectedValues = []
        self.options = options if options else []


        self.button = ctk.CTkButton(self.master, text=displayText, command=self.showDropdown)

    def showDropdown(self):
        # Create a dropdown window
        dropdown = ctk.CTkToplevel(self.master)
        dropdown.title("Select Options")
        dropdown.transient(self.master)

        # Position dropdown relative to the parent
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty() + self.master.winfo_height()
        dropdown.geometry(f"+{x}+{y}")

        # Add checkboxes for options
        self.checkVars = {}
        for option in self.options:
            var = ctk.BooleanVar(value=option in self.selectedValues)
            chk = ctk.CTkCheckBox(dropdown, text=option, variable=var, 
                                  command=lambda opt=option, v=var: self.toggleOption(opt, v))
            chk.pack(anchor="w", padx=5, pady=2)
            self.checkVars[option] = var

        # Close button
        closeButton = ctk.CTkButton(dropdown, text="Done", command=dropdown.destroy)
        closeButton.pack(pady=5)

    def toggleOption(self, option, var):
        if var.get():
            if option not in self.selectedValues:
                self.selectedValues.append(option)
        else:
            if option in self.selectedValues:
                self.selectedValues.remove(option)
