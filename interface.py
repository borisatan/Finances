from data import Data
from data_visualiser import Visualiser
from dropdown import DropdownMenu
from helper import Helper
from tkinter import ttk, Toplevel
import customtkinter as tk
import os

class Interface:
    data = None

    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("320x220")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.helper = Helper()
        self.selectedMonths = []
        self.selectedCategories = []

        self.makeFrames()
        self.createWidgets()
        self.fillDropdown()
        self.loadGUI()


    '''UI Functions'''
    def createWidgets(self):
        self.fileLabel = tk.CTkLabel(self.fileSelectionFrame, text="Select a file to analyse:")
        self.fileDropdown = tk.CTkComboBox(self.fileSelectionFrame, state="readonly")
        self.loadButton = tk.CTkButton(self.fileSelectionFrame, text="Load File", command=self.loadFile)

        self.monthLabel = tk.CTkLabel(self.dataSelectionFrame, text="Months to display:")
        self.monthsDropdown = DropdownMenu(self.dataSelectionFrame, displayText="Months", options=self.helper.getAllMonths())

        self.categoryLabel = tk.CTkLabel(self.dataSelectionFrame, text="Categories to display:")
        self.categoryDropdown = DropdownMenu(self.dataSelectionFrame, displayText="Categories", options=self.helper.getAllCategories())

        self.analyzeButton = tk.CTkButton(self.analyzeFrame, text="Analyze", command=self.analyze)


    def loadGUI(self):
        self.fileLabel.pack(in_=self.fileSelectionFrame, padx=10, pady=5)
        self.fileDropdown.pack(in_=self.fileSelectionFrame, padx=10, pady=10)
        self.loadButton.pack(in_=self.fileSelectionFrame, padx=10, pady=10)

        self.monthLabel.pack(in_=self.dataSelectionFrame, padx=10, pady=5)
        self.monthsDropdown.button.pack(in_=self.dataSelectionFrame, padx=10, pady=10)

        self.categoryLabel.pack(in_=self.dataSelectionFrame, padx=10, pady=5)
        self.categoryDropdown.button.pack(in_=self.dataSelectionFrame, padx=10, pady=10)

        self.analyzeButton.pack(in_=self.analyzeFrame, padx=10, pady=10)


    def makeFrames(self):
        self.fileSelectionFrame = tk.CTkFrame(self.root)
        # self.fileSelectionFrame.pack(side="left", fill="both", expand=True)
        self.fileSelectionFrame.grid(row=0, column=0, sticky="nsew")

        self.dataSelectionFrame = tk.CTkFrame(self.root)
        # self.dataSelectionFrame.pack(side="left", fill="both", expand=True)
        self.dataSelectionFrame.grid(row=0, column=1, sticky="nsew")

        self.analyzeFrame = tk.CTkFrame(self.root)
        # self.analyzeFrame.pack(side="bottom", fill="both", expand=False)
        self.analyzeFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")


    def display_data_in_treeview(self, details, month, category):
        window = Toplevel(self.root)
        window.title(f"Purchases for {category} in {month}")
        window.geometry("800x400")

        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        # Define the Treeview with columns
        tree = ttk.Treeview(window, columns=('Price', 'Date', 'Place', 'Category'), show='headings')
        tree.heading('Price', text='Price')
        tree.heading('Date', text='Date')
        tree.heading('Place', text='Place')
        tree.heading('Category', text='Category')

        # Set font size for all columns using tags
        tree.tag_configure('big', font=('Arial', 16))

        # Insert each row into the Treeview and apply the 'big' tag to the rows
        for detail in details:
            price_with_currency = f"{detail[0]} BGN"
            tree.insert('', 'end', values=(price_with_currency, detail[1], detail[2], detail[3]), tags=('big',))

        # Add scrollbars
        horizontal_scrollbar = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=horizontal_scrollbar.set)
        horizontal_scrollbar.pack(side='bottom', fill='x')

        vertical_scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vertical_scrollbar.set)
        vertical_scrollbar.pack(side='right', fill='y')

        tree.pack(expand=True, fill='both', side='top')

        # Bind double-click and Enter key events to display the description
        tree.bind("<Double-1>", lambda event: on_row_select(event, tree, details))
        tree.bind("<Return>", lambda event: on_row_select(event, tree, details))

        # Track the window
        self.treeview_window = window
        self.description_windows = []

        def on_row_select(event, tree, details):
            selected_item = tree.selection()[0]
            index = tree.index(selected_item)
            description = details[index][4]  # Use the correct index for the description

            # Open the description window
            desc_window = Toplevel(self.root)
            desc_window.title("Description")
            desc_window.geometry("550x250")
            desc_label = tk.CTkLabel(
                desc_window,
                text=description,
                wraplength=380,
                justify='left',
                fg_color="black",  # Ensure black text
            )
            desc_label.pack(padx=10, pady=10, expand=True, fill='both')

            # Track the description window
            self.description_windows.append(desc_window)

        # Ensure all description windows are closed when the main treeview window is closed
        self.treeview_window.protocol("WM_DELETE_WINDOW", lambda: self.close_all_description_windows())


        # Close all description windows when the main window is closed
        def on_close():
            for desc_window in self.description_windows:
                desc_window.destroy()
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_close)




    '''Button and Data Functions'''

    def loadFile(self):
        self.selectedFile = self.fileDropdown.get()
        self.data = Data(self.selectedFile)

        self.data.df = self.data.reindex(self.data.df)  # reindexing data


    def analyze(self):
        self.selectedMonths = self.monthsDropdown.selectedValues
        self.selectedCategories = self.categoryDropdown.selectedValues

        if self.selectedFile:
            print(f"Analyzing for months: {self.selectedMonths}, categories: {self.selectedCategories}")
            purchases = self.getPurchases()

            self.visualiser = Visualiser(self.data)
            self.visualiser.plotFinances(purchases, onPick=self.display_data_in_treeview)
            
        else:
            print("SELECT FILE")


    '''Helper Functions'''        

    def getPurchases(self):
        purchases = self.helper.getSelectedCategories(self.selectedCategories, self.data)
        months = self.getSelectedMonths()[1]
        remove = []
        for i, j in enumerate(purchases):
            if not (int((purchases[i])[1].split(".")[1]) in months):
                remove.append(j)

        # Make purchase and remove lists sets, to get their disjunktion
        purchaseSet = set(map(tuple, purchases))
        removeSet = set(map(tuple, remove))

        purchases = list(map(list, purchaseSet.difference(removeSet))) # Get intersection and convert back to a list
        return purchases        

    def getSelectedMonths(self):
        # if self.monthsDropdown.get() == "All":
        if ("All" in self.selectedMonths) or not self.selectedMonths:
            months = self.helper.getAvailableMonths(self.data)
        else:
            months = self.selectedMonths
        
        if ("All" in self.selectedCategories) or self.selectedCategories == []:
            categories = self.helper.getAllCategories()
        else:
            categories = self.selectedCategories

        monthsDict = self.helper.getMonthsDictionary()

        monthIndexes = [monthsDict[month] for month in months if month in monthsDict]
        if not monthIndexes: monthIndexes = months
        
        return [categories, monthIndexes]

    def fillDropdown(self):
        files = [f for f in os.listdir("Finance Statements")]
        self.fileDropdown.configure(values=files)

        if files:
            self.fileDropdown.set(files[0])

    def on_close(self):
        # Ensure matplotlib window closes first
        if hasattr(self, 'visualiser'):
            self.visualiser.onClose()  # Close matplotlib window before Tkinter quits
        self.root.quit()  # Quit the Tkinter mainloop
        self.root.destroy()  # Destroy the Tkinter window