from visualizations.base_module import BaseModule
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class PlotlyModule(BaseModule):

    def __init__(self, subplots_count, vertical=False):
        if not vertical:
            rows, cols = self.calculate_subplots(subplots_count)
            self.fig = make_subplots(rows=rows, cols=cols, shared_xaxes=False)
        else:
            self.fig = make_subplots(rows=subplots_count, cols=1, shared_xaxes=False, row_heights=[10]*subplots_count)
            

        self.vertical = vertical
        self.subplots_count = subplots_count
        self.subplot_no = 0

    def calculate_subplots(self, subplots_count):
        if subplots_count == 2:
            return 1, 2
        elif subplots_count == 3:
            return 1, 3
        elif subplots_count == 4:
            return 2, 2
        else:
            return 1, 1

    def _get_plot_index(self, plot_no):
        if self.vertical:
            return (1, plot_no+1)
        else:
            if self.subplots_count <= 3:
                return (1, plot_no+1)
            else:
                return (plot_no // 2 + 1, plot_no % 2 + 1)

    def create_plot(self, data, xlabel, ylabel, dotted=False):
        
        rows, cols = self._get_plot_index(self.subplot_no)
        ax = self.fig
        for country, gender, coords in data:
            trace = go.Scatter(x=coords["x"], y=coords["y"], mode='lines', name=f"<b>{country}</b>-{gender}")
        
            ax.add_trace(trace, row=rows, col=cols)

        print(rows,cols)
        print(ylabel)
        ax.update_xaxes(title_text=xlabel, row=rows, col=cols)
        ax.update_yaxes(title_text=ylabel, row=rows, col=cols)

        ax.update_layout(
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            title=f"",
            showlegend=True if self.subplots_count == 4 else False,
            legend=dict(
                title="Legend",
                orientation="h",  # Set to "v" for vertical legend
                xanchor="left",
                yanchor="top",
                traceorder="normal",
                tracegroupgap=2  # Adjust this value as needed
            )
        )

        # trace = go.Scatter(x=data[0][2]["x"], y=data[0][2]["y"],
        #                    name=f"{data[0][0]} {data[0][1]}", line=dict(dash='dash' if dotted else 'solid'))

        # plot_index = self._get_plot_index(self.subplot_no)
        # print(plot_index)
        # self.fig.add_trace(trace, row=plot_index[0], col=plot_index[1])

        # self.fig.update_layout(title=f"{ylabel} vs {xlabel}")

        # s_y, e_y = min(data[0][2]["x"]), max(data[0][2]["x"])
        # gap = (e_y - s_y) // 6
        # if gap < 1:
        #     gap = 1
        # self.fig.update_xaxes(tickvals=list(range(int(s_y), int(e_y) + 1, gap)))

        # self.fig.update_layout(legend=dict(orientation="h"))

        self.subplot_no += 1

    def get_fig(self):
        return self.fig
