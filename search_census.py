import requests
import json
import pandas

# Reference: https://www.census.gov/data/developers/data-sets/acs-5year.html


def acs_5yr_data(census_api_key):
    # PROFILE VARIABLES (https://api.census.gov/data/2018/acs/acs5/profile/variables.html)
    # DP03_0062E -- Estimate!!INCOME AND BENEFITS (IN 2018 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars)
    # DP02_0001E -- Estimate!!HOUSEHOLDS BY TYPE!!Total households
    # DP04_0001E -- Estimate!!HOUSING OCCUPANCY!!Total housing units
    # STATE -- Geography
    # ZCTA -- Geography
    # ...

    # SUBJECT VARIABLES ()
    # S0101_C02_001E -- Estimate!!Percent!!Total population
    # S0102_C01_074E -- Estimate!!Total!!INCOME IN THE PAST 12 MONTHS (IN 2018 INFLATION-ADJUSTED DOLLARS)!!Households
    # ...

    url_subject = f"https://api.census.gov/data/2018/acs/acs5/subject?get=NAME,S0101_C01_001E&for=zip%20code%20tabulation%20area:*&key={census_api_key}"
    url_profile = f"https://api.census.gov/data/2018/acs/acs5/profile?get=STATE,ZCTA,DP03_0062E,DP02_0001E,DP04_0001E&for=zip%20code%20tabulation%20area:*&key={census_api_key}"
    response = requests.get(url=url_profile)

    # print(response.status_code)
    print(response.text)


acs_5yr_data("ee5070bcdcb0591934ba1076339e43b561a101ee")

