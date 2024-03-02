

class BaseModule:
    def create_plot(self, data, options):
        raise NotImplementedError("Subclasses must implement create_plot")

    def get_fig(self):
        raise NotImplementedError("Subclasses must implement get_fig")