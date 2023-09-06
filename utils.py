# pyright: reportMissingModuleSource=false
import pandas as pd

root = "./edu_datasets/"
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


def get_country_coords(country, x, y, years):
    df_1 = pd.read_csv(datasets_path[x])
    df_2 = pd.read_csv(datasets_path[y])

    df_1 = df_1[df_1["Country"] == country]
    df_2 = df_2[df_2["Country"] == country]

    df_1 = df_1.drop(["Country"], axis=1)
    df_2 = df_2.drop(["Country"], axis=1)

    df_1 = df_1.T
    df_2 = df_2.T

    df_3 = df_1.merge(df_2, left_index=True, right_index=True)
    df_3.columns = ["x", "y"]

    df_3.reset_index(inplace=True)
    df_3.rename(columns={"index": "year"}, inplace=True)
    df_3 = df_3[df_3["year"].str.isnumeric()]
    df_3["year"] = df_3["year"].astype(int)
    df_3 = df_3[df_3["year"] >= years[0]]
    df_3 = df_3[df_3["year"] <= years[1]]
    df_3.dropna(inplace=True)

    df_3.drop(["year"], axis=1, inplace=True)
    return df_3


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
