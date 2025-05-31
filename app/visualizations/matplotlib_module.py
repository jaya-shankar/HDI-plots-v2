import matplotlib.pyplot as plt
from .base_module import BaseModule
from matplotlib.axes import Axes

class MatplotlibModule(BaseModule):

    def __init__(self, subplots_count, vertical=False):
        # Standard colors from matplotlib color cycle
        self.color_cycle = [
            '#1f77b4',  # Blue
            '#ff7f0e',  # Orange
            '#2ca02c',  # Green
            '#d62728',  # Red
            '#9467bd',  # Purple
            '#8c564b',  # Brown
            '#e377c2',  # Pink
            '#7f7f7f',  # Gray
            '#bcbd22',  # Yellow-green
            '#17becf'   # Cyan
        ]
        self.entity_colors = {}
        self.next_color_idx = 0

        fig, ax = plt.subplots(1, 1)
        if not vertical:
            if subplots_count == 2:
                fig, ax = plt.subplots(1, 2, figsize=(10, 4))
            elif subplots_count == 3:
                fig, ax = plt.subplots(1, 3, figsize=(15, 4))
            elif subplots_count == 4:
                fig, ax = plt.subplots(2, 2, figsize=(10, 10))
        else:
            fig, ax = plt.subplots(subplots_count, 1, figsize=(5, 5*subplots_count))

        self.vertical = vertical
        self.subplots_count = subplots_count
        self.subplot_no = 0
        self.fig = fig
        self.ax = ax

    def _get_plot_index(self, plot_no: int) -> int:
        if self.vertical:
            return plot_no
        if self.subplots_count <= 3:
            return plot_no
        return     plot_no//2, plot_no%2

    def create_plot(self, data: list[tuple], xlabel: str, ylabel: str, dotted: bool = False) -> None:
        # Check if data is empty
        if not data:
            self.subplot_no += 1
            return

        # Get the correct Axes object based on subplot count
        if self.subplots_count == 1:
            ax = self.ax
        else:
            if hasattr(self.ax, 'flat'):
                # This handles both 2D arrays (like in 2x2 grid) and 1D arrays
                ax = self.ax.flat[self.subplot_no] if self.subplot_no < len(self.ax.flat) else self.ax
            else:
                # This handles cases where we have a 1D array of axes
                if isinstance(self.ax, (list, tuple)):
                    ax = self.ax[self.subplot_no] 
                else:
                    # Single axes object
                    ax = self.ax
            
        for country, gender, coords in data:
            # Get or assign a consistent color for this entity
            if country not in self.entity_colors:
                self.entity_colors[country] = self.color_cycle[self.next_color_idx]
                self.next_color_idx = (self.next_color_idx + 1) % len(self.color_cycle)
            
            ax.plot(coords["x"], coords["y"], 
                   label=f"{country} {gender}", 
                   color=self.entity_colors[country],
                   linestyle='dotted' if dotted else None)

        self.next_color_idx = 0

        ax.set_title(f"{ylabel} vs {xlabel}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        handles, labels = ax.get_legend_handles_labels()
        if handles:  # Only add legend if there are any labels
            sorted_labels_handles = sorted(zip(labels, handles), key=lambda x: x[0])
            labels, handles = zip(*sorted_labels_handles)
            ax.legend(handles, labels)
        
        self.subplot_no += 1
    
    def save_plot(self, file_name: str = "chart.png"):
        self.fig.savefig(file_name)

    def reduce_subplot_no(self):
        self.subplot_no -= 1

    def get_fig(self):
        return self.fig
