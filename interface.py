from data import Data
from data_visualiser import Visualiser
from dropdown import DropdownMenu
from helper import Helper
from tkinter import ttk, Toplevel, Label
import customtkinter as tk
from datetime import datetime
import os

class Interface:
    data = None

    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("320x220")
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)

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


    def displayDataInTreeview(self, details, month, category):
        window = Toplevel(self.root)
        window.title(f"Purchases for {category} in {month}")
        window.geometry("800x400")

        style = ttk.Style()

        # Configure the Treeview for dark mode
        style.configure("Treeview",
                        background="#2E2E2E",  # Dark background for rows
                        foreground="white",    # Light text for rows
                        rowheight=30,
                        fieldbackground="#2E2E2E")  # Dark background for field area
        style.map("Treeview", background=[('selected', '#4D4D4D')],  # Darker shade when selected
                foreground=[('selected', 'white')])

        # Configure the Treeview headers for dark mode
        style.configure("Treeview.Heading",
                        background="#333333",  # Dark background for headers
                        foreground="white",    # Light text for headers
                        font=('Arial', 12, 'bold'))

        tree = ttk.Treeview(window, columns=('Price', 'Date', 'Place', 'Category'), show='headings')
        tree.heading('Price', text='Price')
        tree.heading('Date', text='Date')
        tree.heading('Place', text='Place')
        tree.heading('Category', text='Category')

        tree.tag_configure('big', font=('Arial', 16))

        # Sort the details by the date field
        sorted_details = sorted(details, key=lambda x: datetime.strptime(x[1], '%d.%m.%Y'))  # Assuming 'YYYY-MM-DD' format

        for detail in sorted_details:
            priceWithCurrency = f"{detail[0]} BGN"
            tree.insert('', 'end', values=(priceWithCurrency, detail[1], detail[2], detail[3]), tags=('big',))

        horizontalScrollbar = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=horizontalScrollbar.set)
        horizontalScrollbar.pack(side='bottom', fill='x')

        verticalScrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=verticalScrollbar.set)
        verticalScrollbar.pack(side='right', fill='y')

        tree.pack(expand=True, fill='both', side='top')

        tree.bind("<Double-1>", lambda event: onRowSelect(event, tree, sorted_details))
        tree.bind("<Return>", lambda event: onRowSelect(event, tree, sorted_details))

        self.treeviewWindow = window
        self.descriptionWindows = []

        def onRowSelect(event, tree, details):
            selectedItem = tree.selection()[0]
            index = tree.index(selectedItem)
            description = details[index][4]

            descWindow = Toplevel(self.root)
            descWindow.title("Description")
            descWindow.geometry("600x250")
            descLabel = Label(
                descWindow,
                text=description,
                wraplength=550,
                justify='left',
                font=("Arial", 15),
                bg="#2E2E2E",
                fg='white'
            )
            descLabel.pack(padx=10, pady=10, expand=True, fill='both')

            self.descriptionWindows.append(descWindow)

        def onClose():
            for descWindow in self.descriptionWindows:
                descWindow.destroy()
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", onClose)




    '''Button and Data Functions'''

    def loadFile(self):
        self.selectedFile = self.fileDropdown.get()
        self.data = Data(self.selectedFile)

        self.data.df = self.data.reindex(self.data.df)  # reindexing data


    def analyze(self):
        self.selectedMonths = self.monthsDropdown.selectedValues
        self.selectedCategories = self.categoryDropdown.selectedValues

        if self.selectedFile:
            purchases = self.getPurchases()

            self.visualiser = Visualiser(self.data)
            self.visualiser.plotFinances(purchases, onPick=self.displayDataInTreeview)
            
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

    def onClose(self):
        # Ensure matplotlib window closes first
        if hasattr(self, 'visualiser'):
            self.visualiser.onClose()  # Close matplotlib window before Tkinter quits
        self.root.quit()  # Quit the Tkinter mainloop
        self.root.destroy()  # Destroy the Tkinter window