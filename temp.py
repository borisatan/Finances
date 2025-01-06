import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import csv
import os

# Example data
purchases = [
    [-150, "20.10.2024", "media markt", "Tech"],
    [-170, "22.10.2024", "lidl", "Food"],
    [-170, "22.10.2024", "lidl", "Food"],
    [-200, "15.11.2024", "amazon", "Tech"],
    [-50, "10.11.2024", "lidl", "Food"]
]

# Track created CSV files
created_files = []

# Step 1: Group data by month and category
grouped_data = defaultdict(lambda: defaultdict(float))
purchase_details = defaultdict(list)  # For storing detailed purchases

for price, date_str, place, category in purchases:
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    month_year = date_obj.strftime("%Y-%m")
    grouped_data[month_year][category] += price
    purchase_details[(month_year, category)].append([price, date_str, place, category])

# Step 2: Prepare data for plotting
months = sorted(grouped_data.keys())
categories = sorted({category for month in grouped_data for category in grouped_data[month]})
data = {category: [grouped_data[month].get(category, 0) for month in months] for category in categories}

# Step 3: Plot the data
bar_width = 0.2
x = range(len(months))
fig, ax = plt.subplots(figsize=(10, 6))
bars = {}

for i, (category, values) in enumerate(data.items()):
    bars[category] = ax.bar(
        [pos + i * bar_width for pos in x],
        values,
        bar_width,
        label=category,
        picker=True
    )

ax.set_xlabel('Month')
ax.set_ylabel('Total Spent')
ax.set_title('Purchases by Month and Category')
ax.set_xticks([pos + (len(categories) - 1) * bar_width / 2 for pos in x])
ax.set_xticklabels(months)
ax.legend()

def on_pick(event):
    bar = event.artist
    x_positions = bar.get_x() + bar.get_width() / 2
    x_value = event.mouseevent.xdata
    index = (abs(x_positions - x_value)).argmin()
    category = next(cat for cat, bars_group in bars.items() if bar in bars_group)
    month = months[index]
    
    details = purchase_details[(month, category)]
    
    print(f"Purchases for {category} in {month}:")
    for detail in details:
        print(detail)
    filename = f"purchases_{category}_{month}.csv".replace(' ', '_')
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Price ", " Date ", " Place ", " Category"])
        for detail in details:
            # Adding a space between each value for readability
            writer.writerow([detail[0]] + [f" {value} " for value in detail[1:]])

    created_files.append(filename)
    print(f"Details saved to {filename}")

def on_close(event):
    for filename in created_files:
        try:
            os.remove(filename)
            print(f"Deleted file: {filename}")
        except OSError as e:
            print(f"Error deleting file {filename}: {e}")

fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('close_event', on_close)

plt.tight_layout()
plt.show()
