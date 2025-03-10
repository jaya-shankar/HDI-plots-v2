# pyright: reportMissingModuleSource=false
# pyright: reportMissingImports=false
import streamlit as st
import pandas as pd
import app.constants as constants
from app.utils import (
    get_country_coords,
    get_state_coords,
    save_csv,
    get_countries,
    get_indian_states
)

from app.visualizations.matplotlib_module import MatplotlibModule

# XXX TODO set world in params
def get_world_state(params):
    """Initialize the app state"""
    if "world" not in st.session_state:
           st.session_state["world"] = True
    if "world" in params:
           st.session_state["world"] = True if params.get("world")[0] == "true" else False
    return st.session_state["world"]

def get_countries_and_states():
    """Get the list of countries and states"""
    countries     = get_countries()
    indian_states = get_indian_states()
    return countries, indian_states

def get_indices():
    """Get the education indices"""
    indices       = constants.edu_indices
    india_indices = constants.india_edu_indices
    return indices, india_indices

def get_query_params():
    """Get the query parameters"""
    params = st.query_params.to_dict()
    for k, v in params.items():
        params[k] = v.split(",")
    return params

def get_selected_options(params):
    """Get the selected options from the query parameters"""
    selected_options = params.get("gender", [])
    selected_other_indicators = params.get("other", [])
    if len(selected_options) == 0:
        selected_options = ["Female"]
    return selected_options, selected_other_indicators

def get_selected_x_and_y(params, indices):
    """Get the selected x and y values from the query parameters"""
    selected_x, selected_y = indices[0], indices[1]
    try:
        selected_x = constants.cleaned_indices[params.get("x", indices)[0]]
    except:
        pass
    try:
        selected_y = constants.cleaned_indices[params.get("y", indices)[0]]
    except:
        pass
    return selected_x, selected_y

def get_selected_countries_and_states(params, world, countries, indian_states):

    """Get the selected countries and states from the query parameters"""

    selected_countries = []
    selected_states    = []

    if world:
        selected_countries = params.get("c", ["India"])
    else:
        selected_states = params.get("s", ["Kerala"])

    return selected_countries, selected_states

def set_page_config():
    """Set the page configuration"""
    st.set_page_config(
        page_title="HDI Plots",
        page_icon="🌏",  # Replace this with your desired icon emoji or path to an icon image
        layout="centered",  # Optional: Set the layout style (wide, center, or fullscreen)
    )

