import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
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

    def plotFinances(self, purchases, onPick=None):
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

        # Adjust figure size dynamically based on data size
        fig_width = max(12, len(self.months) * len(categories) * 0.5)
        fig_height = max(8, len(categories) * 0.5)
        self.fig, self.ax = plt.subplots(figsize=(fig_width, fig_height))

        # Set up bar chart parameters
        try:
            barWidth = 0.8 / len(categories)  # Adjust bar width based on number of categories
        except ZeroDivisionError:
            print("No categories given")

        x = range(len(self.months))
        self.bars = {}

        # Generate a color map with enough unique colors
        cmap = cm.get_cmap('Set1', len(categories))  # 'tab20' provides 20 distinct colors

        # Plot a bar for each category
        for i, (category, values) in enumerate(data.items()):
            color = cmap(i)  # Get a unique color from the colormap
            bar_positions = [pos + (i - len(categories) / 2) * barWidth + barWidth / 2 for pos in x]
            self.bars[category] = self.ax.bar(
                bar_positions,
                values,
                barWidth,
                label=category,
                color = color,
                picker=True
            )
            # Add labels to each bar
            for pos, value in zip(bar_positions, values):
                y_offset = -5 if value < 0 else 5  # Offset below for negative, above for positive
                self.ax.text(
                    pos,
                    value + y_offset,
                    f'{int(value)}',  # Display integer values
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

        self.fig.canvas.mpl_connect('pick_event', lambda event: self.onPick(event, onPick))
        self.fig.canvas.mpl_connect('close_event', self.onClose)

        # Adjust window size and position
        mng = plt.get_current_fig_manager()
        if hasattr(mng, 'window') and hasattr(mng.window, 'wm_geometry'):
            window_size = f"{int(fig_width * 80)}x{int(fig_height * 80)}+100+100"
            mng.window.wm_geometry(window_size)

        plt.tight_layout()
        plt.show()


    def onPick(self, event, onPick):
        bar = event.artist

        for category, barsGroup in self.bars.items():
            if bar in barsGroup:
                index = barsGroup.index(bar)
                selected_category = category
                break

        month = self.months[index]
        details = self.purchaseDetails[(month, selected_category)]

        if onPick:
            onPick(details, month, selected_category)

    def onClose(self, event=None):
        # Handle close event to clean up created files
        if self.fig:
            plt.close(self.fig)

        for filename in self.createdFiles:
            try:
                os.remove(filename)
                print(f"Deleted file: {filename}")
            except OSError as e:
                print(f"Error deleting file {filename}: {e}")
