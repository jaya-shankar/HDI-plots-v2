# pyright: reportMissingModuleSource=false
import pandas as pd
import os
import re
import unicodedata
from functools import lru_cache
from typing import Optional, Set, Dict, List
from app.hdi_preprocessor import preprocess_hdi_data, get_hdi_data_for_country, get_hdi_data_for_save_csv, get_hdi_data_for_state

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
    
    "Total Fertility Rate": root + "Fertility_rate_2022.csv",
    "Life Expectancy": root + "Life_Expectancy_2022.csv",
    "Human Development Index": root + "human-development-index.csv",
    
    "GDP per Capita": root + "gdppercapita_us.csv",
    
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

# Alias and country name normalization utilities
ALIAS_CSV_PATH = os.path.join("datasets", "country_name_map.csv")

def _strip_accents(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKD", text)
    return "".join([c for c in text if not unicodedata.combining(c)])

def normalize_country_name(name: str) -> str:
    # Lowercase, strip, remove diacritics, normalize punctuation/whitespace, map & to and
    if name is None:
        return ""
    s = str(name).strip()
    s = _strip_accents(s)
    s = s.replace("&", " and ")
    s = re.sub(r"[\"'`]", "", s)  # quotes
    s = re.sub(r"[().]", " ", s)  # parens and dots to space
    s = re.sub(r"[-_/]", " ", s)  # separators to space
    s = re.sub(r"\s+", " ", s)    # collapse spaces
    return s.lower().strip()

@lru_cache(maxsize=1)
def load_country_alias_map():
    # Returns a dict from normalized alias -> canonical
    mapping = {}
    canonical_to_aliases = {}
    # Built-in common aliases beyond the CSV
    builtin = {
        # Prefer South Korea as canonical
        "Korea, Rep.": "South Korea",
        "Republic of Korea": "South Korea",
        "Korea (Republic of)": "South Korea",
        "Korea, South": "South Korea",
        # A few common variants
        "Bahamas, The": "Bahamas",
        "Gambia, The": "Gambia",
        "Curacao": "Curaçao",
    }
    try:
        df = pd.read_csv(ALIAS_CSV_PATH, encoding="utf-8-sig")
        for _, row in df.iterrows():
            canonical = str(row.get("canonical", "")).strip()
            alias = str(row.get("alias", "")).strip()
            if not canonical or not alias:
                continue
            mapping[normalize_country_name(alias)] = canonical
            canonical_to_aliases.setdefault(canonical, set()).add(alias)
    except Exception:
        # File may not exist; continue with builtins only
        pass
    for alias, canonical in builtin.items():
        mapping[normalize_country_name(alias)] = canonical
        canonical_to_aliases.setdefault(canonical, set()).add(alias)
    # Ensure canonical self-maps too
    canonicals = set(canonical_to_aliases.keys())
    for c in canonicals:
        mapping[normalize_country_name(c)] = c
    return mapping

@lru_cache(maxsize=1)
def get_alias_display_map():
    # Dict[canonical] -> sorted list of aliases
    display = {}
    try:
        df = pd.read_csv(ALIAS_CSV_PATH, encoding="utf-8-sig")
        for canonical, group in df.groupby("canonical"):
            aliases = sorted(set([a for a in group["alias"].dropna().astype(str).str.strip().tolist() if a]))
            if aliases:
                display[canonical] = aliases
    except Exception:
        pass
    # Merge builtins
    for alias, canonical in {
        "Korea, Rep.": "South Korea",
        "Republic of Korea": "South Korea",
        "Korea (Republic of)": "South Korea",
        "Korea, South": "South Korea",
        "Bahamas, The": "Bahamas",
        "Gambia, The": "Gambia",
        "Curacao": "Curaçao",
    }.items():
        display.setdefault(canonical, [])
        if alias not in display[canonical]:
            display[canonical].append(alias)
    # Sort lists
    for k in list(display.keys()):
        display[k] = sorted(set(display[k]))
    return display

def canonicalize_country_name(name: str, valid_canonicals: Optional[Set[str]] = None) -> str:
    if not name:
        return ""
    mapping = load_country_alias_map()
    norm = normalize_country_name(name)
    canonical = mapping.get(norm)
    resolved_from_map_or_match = canonical is not None
    # If explicit mapping not found, try to match against valid canonicals by normalization
    if canonical is None and valid_canonicals is not None:
        for vc in valid_canonicals:
            if normalize_country_name(vc) == norm:
                canonical = vc
                resolved_from_map_or_match = True
                break
    # Fallback: if still not found, return the original name (even if not in valid set)
    if canonical is None:
        canonical = name
        resolved_from_map_or_match = False
    return canonical

def canonicalize_country_list(names, valid_canonicals: Optional[Set[str]] = None) -> List[str]:
    if not names:
        return []
    out = []
    seen = set()
    for n in names:
        c = canonicalize_country_name(n, valid_canonicals=valid_canonicals)
        if c and c not in seen:
            out.append(c)
            seen.add(c)
    return out

def standardize_country_column(df: pd.DataFrame, country_col: str = "Country") -> pd.DataFrame:
    if country_col not in df.columns:
        return df
    mapping = load_country_alias_map()
    # Map by normalization
    def _map_fn(x):
        return mapping.get(normalize_country_name(x), x)
    df = df.copy()
    df[country_col] = df[country_col].apply(_map_fn)
    return df

def get_countries():
    
    le_df     = pd.read_csv(datasets_path["Life Expectancy"], encoding='utf-8-sig')
    le_df     = standardize_country_column(le_df, "Country")
    countries = le_df["Country"].unique()
    return countries
    
def get_indian_states():
    ind_edu_df    = pd.read_csv(states_datasets_path["Life Expectancy"], encoding='utf-8-sig')
    indian_states = ind_edu_df["state"].unique()
    return indian_states


# HDI preprocessing functions moved to app/hdi_preprocessor.py

def get_country_coords(country, y, years):
    years = list(years)
    
    # Special handling for HDI data
    if y == "Human Development Index":
        return get_hdi_data_for_country(country, years)
    else:
        # Original implementation for other indicators
        df = pd.read_csv(datasets_path[y], encoding='utf-8-sig')
        df = standardize_country_column(df, "Country")
        df = df[df["Country"] == country]
        
        if len(df) == 0:
            return None

        df = df.drop(["Country"], axis=1)
        
        # Clean column names - remove quotes and strip whitespace
        df.columns = df.columns.astype(str).str.strip('"').str.strip()
        
        # keep only columns within values years[0] and years[1]
        selected_columns = [str(year) for year in range(years[0], years[1] + 1)]
        
        # Filter to only include columns that exist in the dataframe
        existing_columns = [col for col in selected_columns if col in df.columns]
        if len(existing_columns) == 0:
            return None
            
        df = df[existing_columns]
        
        df = df.dropna(axis=1)
        if df.empty or df.shape[1] == 0:
            return None
            
        df = df.T
        df.reset_index(inplace=True)
        
        df.columns = ["x", "y"]
        df["x"] = df["x"].astype(int)
        
        if (df["y"].dtype == "object"):
            df["y"] = df["y"].astype(float)
        return df


def get_state_coords(state, y):
    # Special handling for HDI data for Indian states
    if y == "Human Development Index":
        return get_hdi_data_for_state(state)
    
    # Check if the dataset exists for this indicator
    if y not in states_datasets_path:
        return None
    
    df = pd.read_csv(states_datasets_path[y], encoding='utf-8-sig')
    df = df[df["state"] == state]
    if len(df) == 0:
        return None
    df = df.drop(["state"], axis=1)
    
    # Clean column names - remove quotes and strip whitespace
    df.columns = df.columns.astype(str).str.strip('"').str.strip()
    
    df = df.dropna(axis=1)
    if df.empty or df.shape[1] == 0:
        return None
        
    df = df.T
    df.reset_index(inplace=True)
    df.columns = ["x", "y"]
    df["x"] = df["x"].astype(int)
    
    if (df["y"].dtype == "object"):
        df["y"] = df["y"].astype(float)
    return df


def save_csv(selected_countries, x, y, years):
    # Special handling for HDI data
    if y == "Human Development Index":
        df_1 = pd.read_csv(datasets_path[x], encoding='utf-8-sig')
        df_2 = get_hdi_data_for_save_csv(selected_countries)
        df_1 = standardize_country_column(df_1, "Country")
        df_2 = standardize_country_column(df_2, "Country")
    else:
        df_1 = pd.read_csv(datasets_path[x], encoding='utf-8-sig')
        df_2 = pd.read_csv(datasets_path[y], encoding='utf-8-sig')
        df_1 = standardize_country_column(df_1, "Country")
        df_2 = standardize_country_column(df_2, "Country")
    
    df_1 = df_1[df_1["Country"].isin(selected_countries)]
    df_2 = df_2[df_2["Country"].isin(selected_countries)]

    melted_df_1 = pd.melt(df_1, id_vars=["Country"], var_name="year", value_name=x)
    melted_df_1["year"] = melted_df_1["year"].astype(int)

    # Handle HDI data which has integer column names after preprocessing
    if y == "Human Development Index":
        # Convert column names to strings for consistency
        year_columns = [str(col) for col in df_2.columns if col != "Country"]
        df_2_subset = df_2[["Country"] + year_columns]
        melted_df_2 = pd.melt(df_2_subset, id_vars=["Country"], var_name="year", value_name=y)
    else:
        melted_df_2 = pd.melt(df_2, id_vars=["Country"], var_name="year", value_name=y)
    
    melted_df_2["year"] = melted_df_2["year"].astype(int)

    merged_df = pd.merge(melted_df_1, melted_df_2, on=["Country", "year"])
    merged_df.sort_values(by=["Country", "year"], inplace=True)
    
    merged_df = merged_df[merged_df["year"] >= years[0]]
    merged_df = merged_df[merged_df["year"] <= years[1]]
    
    merged_df.to_csv("chart.csv", index=False)
    return
