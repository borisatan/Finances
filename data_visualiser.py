import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import currency_converter
import csv
import os

class Visualiser:
    def __init__(self, data):
        self.data = data
        self.currencyConverter = currency_converter.CurrencyConverter()

        plt.style.use("fivethirtyeight")
        self.fig, self.ax = plt.subplots(figsize=(12, 8))  # Initialize a larger figure size

    def plotFinances(self, purchases):
        # Track created CSV files
        self.createdFiles = []

        # Group data by month and category
        groupedData = defaultdict(lambda: defaultdict(float))
        self.purchaseDetails = defaultdict(list)  # For storing detailed purchases

        for price, dateStr, place, category, description in purchases:
            price *= -1

            dateObj = datetime.strptime(dateStr, "%d.%m.%Y")
            monthYear = dateObj.strftime("%Y-%m")
            groupedData[monthYear][category] += price
            self.purchaseDetails[(monthYear, category)].append([price, dateStr, place, category, description])

        # Prepare data for plotting
        self.months = sorted(groupedData.keys())
        categories = sorted({category for month in groupedData for category in groupedData[month]})
        data = {category: [groupedData[month].get(category, 0) for month in self.months] for category in categories}

        # Set up bar chart parameters
        try: barWidth = 0.8 / len(categories)  # Adjust bar width based on number of categories
        except ZeroDivisionError: print("No categories given")     

        x = range(len(self.months))
        self.bars = {}

        # Plot a bar for each category
        for i, (category, values) in enumerate(data.items()):
            bar_positions = [pos + (i - len(categories)/2) * barWidth + barWidth/2 for pos in x]
            self.bars[category] = self.ax.bar(
                bar_positions,
                values,
                barWidth,
                label=category,
                picker=True
            )
            # Add labels to each bar
            for pos, value in zip(bar_positions, values):
                y_offset = -5 if value < 0 else 5  # Offset below for negative, above for positive
                self.ax.text(
                    pos,
                    value + y_offset,
                    f'{value:.2f}',
                    ha='center',
                    va='bottom' if value > 0 else 'top',
                    fontsize=9,
                    color='black'
                )

        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('Total Spent')
        self.ax.set_title('Purchases by Month and Category')
        self.ax.set_xticks([pos + barWidth * (len(categories) - 1) / 2 for pos in x])
        self.ax.set_xticklabels(self.months)
        self.ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

        self.fig.canvas.mpl_connect('pick_event', self.onPick)
        self.fig.canvas.mpl_connect('close_event', self.onClose)

        plt.tight_layout()
        plt.show()

    def onPick(self, event):
        # Handle pick event when a bar is clicked
        bar = event.artist
        xValue = event.mouseevent.xdata
        
        # Find the correct bar group and corresponding month index
        for category, barsGroup in self.bars.items():
            if bar in barsGroup:
                index = barsGroup.index(bar)
                selected_category = category
                break
                
        month = self.months[index]
        
        # Retrieve and display purchase details
        details = self.purchaseDetails[(month, selected_category)]
        print(f"Purchases for {selected_category} in {month}:")
        for detail in details:
            print(detail)
        
        # Ensure the directory exists
        directory = "Category Statements"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create and write to the CSV file
        filename = os.path.join(directory, f"purchases_{selected_category}_{month}.csv".replace(' ', '_'))
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Price", "Date", "Place", "Category", "Description"])
            writer.writerows(details)
        
        self.createdFiles.append(filename)
        print(f"Details saved to {filename}")

    def onClose(self, event):
        # Handle close event to clean up created files
        for filename in self.createdFiles:
            try:
                os.remove(filename)
                print(f"Deleted file: {filename}")
            except OSError as e:
                print(f"Error deleting file {filename}: {e}")
