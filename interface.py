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
        self.root.geometry("300x300")

        self.makeFrames()
        self.createWidgets()
        self.fillDropdown()
        self.loadGUI()

    def createWidgets(self):
        self.fileLabel = tk.CTkLabel(self.fileSelectionFrame, text="Select a file to analyse:")
        self.fileDropdown = tk.CTkComboBox(self.fileSelectionFrame, state="readonly")
        self.loadButton = tk.CTkButton(self.fileSelectionFrame, text="Load File", command=self.loadFile)

        # Removed month range selection since it's no longer needed
        self.analyzeButton = tk.CTkButton(self.fileSelectionFrame, text="Analyze", command=self.analyze)

    def loadGUI(self):
        self.fileLabel.pack(in_=self.fileSelectionFrame, pady=5)
        self.fileDropdown.pack(in_=self.fileSelectionFrame, pady=5)
        self.loadButton.pack(in_=self.fileSelectionFrame, pady=10)

        self.analyzeButton.pack(in_=self.fileSelectionFrame, pady=10)

    def loadFile(self):
        self.selectedFile = self.fileDropdown.get()
        self.data = Data(self.selectedFile)

        # Clean the data
        self.data.removeNanRows()
        self.data.df = self.data.reindex(self.data.df)  # reindexing data
        self.data.makeCategories()

    def analyze(self):
        if self.selectedFile:
            self.makeBarChart()  # Show data for all months present in the file
        else:
            print("SELECT FILE")

    def makeBarChart(self):
        months = self.getAvailableMonths()

        # Create a visualizer and plot the data
        self.visualiser = Visualiser(self.data)
        self.visualiser.plotMonths(months)

    def makeFrames(self):
        self.fileSelectionFrame = tk.CTkFrame(self.root)
        self.fileSelectionFrame.pack(fill="both", expand=True)

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



# TODO: Find a way to display the data       
# TODO: When sorting by month the original dataframe gets messed up