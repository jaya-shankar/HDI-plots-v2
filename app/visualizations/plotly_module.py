def plot_line_chart(ax, all_coords, selected_x, selected_y, title):
    for country, gender, coords in all_coords:
        ax.add_trace(go.Scatter(x=coords["x"], y=coords["y"], mode='lines', name=f"<b>{country}</b>-{gender}"))

    ax.update_layout(
        xaxis_title=selected_x,
        yaxis_title=selected_y,
        title=title,
        showlegend=True,
        legend=dict(
            title="Legend",
            orientation="h",  # Set to "v" for vertical legend
            xanchor="left",
            yanchor="top"
        )
    )

