from data import Data
from data_visualiser import Visualiser
from dropdown import DropdownMenu
import customtkinter as tk
import os

class Interface:
    data = None

    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("320x220")

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
        self.monthsDropdown = DropdownMenu(self.dataSelectionFrame, displayText="Months", options=self.getAllMonths())

        self.categoryLabel = tk.CTkLabel(self.dataSelectionFrame, text="Categories to display:")
        self.categoryDropdown = DropdownMenu(self.dataSelectionFrame, displayText="Categories", options=self.getAllCategories())

        self.analyzeButton = tk.CTkButton(self.analyzeFrame, text="Analyze", command=self.analyze)


    def loadGUI(self):
        self.fileLabel.pack(in_=self.fileSelectionFrame, padx=10, pady=5)
        self.fileDropdown.pack(in_=self.fileSelectionFrame, padx=10, pady=10)
        self.loadButton.pack(in_=self.fileSelectionFrame, padx=10, pady=10)

        self.monthLabel.pack(in_=self.dataSelectionFrame, padx=10, pady=5)

        self.categoryLabel.pack(in_=self.dataSelectionFrame, padx=10, pady=5)

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


    '''Button Functions'''

    def loadFile(self):
        self.selectedFile = self.fileDropdown.get()
        self.data = Data(self.selectedFile)

        self.data.df = self.data.reindex(self.data.df)  # reindexing data
        print(self.data.df)

    def analyze(self):
        self.selectedMonths = self.monthsDropdown.selectedValues
        self.selectedCategories = self.categoryDropdown.selectedValues

        if self.selectedFile:
            print(f"Analyzing for months: {self.selectedMonths}, categories: {self.selectedCategories}")
            self.makeBarChart()
        else:
            print("SELECT FILE")



    '''Helper Functions'''        

    def makeBarChart(self):
        # if self.monthsDropdown.get() == "All":
        months = self.selectedMonths if "All" not in self.selectedMonths else self.getAvailableMonths()


        # Create a visualizer and plot the data
        self.visualiser = Visualiser(self.data)
        self.visualiser.plotMonths(months)

    def getAvailableMonths(self):
        # Get the months available in the file
        availableMonths = self.data.df["Date"].apply(lambda x: x.split(".")[1]).unique()
        availableMonths = sorted(map(int, availableMonths))  # Sort months numerically
        return availableMonths

    def fillDropdown(self):
        files = [f for f in os.listdir("finance_statements")]
        self.fileDropdown.configure(values=files)

        if files:
            self.fileDropdown.set(files[0])

    def getAllMonths(self):
        return ["All", "Jan", "Feb", 'Mar', "Apr", 'May', "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def getAllCategories(self):
        return [
        "All",
        "Food", 
        "Furnitare",
        "Tech", 
        "Drugs",
        "Transport",
        "Flights", 
        "Music", 
        "Shopping",
        "Gas" ,
        "Others"]
    

# TODO: When sorting by month the original dataframe gets messed up