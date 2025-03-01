# pyright: reportMissingModuleSource=false
import pandas as pd

root = "datasets/"
datasets_path = {
    "Female Primary Education": root + "20-24-female-Primary_fin.csv",
    "Female Lower Secondary Education": root + "20-24-female-Lower_Secondary_fin.csv",
    "Female Higher Secondary Education": root + "20-24-female-Higher_Secondary_fin.csv",
    "Female College Completion": root + "20-24-female-College_comp.csv",
    
    "Male Primary Education": root + "20-24-male-Primary_fin.csv",
    "Male Lower Secondary Education": root + "20-24-male-Lower_Secondary_fin.csv",
    "Male Higher Secondary Education": root + "20-24-male-Higher_Secondary_fin.csv",
    "Male College Completion": root + "20-24-male-College_comp.csv",
    
    "Both Primary Education": root + "20-24-Primary_fin.csv",
    "Both Lower Secondary Education": root + "20-24-Lower_Secondary_fin.csv",
    "Both Higher Secondary Education": root + "20-24-Higher_Secondary_fin.csv",
    "Both College Completion": root + "20-24-College_comp.csv",
    
    "Total Fertility Rate": root + "children_per_woman_total_fertility.csv",
    "Life Expectancy": root + "life_expectancy_years.csv",
    
    "GDP per Capita": root + "gdppercapita_us_inflation_adjusted.csv",
    
    "Years": root + "years.csv",
    
    "india_tfr": root + "India/TFR.csv",
}

india = "India/"
states_datasets_path = {
    "Female Primary Gross Enrolment Ratio": root + india +"primary-girls.csv",
    "Female Lower Secondary Gross Enrolment Ratio": root + india +"lower-secondary-girls.csv",
    "Female Higher Secondary Gross Enrolment Ratio": root + india +"upper-secondary-girls.csv",
    
    "Male Primary Gross Enrolment Ratio": root + india +"primary-boys.csv",
    "Male Lower Secondary Gross Enrolment Ratio": root + india + "lower-secondary-boys.csv",
    "Male Higher Secondary Gross Enrolment Ratio": root + india + "upper-secondary-boys.csv",
    
    "Both Primary Gross Enrolment Ratio": root + india + "primary-total.csv",
    "Both Lower Secondary Gross Enrolment Ratio": root + india + "lower-secondary-total.csv",
    "Both Higher Secondary Gross Enrolment Ratio": root + india + "upper-secondary-total.csv",
    
    "Female Primary Education": root + india +"primary-girls.csv",
    "Female Lower Secondary Education": root + india +"lower-secondary-girls.csv",
    "Female Higher Secondary Education": root + india +"upper-secondary-girls.csv",
    
    "Male Primary Education": root + india +"primary-boys.csv",
    "Male Lower Secondary Education": root + india + "lower-secondary-boys.csv",
    "Male Higher Secondary Education": root + india + "upper-secondary-boys.csv",
    
    "Both Primary Education": root + india + "primary-total.csv",
    "Both Lower Secondary Education": root + india + "lower-secondary-total.csv",
    "Both Higher Secondary Education": root + india + "upper-secondary-total.csv",
    
    "Life Expectancy": root + india + "le-india-both.csv",
    "Total Fertility Rate": root + india + "tfr-india.csv",
    
    "GDP per Capita": root + india + "gdp-india.csv",
}

def get_countries():
    le_df     = pd.read_csv(datasets_path["Life Expectancy"])
    countries = le_df["Country"].unique()
    return countries
    
def get_indian_states():
    ind_edu_df    = pd.read_csv(states_datasets_path["Life Expectancy"])
    indian_states = ind_edu_df["state"].unique()
    return indian_states

def get_country_coords(country, y, years):
    years = list(years)
    df    = pd.read_csv(datasets_path[y])
    df    = df[df["Country"] == country]
    
    if len(df) == 0:
        return None

    df    = df.drop(["Country"], axis=1)
    # keep only columns within values years[0] and years[1]
    if(y == "Total Fertility Rate" and years[1]>2015):
        years[1] = 2015
    selected_columns = [str(year) for year in range(years[0], years[1] + 1)]
    df    = df[selected_columns]
    
    df    = df.dropna(axis=1)
    df    = df.T
    df.reset_index(inplace=True)
    
    df.columns = ["x", "y"]
    # df = df[df["x"].str.isnumeric()]
    df["x"] = df["x"].astype(int)
    
    if (df["y"].dtype == "object"):
        df["y"] = df["y"].astype(float)
    return df


def get_state_coords(state, y):
    df = pd.read_csv(states_datasets_path[y])
    df = df[df["state"] == state]
    if len(df) == 0:
        return None
    df = df.drop(["state"], axis=1)
    df = df.dropna(axis=1)
    df = df.T
    df.reset_index(inplace=True)
    df.columns = ["x", "y"]
    # df = df[df["x"].str.isnumeric()]
    df["x"] = df["x"].astype(int)
    
    if (df["y"].dtype == "object"):
        df["y"] = df["y"].astype(float)
    return df


def save_csv(selected_countries, x, y, years):
    df_1 = pd.read_csv(datasets_path[x])
    df_2 = pd.read_csv(datasets_path[y])
    df_1 = df_1[df_1["Country"].isin(selected_countries)]
    df_2 = df_2[df_2["Country"].isin(selected_countries)]

    melted_df_1 = pd.melt(df_1, id_vars=["Country"], var_name="year", value_name=x)

    melted_df_1["year"] = melted_df_1["year"].astype(int)

    melted_df_2 = pd.melt(df_2, id_vars=["Country"], var_name="year", value_name=y)
    melted_df_2["year"] = melted_df_2["year"].astype(int)

    merged_df = pd.merge(melted_df_1, melted_df_2, on=["Country", "year"])
    merged_df.sort_values(by=["Country", "year"], inplace=True)
    
    merged_df = merged_df[merged_df["year"] >= years[0]]
    merged_df = merged_df[merged_df["year"] <= years[1]]
    
    merged_df.to_csv("chart.csv", index=False)
    return
