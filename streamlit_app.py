# pyright: reportMissingModuleSource=false
# pyright: reportMissingImports=false
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import (
    get_country_coords,
    get_state_coords,
    save_csv,
)

# dropdown box for selecting country



le_df = pd.read_csv("./edu_datasets/life_expectancy_years.csv")
ind_edu_df = pd.read_csv("./edu_datasets/India/primary-total.csv")
countries = le_df["Country"].unique()
indian_states = ind_edu_df["state"].unique()

edu_indices = [
    "Primary Education",
    "Lower Secondary Education",
    "Higher Secondary Education", 
]

india_edu_indices = [
    "Primary Gross Enrolment Ratio",
    "Lower Secondary Gross Enrolment Ratio",
    "Higher Secondary Gross Enrolment Ratio", 
]

college_indices = [
    "College Completion",
]

state_data_indices = [
    "Primary Education",
    "Lower Secondary Education",
]

health_indices = [
    "Total Fertility Rate",
    "Life Expectancy",
]

econ_indices = [
    "GDP per Capita",
]

time_indices = [
    "Years",
]

indices = edu_indices + college_indices + health_indices + econ_indices + time_indices

india_indices = india_edu_indices


cleaned_indices ={
    "f_pri_edu" : "Female Primary Education",
    "f_ls_edu" : "Female Lower Secondary Education",
    "f_hs_edu" : "Female Higher Secondary Education",
    "f_clg_comp" : "Female College Completion",
    "m_pri_edu" : "Male Primary Education",
    "m_ls_edu" : "Male Lower Secondary Education",
    "m_hs_edu" : "Male Higher Secondary Education",
    "m_clg_comp" : "Male College Completion",
    "pri_edu" : "Primary Education",
    "ls_edu" : "Lower Secondary Education",
    "hs_edu" : "Higher Secondary Education",
    "clg_comp" : "College Completion",
    "gdp" : "GDP per Capita",
    "le" : "Life Expectancy",
    "tfr" : "Total Fertility Rate",
    "time" : "Years",
    
}

cleaned_indices_reversed = {v: k for k, v in cleaned_indices.items()}


selected_options = []
selected_ys = []

params = st.experimental_get_query_params()
selected_states = []
selected_countries = params.get("c", countries)
selected_countries = selected_countries[0].split(",")
selected_options = params.get("gender", [])
if(len(selected_options) == 0):
    selected_options = ["Female"]
selected_x, selected_y = indices[0], indices[1]
try:
    selected_x = cleaned_indices[params.get("x", indices)[0]]
except:
    pass

try:
    selected_y = cleaned_indices[params.get("y", indices)[0]]
except:
    pass

try:
    start_year = params.get("sy", 1960)[0]
except:
    start_year = 1960
try:
    end_year = params.get("ey", 2020)[0]
except:
    end_year = 2020
    


st.title("Plots 🌎")

if("world" not in st.session_state):
    st.session_state["world"] = True

col1, col2 = st.columns(2)

if(col1.button("World", type="primary" if st.session_state["world"] else "secondary")):
    st.session_state["world"] = True
    st.experimental_rerun()
    pass
if(col2.button("India",type="primary" if not st.session_state["world"] else "secondary")):
    st.session_state["world"] = False
    st.experimental_rerun()
    pass

col1, col2 = st.columns(2)
if(st.session_state["world"]):
    selected_y      = col1.selectbox("Select y axis", indices, index=indices.index(selected_y))
    selected_x      = col2.selectbox("Select x axis", indices, index=indices.index(selected_x))
else:
    selected_y      = col1.selectbox("Select y axis", india_indices, index=indices.index(selected_y))
    selected_x      = col2.selectbox("Select x axis", time_indices, index=0, disabled=True)

if(st.session_state["world"]):
    if(selected_y in edu_indices): 
        
        col1, col2, col3 = st.columns(3)
        options = ['Both', 'Male', 'Female']
        
        checkbox_state1 = col1.checkbox(options[0],value = options[0] in selected_options)
        checkbox_state2 = col2.checkbox(options[1],value = options[1] in selected_options)
        checkbox_state3 = col3.checkbox(options[2],value = options[2] in selected_options)
        
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
        
    if(selected_x in edu_indices):
        selected_x = "Both " + selected_x
    # Add a dropdown box to select a country
    selected_countries = st.multiselect("Select Countries", countries, selected_countries)

    selected_years  = st.slider("Select years", 1960, 2020, (int(start_year), int(end_year)))

else:

    col1, col2, col3 = st.columns(3)
    options = ['Both', 'Male', 'Female']
    
    checkbox_state1 = col1.checkbox(options[0],value = options[0] in selected_options)
    checkbox_state2 = col2.checkbox(options[1],value = options[1] in selected_options)
    checkbox_state3 = col3.checkbox(options[2],value = options[2] in selected_options)
    
    for i,checkbox in enumerate([checkbox_state1, checkbox_state2, checkbox_state3]):
        if checkbox:
            selected_options.append(options[i])
        elif options[i] in selected_options and not checkbox:
            selected_options.remove(options[i])

    selected_options = list(set(selected_options))
    for selected_option in selected_options:
        selected_ys.append((selected_option + " " + selected_y,selected_option))
    st.write(selected_y)
    
    selected_states = st.multiselect("Select States", indian_states, selected_states)



if(st.session_state["world"]):
    st.experimental_set_query_params(
        c=",".join(selected_countries),
        x=cleaned_indices_reversed[selected_x],
        y=cleaned_indices_reversed[selected_y],
        sy=selected_years[0],
        ey=selected_years[1],
        gender=selected_options
    )


# plot the line chart using Matplotlib
fig, ax = plt.subplots()
country_coords = None
if(st.session_state["world"]):
    for selected_country in selected_countries:
        for selected_y,gender in selected_ys:
            country_coords = get_country_coords(selected_country, selected_x, selected_y,selected_years)
            ax.plot(country_coords["x"], country_coords["y"], label=selected_country + " " + gender)
else:
    for selected_state in selected_states:
        for selected_y,gender in selected_ys:
            state_coords = get_state_coords(selected_state, selected_y)
            # dotted line
            ax.plot(state_coords["x"], state_coords["y"], "--" ,label=selected_state + " " + gender)

ax.set_xlabel(selected_x)
ax.set_ylabel(selected_y)
ax.set_title(f"{selected_y} vs {selected_x}")
ax.legend()



if country_coords is not None and st.session_state["world"]:
    col1, col2  = st.columns(2)
    file_name   = f"{selected_x[:3]}_{selected_y[:3]}"

    csv_snippet = save_csv(selected_countries, selected_x, selected_y, selected_years)
    with open("chart.csv", "rb") as f:
        data_bytes = f.read()
        col1.download_button(
            label       = "Download Data 💿",
            data        = data_bytes,
            file_name   = f"{file_name}.csv",
            mime        = "text/csv",
        )

    fig.savefig("chart.png")
    with open("chart.png", "rb") as f:
        image_bytes = f.read()
        col2.download_button(
            label       = "Download Graph 📈",
            data        = image_bytes,
            file_name   = f"{file_name}.png",
            mime        = "image/png",
        )
# display the chart in Streamlit app
st.pyplot(fig)


st.markdown(
"""**_Note_** :  the Education data used is only 20-25 year old age group and data and it is as follows:

- **Primary Education**           : 6 years of education
- **Lower Secondary Education**   : 9 years of education
- **Higher Secondary Education**  : 12 years of education
- **College Completion**          : 16 years of education
                        """
)




