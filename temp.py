import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Initialize customtkinter
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CustomTkinter with Matplotlib")
        self.geometry("800x600")

        # Create a CTkFrame to hold the Matplotlib chart
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Call the function to add a chart
        self.add_chart(self.chart_frame)

    def add_chart(self, parent):
        # Create a Matplotlib figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Example plot
        x = [0, 1, 2, 3, 4, 5]
        y = [0, 1, 4, 9, 16, 25]
        ax.plot(x, y, label="y = x^2")
        ax.set_title("Matplotlib Chart in CustomTkinter")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.legend()

        # Embed the Matplotlib figure into the CustomTkinter frame
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        # Draw the canvas
        canvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()
