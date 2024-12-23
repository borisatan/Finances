import matplotlib.pyplot as plt

class Visualiser:
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots(figsize=(12, 8))  # Increase the figure size

    def plotMonths(self, months: list):
        # Get monthly expenses from the data
        monthly_expenses = self.data.getExpensesByMonth(months)

        # Prepare data for plotting
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        expenses = [monthly_expenses[month] for month in range(1, 13)]

        # Bar chart plotting
        self.ax.bar(months_list, expenses, color='blue')
        bars = self.ax.bar(months_list, expenses, color='blue')

        # Add labels and title
        self.ax.set_xlabel('Month', fontsize=14, labelpad=10)
        self.ax.set_ylabel('Expenses (BGN)', fontsize=14, labelpad=10)
        self.ax.set_title('Monthly Expenses', fontsize=16)

        # Rotate x-axis labels to avoid clipping
        self.ax.set_xticklabels(months_list, rotation=45, ha='right', fontsize=12)

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

        # Show the plot
        plt.show()
