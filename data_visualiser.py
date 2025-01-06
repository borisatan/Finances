import matplotlib.pyplot as plt

class Visualiser:
    def __init__(self, data):
        self.data = data

        plt.style.use("fivethirtyeight")
        self.fig, self.ax = plt.subplots(figsize=(12, 8))  


    def plotCategories(self):
        return    
    
    
    def makeBarColors(self, expenses):
        biggestExpense = expenses[0]

        for exp in expenses:
            if exp > biggestExpense:
                biggestExpense = exp

        colors = []

        for i in expenses:
            percent = 1 / (biggestExpense / i)
            if percent > 0.75:  # Highest range (close to biggestExpense)
                colors.append("crimson")
            elif percent > 0.5:  # Middle range
                colors.append("darkorange")
            elif percent > 0.25:  # Lower middle range
                colors.append("gold")
            elif percent > 0:  # Smallest range
                colors.append("forestgreen")
            else:
                colors.append("cyan")    
        
        return colors


        # Calculate colors based on percentages

    def prepareBarData(self, months: list, purchases : list):
        monthlyExpenses = self.data.getExpensesByMonth(months)
        print(purchases, "prepBarVis")

        self.monthsList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.expenses = [monthlyExpenses.get(month, 0) for month in range(1, 13)]  # Get expenses, defaulting to 0 if missing
        # print(self.expenses)

        # Collect months to remove (those with 0 expense)
        monthsToRemove = [month for month in range(1, 13) if monthlyExpenses.get(month, 0) == 0]
        for month in reversed(monthsToRemove):    
            del monthlyExpenses[month]  
            self.monthsList.pop(month - 1)

        # Prepare the expenses list after filtering out 0 values
        self.expenses = [monthlyExpenses[month] for month in range(1, 13) if month in monthlyExpenses]



    def plotMonths(self, months: list, purchases : list):
        plt.style.use("fivethirtyeight")

        self.prepareBarData(months, purchases)
        barColors = self.makeBarColors(self.expenses)
            
        # Bar chart plotting
        self.ax.bar(self.monthsList, self.expenses, color=barColors)
        bars = self.ax.bar(self.monthsList, self.expenses, color=barColors)

        # Add labels and title
        self.ax.set_xlabel('Month', fontsize=14, fontweight="bold", labelpad=10)
        self.ax.set_ylabel('Expenses (BGN)', fontsize=14, fontweight="bold", labelpad=10)
        self.ax.set_title('Monthly Expenses', fontweight="bold", fontsize=16)

        # Rotate x-axis labels to avoid clipping
        self.ax.set_xticks(range(len(self.monthsList)))
        self.ax.set_xticklabels(self.monthsList, rotation=45, ha='right', fontsize=12)

        for bar in bars:
            yval = bar.get_height()  # Get the height of the bar (expense value)
            labelOffset = 5 if yval > 0 else -5
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,  # X position (middle of the bar)
                (yval + labelOffset),  # Y position (slightly above the bar)
                f'{yval:.2f}',  # Format the label to show two decimal places
                ha='center',  # Center the label horizontally
                va='bottom' if yval > 0 else 'top',  # Position the label above the bar
                fontsize=12
            )

        # Ensure the layout is tight to prevent clipping
        plt.tight_layout()
        plt.show()