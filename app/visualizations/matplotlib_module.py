import matplotlib.pyplot as plt
from .base_module import BaseModule
from matplotlib.axes import Axes

class MatplotlibModule(BaseModule):
    
    def __init__(self,subplots_count, vertical=False):
        
        fig, ax = plt.subplots(1, 1)
        if(not vertical):
            if(subplots_count == 2):
                fig, ax = plt.subplots(1, 2, figsize=(10, 4))
            elif(subplots_count == 3):
                fig, ax = plt.subplots(1, 3, figsize=(15, 4))
            elif(subplots_count == 4):
                fig, ax = plt.subplots(2, 2, figsize=(10, 10))
        else:
            fig, ax = plt.subplots(subplots_count, 1, figsize=(5, 5*subplots_count))    
        
        self.vertical = vertical
        self.subplots_count = subplots_count
        self.subplot_no = 0
        self.fig = fig
        self.ax = ax
        
        pass

    def _get_plot_index(self, plot_no: int) -> int:
        if(self.vertical):
            return plot_no
        else:
            if (self.subplots_count<=3):
                return plot_no
            else:
                return plot_no//2, plot_no%2
            
    def create_plot(self, data: list[tuple], xlabel: str, ylabel: str, dotted: bool = False) -> None:
        
        ax: Axes = self.ax
        if(self.subplots_count>1):
            ax = self.ax[self._get_plot_index(self.subplot_no)]
        for country,gender,coords in data:
            ax.plot(coords["x"], coords["y"] ,label=f"{country} {gender}", linestyle='dotted' if dotted else None)

        ax.set_title(f"{ylabel} vs {xlabel}")
        
        # s_y,e_y = min(data[0][2]["x"]), max(data[0][2]["x"])
        # gap = (e_y-s_y)//6 
        # if(gap<1):
        #     gap = 1
        # ax.set_xticks(range(int(s_y), int(e_y) + 1, gap))
        
        ax.legend()
        self.subplot_no += 1
    
    def save_plot(self,file_name = "chart.png"):
        self.fig.savefig(file_name)
    def reduce_subplot_no(self):
        self.subplot_no -= 1
        
    def get_fig(self):
        return self.fig