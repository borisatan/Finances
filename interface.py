from data import Data
from data_visualiser import Visualiser
import customtkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class Interface:
    data = None
    
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("600x600")

        self.makeFrames()
        self.createWidgets()
        self.fillDropdown()
        self.loadGUI()

    def createWidgets(self):
        self.fileLabel = tk.CTkLabel(self.fileSelectionFrame, text="Select a file to analyse:")
        self.fileDropdown = tk.CTkComboBox(self.fileSelectionFrame, state="readonly")
        self.loadButton = tk.CTkButton(self.fileSelectionFrame, text="Load File", command=self.loadFile)

        self.monthLabel = tk.CTkLabel(self.monthSelectionFrame, text="Select Month Range:")

        self.startMonth = tk.CTkComboBox(self.monthSelectionFrame, state="readonly", values=self.getMonths())
        self.startMonth.set("Start Month")

        self.endMonth = tk.CTkComboBox(self.monthSelectionFrame, state="readonly", values=self.getMonths())
        self.endMonth.set("End Month")

        self.analyzeButton = tk.CTkButton(self.monthSelectionFrame, text="Analyze", command=self.analyze)
        

    def loadGUI(self):

        # First three widgets in the first frame (vertically aligned)
        self.fileLabel.pack(in_=self.fileSelectionFrame, pady=5)
        self.fileDropdown.pack(in_=self.fileSelectionFrame, pady=5)
        self.loadButton.pack(in_=self.fileSelectionFrame, pady=10)

        self.startMonth.pack(in_=self.monthSelectionFrame, pady=5)
        self.endMonth.pack(in_=self.monthSelectionFrame, pady=5)
        self.analyzeButton.pack(in_=self.monthSelectionFrame, pady=10)


    def loadFile(self):
        self.selectedFile = self.fileDropdown.get()
        self.data = Data(self.selectedFile)

        self.data.removeNanRows()
        self.data.df = self.data.reindex(self.data.df) # reindexing data
        self.data.makeCategories()
        self.data.printCategories([])

    def analyze(self):
        startMonth = self.startMonth.get()
        endMonth = self.endMonth.get()
        monthsMap = {}

        months = self.getMonths()
        for i, element in enumerate(months):
            monthsMap[element] = i + 1

        if self.selectedFile and startMonth == "Start Month" and endMonth == "End Month":
            return # all months
            # self.data.sortByMonth([])
            # self.data.printCategories([])
        
        elif self.selectedFile and startMonth != "Start Month" and endMonth != "End Month":
            start = monthsMap[startMonth] # gets all values, need to make start and end
            end = monthsMap[endMonth] # gets all values, need to make start and end

            # self.data.sortByMonth([start, end])
            self.makeBarChartMonths([start, end])

    def makeBarChartMonths(self, months: list): # [start, end]
        self.visualiser = Visualiser(self.data)
        self.visualiser.plotMonths(months)

        self.barCanvas = FigureCanvasTkAgg(self.visualiser.fig, master=self.barPlotFrame)
        self.barCanvasWidget = self.barCanvas.get_tk_widget()
        self.barCanvasWidget.pack(fill="both", expand=True)
        self.barCanvas.draw()

    def makeFrames(self):
        self.fileSelectionFrame = tk.CTkFrame(self.root)
        self.fileSelectionFrame.grid(row=0, column=0, padx=10, pady=10)

        self.monthSelectionFrame = tk.CTkFrame(self.root)
        self.monthSelectionFrame.grid(row=0, column=1, padx=10, pady=10)

        self.barPlotFrame = tk.CTkFrame(self.root)
        self.barPlotFrame.grid(row=1, column=0, padx=10, pady=10)

    def getMonths(self):
        return ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]    

    def fillDropdown(self):
        # GET FILES FROM FINANCE STATEMENTS FOLDER
        files = [f for f in os.listdir("finance_statements")] 
        self.fileDropdown.configure(values=files)

        if files:
            self.fileDropdown.set(files[0])    



# TODO: Find a way to display the data       
# TODO: When sorting by month the original dataframe gets messed up