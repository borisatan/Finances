from data import Data
import matplotlib.pyplot as plt
import pandas as pd

class Visualiser():

    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()


    def plotMonths(self, months):
        dataDF = self.data.sortByMonth(months)
        plt.style.use("classic")

        # months = ["Jan", "Feb", "Oct"] # LIST OF MONTHS TO DISPLAY
        expenses = [400, 350, 300] # list of expenses for each month
        colors = ["limegreen", "yellow", "crimson"] # need to change them conditionally

        self.barDF = pd.DataFrame({"months": months, "expenses": expenses}) # df to display in bar chart

        self.ax.bar(self.barDF["months"], self.barDF["expenses"], color=colors, edgecolor="black")
        
        # chart settings
        self.ax.set_facecolor("#121212")
        plt.title('Expenses by month')
        plt.xlabel('Months')
        plt.ylabel('Amount spent')
        plt.show()
    