# LiveSessionPlots - HDI Data Visualization

## Project Overview
This project visualizes Human Development Index (HDI) data across different countries and years. It provides interactive plots and analysis tools to understand global development trends using Streamlit.

## Deployed Streamlit URL:
https://hdi-plots-v3.streamlit.app/

## Data Source
The data is sourced from multiple official United Nations Development Programme (UNDP) resources:

### Dataset Files and Sources:

#### Education Related Datasets (From World Bank Education Statistics):
1. College Completion Rate Datasets:
   - `20-24-College_comp.csv`
   - `20-24-female-College_comp.csv`
   - `20-24-male-College_comp.csv`
   Source: [World Bank EdStats](https://databank.worldbank.org/source/education-statistics)****

2. Secondary Education Completion Datasets:
   - `20-24-Higher_Secondary_fin.csv`
   - `20-24-female-Higher_Secondary_fin.csv`
   - `20-24-male-Higher_Secondary_fin.csv`
   - `20-24-Lower_Secondary_fin.csv`
   - `20-24-female-Lower_Secondary_fin.csv`
   - `20-24-male-Lower_Secondary_fin.csv`
   Source: [UNESCO Institute for Statistics](http://data.uis.unesco.org/)

3. Primary Education Completion Datasets:
   - `20-24-Primary_fin.csv`
   - `20-24-female-Primary_fin.csv`
   - `20-24-male-Primary_fin.csv`
   Source: [UNESCO Institute for Statistics](http://data.uis.unesco.org/)

#### Economic and Demographic Indicators:
1. `gdppercapita_us.csv`
   Source: [Gapminder GDP per capita](https://www.gapminder.org/data/documentation/gd001/) 

2. `Life_Expectancy_2022.csv`
   Source: [Gapminder Life Expectancy](https://www.gapminder.org/data/documentation/gd004/)

3. `Fertility_rate_2022.csv`
   Source: [Gapminder Total Fertility](https://www.gapminder.org/data/documentation/gd008/)

4. `years.csv`
   Source: Generated internally for time series reference

Note: The India directory contains country-specific detailed data from various government sources.

All datasets are publicly available and were downloaded between 2022-2023. Some datasets required preprocessing and format conversion for compatibility with the application.

1. `hdi_master.csv`: Contains HDI values and rankings (1990-2021)
   - Source: [UNDP HDI Time Series Data](https://hdr.undp.org/sites/default/files/2021-22_HDR/HDR21-22_Statistical_Annex_HDI_Table.xlsx)

2. `life_expectancy.csv`: Life expectancy at birth data
   - Source: [UNDP Life Expectancy Dataset](https://hdr.undp.org/sites/default/files/2021-22_HDR/HDR21-22_Statistical_Annex_Life_Expectancy_Table.xlsx)

3. `education_index.csv`: Education index components
   - Source: [UNDP Education Data Tables](https://hdr.undp.org/sites/default/files/2021-22_HDR/HDR21-22_Statistical_Annex_Education_Table.xlsx)

4. `gni_per_capita.csv`: GNI per capita (PPP $) data
   - Source: [UNDP Income Index Data](https://hdr.undp.org/sites/default/files/2021-22_HDR/HDR21-22_Statistical_Annex_GNI_Table.xlsx)

All datasets were processed and converted from their original Excel format to CSV for use in this application. The raw data can be accessed through the [UNDP Human Development Reports Data Center](https://hdr.undp.org/data-center).

The dataset includes:
- HDI values for countries from 1990 to 2021
- Components of HDI:
  - Life expectancy at birth
  - Expected years of schooling
  - Mean years of schooling
  - GNI per capita (PPP $)

## Features
- Interactive time series plots of HDI trends
- Country comparison tools
- Component-wise HDI analysis
- Regional and global development patterns
- Downloadable data visualization

## Technical Implementation
- Backend: Python with Pandas for data processing
- Visualization: Plotly for interactive charts
- Web Interface: Streamlit
- Data format: CSV files stored in the `data/` directory

## To run locally

1. Create and Activate virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Start streamlit app
```
streamlit run streamlit_app.py
```

## Project Structure
```
├── data/                  # Contains HDI dataset files
├── streamlit_app.py       # Main application file
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Data Processing
The application processes HDI data through the following steps:
1. Data loading from CSV files
2. Cleaning and preprocessing
3. Creating interactive visualizations
4. Enabling user-driven analysis through filters and selections

## Contributing
Feel free to submit issues and enhancement requests for improving the visualization and analysis capabilities.
