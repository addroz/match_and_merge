# Match and Merge Module

Compact module for fetching, preprocessing, matching, merging and aggregating power plants data.

The module consists of two separate programs: data_fetch and match_and_merge, and the config file
config.py, shared by both programs.

# Data fetch

Simple data fetcher for the three databases used for merging. Loads newest original versions of the
databases from adresses provided in the config file, and saves them accordingly in `cpp_db_original`,
`jrc_db_original` and `wri_db_original` directories. The program should be run whenever a new
version of the databases is published. Usage:

`python data_fetch.py`

Note: It is not advised to introduce any manual changes in the data in `cpp_db_original`,
`jrc_db_original` and `wri_db_original` directories, as all such changes will be overwritten whenever
the script is run.

# Match and Merge

More complex of the two programs, performing the following main operations:
1. Reading and preprocessing the data from the three databases, unifying their format.
2. Matching the power plants in three databases.
4. Merging them into one data file, containing all the unique data in there (merged.csv).
3. Grouping the data about power plants by year and by country (grouped.xlsx).

Usage:
`python match_and_merge.py`

Basic configuration, to change in config.py file:
1. COUNTRIES - list of countries to be included in the merged and grouped data.
2. COUNTRIES_NAME_TO_ABBR - a dictionary of countries' abbreviations, used later in the grouped.xlsx file as sheets' titles.
3. TYPES - types of power plants/fuels distinguished and used in the output file.
4. YEARS - all years (ID-year) used as periods signatures in the grouped file.
5. DATA_YEAR - the year (year) for which data is generated, ie. we are only interested in plants active in this year.
6. *_FILE_PATH - relative paths to the main .csv files for each database
7. UNCONDITIONAL_DISTANCE_CRITERION -the distance, below which two plants in the same type group and in the same country, will be considered the same plant regardless of their other characteristics (in km)

More advanced configuration options are described in the config.py file.

Note: It is not advised to introduce any manual changes in the output files `grouped.xlsx` and `merged.csv`,
as all such changes will be overwritten whenever the script is run.