def main():
    """Main function"""
    params                   = get_query_params()
    world                    = get_world_state(params)
    countries, indian_states = get_countries_and_states()
    indices, india_indices   = get_indices()
    selected_options, selected_other_indicators = get_selected_options(params)
    selected_x, selected_y   = get_selected_x_and_y(params, indices)

    selected_countries, selected_states = get_selected_countries_and_states(params, world, countries, indian_states)

    set_page_config()
    st.markdown(constants.custom_style, unsafe_allow_html=True)


    cleaned_indices_reversed = {v: k for k, v in constants.cleaned_indices.items()}

    # Create a function to plot using Plotly
    selected_options = []
    selected_ys      = []



    selected_options       = params.get("gender", [])
    selected_other_indicators = params.get("other", [])
    if len(selected_options) == 0:
        selected_options   = ["Female"]
    selected_x, selected_y = indices[0], indices[1]
    try:
        selected_x = constants.cleaned_indices[params.get("x", indices)[0]]
    except:
        pass

    try:
        selected_y = constants.cleaned_indices[params.get("y", indices)[0]]
    except:
        pass

    try:
        start_year = int(params.get("sy", [1960])[0])
    except:
        start_year = 1960
    try:
        end_year   = int(params.get("ey", [2020])[0])
    except:
        end_year   = 2020

    try:
        vertical_view = params.get("vertical", ["false"])[0].lower() == "true"
    except:
        vertical_view = False



    st.title("Plots 🌎")

    col1, col2 = st.columns(2)

    if col1.button("World", type = "primary" if world else "secondary", key="world_button"):
        st.query_params["world"] = "true"
        world                    = True
        st.rerun()

    if col2.button("India", type = "primary" if not world else "secondary", key = "india_button"):
        st.query_params["world"] = "false"
        world                    = False
        st.rerun()

    col1, col2 = st.columns(2)
    if world:
        if selected_y not in indices:
            selected_y = indices[0]
        selected_y     = col1.selectbox("Select y axis", indices, index=indices.index(selected_y), key="y_axis_selectbox")

        selected_x     = col2.selectbox("Select x axis",  constants.time_indices, index=0, disabled=True, key="x_axis_selectbox")
    else:
        if selected_y not in india_indices:
            selected_y = india_indices[0]
        selected_y     = col1.selectbox("Select y axis", india_indices, index=india_indices.index(selected_y), key="y_axis_selectbox_india")
        selected_x     = col2.selectbox("Select x axis", constants. time_indices, index=0, disabled=True, key="x_axis_selectbox_india")

    if world:
        if selected_y in constants.edu_indices:

            col1, col2, col3 = st.columns(3)
            options = ['Both', 'Male', 'Female']

            checkbox_state1 = col1.checkbox(options[0],value = options[0] in selected_options, key = "both_checkbox_world")
            checkbox_state2 = col2.checkbox(options[1],value = options[1] in selected_options, key = "male_checkbox_world")
            checkbox_state3 = col3.checkbox(options[2],value = options[2] in selected_options, key = "female_checkbox_world")

            for i,checkbox in enumerate([checkbox_state1, checkbox_state2, checkbox_state3]):
                if checkbox:
                    selected_options.append(options[i])
                elif options[i] in selected_options and not checkbox:
                    selected_options.remove(options[i])

            selected_options = list(set(selected_options))
            for selected_option in selected_options:
                selected_ys.append((selected_option + " " + selected_y,selected_option))
            st.write(selected_y)
        else:
            selected_ys.append((selected_y,""))

        if selected_x in constants.edu_indices:
            selected_x = "Both " + selected_x
        # Add a dropdown box to select a country
        try:
            selected_countries = selected_countries.remove("")
        except:
            pass
        try:
            selected_states = selected_states.remove("")
        except:
            pass

        selected_countries = st.multiselect("Select Countries", countries, default=selected_countries, key = "countries_multiselect")
        selected_states = st.multiselect("Select Indian States", indian_states, default=selected_states, key = "states_multiselect_world")

        selected_years  = st.slider("Select years", min_value = 1960, max_value=2020, value=(start_year, end_year), key = "years_slider")

    else:

        col1, col2, col3 = st.columns(3)
        options = ['Both', 'Male', 'Female']

        checkbox_state1 = col1.checkbox(options[0],value = options[0] in selected_options, key = "both_checkbox_india")
        checkbox_state2 = col2.checkbox(options[1],value = options[1] in selected_options, key = "male_checkbox_india")
        checkbox_state3 = col3.checkbox(options[2],value = options[2] in selected_options, key = "female_checkbox_india")

        for i,checkbox in enumerate([checkbox_state1, checkbox_state2, checkbox_state3]):
            if checkbox:
                selected_options.append(options[i])
            elif options[i] in selected_options and not checkbox:
                selected_options.remove(options[i])

        selected_options = list(set(selected_options))
        for selected_option in selected_options:
            selected_ys.append((selected_option + " " + selected_y,selected_option))
        st.write(selected_y)
        # checkbox_state3 = col3.checkbox(options[2],value = options[2] in selected_options)

        selected_states = st.multiselect("Select States", indian_states, selected_states, key = "states_multiselect_india")

    col1, col2, col3 = st.columns(3)
    other_indicators = ['Life Expectancy', 'Total Fertility Rate', 'GDP per Capita']

    # Single vertical view checkbox with unique key
    vertical_view = st.checkbox(
        "Vertical View",
        value=vertical_view,
        key="vertical_view_checkbox"
    )


    le_indicator  = col1.checkbox(other_indicators[0],value = other_indicators[0] in selected_other_indicators, key = "le_checkbox")
    tfr_indicator = col2.checkbox(other_indicators[1],value = other_indicators[1] in selected_other_indicators, key = "tfr_checkbox")
    gdp_indicator = col3.checkbox(other_indicators[2],value = other_indicators[2] in selected_other_indicators, key = "gdp_checkbox")
    for i,checkbox in enumerate([le_indicator, tfr_indicator, gdp_indicator]):
        if checkbox:
            selected_other_indicators.append(other_indicators[i])
        elif other_indicators[i] in selected_other_indicators and not checkbox:
            selected_other_indicators.remove(other_indicators[i])

    selected_other_indicators = list(set(selected_other_indicators))

    # plot the line chart using Matplotlib
    rows = 1
    edu_indicator = True
    if le_indicator:
        rows += 1
    if tfr_indicator:
        rows += 1
    if gdp_indicator:
        rows += 1

    plotter = MatplotlibModule(rows, vertical=vertical_view)

    country_coords = None


    all_coords = []
