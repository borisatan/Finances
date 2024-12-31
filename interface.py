from data import Data
from data_visualiser import Visualiser
from dropdown import DropdownMenu
from helper import Helper
import customtkinter as tk
import os

class Interface:
    data = None

    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("320x220")

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


    def updateDataSelection(self, value):
        # Clear current widgets in dataSelectionFrame
        for widget in self.dataSelectionFrame.winfo_children():
            widget.pack_forget()

        self.monthLabel.pack(in_=self.dataSelectionFrame, padx=10, pady=5)

        self.categoryLabel.pack(in_=self.dataSelectionFrame, padx=10, pady=5)


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
            # self.makeBarChart()
            print(self.getPurchases())
        else:
            print("SELECT FILE")


    '''Helper Functions'''        

    def getPurchases(self):
        purchases = self.helper.getSelectedCategories(self.selectedCategories, self.data)
        months = self.getSelectedMonths()[1]
        remove = []

        for i, j in enumerate(purchases):
            # print(i)
            if int(purchases[i][1].split(".")[1]) not in months:
                remove.append(j)

        for i in remove:
            purchases.remove(i)
        return purchases        

    def getSelectedMonths(self):
        # if self.monthsDropdown.get() == "All":
        if "All" not in self.selectedMonths:
            months = self.selectedMonths
        else:
            months =  self.helper.getAvailableMonths()
        categories = self.selectedCategories if "All" not in self.selectedCategories else self.helper.getAllCategories()
        monthsDict = self.helper.getMonthsDictionary()
        monthIndexes = []

        monthIndexes = [monthsDict[month] for month in months if month in monthsDict]
        return [categories, monthIndexes]

    def makeBarChart(self):
        mC = self.getSelectedMonths()
        monthIndexes = mC[0]
        categories = mC[1]
        # Create a visualizer and plot the data
        self.visualiser = Visualiser(self.data)
        self.visualiser.plotMonths(monthIndexes, categories)


    def fillDropdown(self):
        files = [f for f in os.listdir("finance_statements")]
        self.fileDropdown.configure(values=files)

        if files:
            self.fileDropdown.set(files[0])

# TODO: Refactor everything around the getPuchases method