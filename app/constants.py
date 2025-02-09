

edu_indices = [
    "Primary Education",
    "Lower Secondary Education",
    "Higher Secondary Education", 
    "College Completion",
]

india_edu_indices = [
    "Primary Gross Enrolment Ratio",
    "Lower Secondary Gross Enrolment Ratio",
    "Higher Secondary Gross Enrolment Ratio", 
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

cleaned_indices ={
    "pri_edu" : "Primary Education",
    "pri_ge" : "Primary Gross Enrolment Ratio",
    "ls_edu" : "Lower Secondary Education",
    "ls_ge" : "Lower Secondary Gross Enrolment Ratio",
    "hs_edu" : "Higher Secondary Education",
    "hs_ge" : "Higher Secondary Gross Enrolment Ratio",
    "clg_comp" : "College Completion",
    "gdp" : "GDP per Capita",
    "le" : "Life Expectancy",
    "tfr" : "Total Fertility Rate",
    "time" : "Years",
    
}

custom_style = """
    <style>
    .image-container {
        position: relative;
        display: inline-block;
    }

    .icon {
        position: absolute;
        top: 5px;
        right: 5px;
        width:20px;
        height:20px;
        font-size: 15px;
        color: white;
        background-color: #fff;
        display: flex;
        justify-content: center; 
        align-items: center;
        border-radius: 50%;
    }
    
    .trackedIcon {
        width:24px;
        height:24px;
        font-size: 19px;
        color: white;
        background-color: #000;
        border-radius: 50%;
        display: flex;
        justify-content: center; 
        align-items: center;
    }
    </style>
    """