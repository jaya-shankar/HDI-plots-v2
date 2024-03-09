

class BaseModule:
    def create_plot(self, data, options):
        raise NotImplementedError("Subclasses must implement create_plot")

    def get_fig(self):
        raise NotImplementedError("Subclasses must implement get_fig")
    
    def save_plot(self,file_name = "chart.png"):
        raise NotImplementedError("Subclasses must implement save_plot")