# XXX TODO sort by name only
    if world:

        if edu_indicator:
            all_coords = []

            if len(selected_states) > 0:
                for selected_state in selected_states:
                    for selected_y_t,gender in selected_ys:
                        state_coords = get_state_coords(selected_state, selected_y_t)
                        all_coords.append((selected_state,gender,state_coords))

                all_coords = sorted(all_coords, key=lambda x: x[2]["y"][0], reverse=True)
                plotter.create_plot(all_coords, selected_x, selected_y, dotted=True)
                plotter.reduce_subplot_no()

            all_coords = []
            for selected_country in selected_countries:
                for selected_y_t,gender in selected_ys:
                    state_coords = get_country_coords(selected_country, selected_y_t, selected_years)
                    all_coords.append((selected_country,gender,state_coords))
            all_coords = sorted(all_coords, key=lambda x: x[2]["y"][0], reverse=True)

            plotter.create_plot(all_coords, selected_x, selected_y)



        for indicator_selected, indicator_name in zip([le_indicator, tfr_indicator, gdp_indicator], other_indicators):
            if not indicator_selected:
                continue
            data = []
            if len(selected_states) > 0:
                for selected_state in selected_states:
                    state_coords = get_state_coords(selected_state, indicator_name)
                    if state_coords is None:
                        continue
                    data.append((selected_state, "" ,state_coords))
                plotter.create_plot(data, selected_x, indicator_name, dotted=True)
                plotter.reduce_subplot_no()

            data = []
            for selected_country in selected_countries:
                country_coords = get_country_coords(selected_country, indicator_name, selected_years)
                if country_coords is None:
                    continue
                data.append((selected_country, "" ,country_coords))
            plotter.create_plot(data, selected_x, indicator_name)

    else:

        if edu_indicator:
            all_coords = []
            for selected_state in selected_states:
                for selected_y_t,gender in selected_ys:
                    state_coords = get_state_coords(selected_state, selected_y_t)
                    all_coords.append((selected_state,gender,state_coords))

            all_coords = sorted(all_coords, key=lambda x: x[2]["y"][0], reverse=True)
            plotter.create_plot(all_coords, selected_x, selected_y, dotted=True)


        for indicator_selected, indicator_name in zip([le_indicator, tfr_indicator, gdp_indicator], other_indicators):
            if not indicator_selected:
                continue
            data = []
            for selected_state in selected_states:
                state_coords = get_state_coords(selected_state, indicator_name)
                if state_coords is None:
                    continue
                data.append((selected_state, "" ,state_coords))
            plotter.create_plot(data, selected_x, indicator_name, dotted=True)



    if country_coords is not None and world:
        col1, col2  = st.columns(2)
        file_name   = f"{selected_x[:3]}_{selected_y[:3]}"

        if selected_y in constants.edu_indices:
            c_selected_y = selected_options[0] + " " + selected_y
        else:
            c_selected_y = selected_y
        csv_snippet = save_csv(selected_countries, selected_x, c_selected_y, selected_years)
        with open("chart.csv", "rb") as f:
            data_bytes      = f.read()
            col1.download_button(
                label       = "Download Data 💿",
                data        = data_bytes,
                file_name   = f"{file_name}.csv",
                mime        = "text/csv",
                key         = "data_download_button"
            )

        plotter.save_plot("chart.png")
        # fig.savefig("chart.png")
        with open("chart.png", "rb") as f:
            image_bytes     = f.read()
            col2.download_button(
                label       = "Download Graph 📈",
                data        = image_bytes,
                file_name   = f"{file_name}.png",
                mime        = "image/png",
                key         = "graph_download_button"
            )

    st.pyplot(plotter.get_fig())
    # st.plotly_chart(plotter.get_fig(), use_container_width=True)


    if world:

        st.query_params.update({
            "c"       : ",".join(selected_countries),
            "x"       : cleaned_indices_reversed[selected_x],
            "y"       : cleaned_indices_reversed[selected_y],
            "sy"      : selected_years[0],
            "ey"      : selected_years[1],
            "gender"  : ",".join(selected_options),
            "other"   : ",".join(selected_other_indicators),
            "world"   : "true",
            "vertical": str(vertical_view).lower()
        })
    else:
        st.query_params.update({
            "s"       : ",".join(selected_states),
            "y"       : cleaned_indices_reversed[selected_y],
            "gender"  : ",".join(selected_options),
            "other"   : ",".join(selected_other_indicators),
            "world"   : "false",
            "vertical": str(vertical_view).lower()
        })


    if world:
        st.markdown(
    """**_Note_** :  the Education data used is for age group 20-24 old:

    - **Primary Education**           : 6 years of education
    - **Lower Secondary Education**   : 9 years of education
    - **Higher Secondary Education**  : 12 years of education
    - **College Completion**          : 16 years of education
                            """
        )


main()
