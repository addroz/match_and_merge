### Fetch config

# links to the websites from which we download both databases
WRI_DB_LINK = 'https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip?download=1'
JRC_DB_LINK = 'https://zenodo.org/record/3574566/files/JRC-PPDB-OPEN.ver1.0.zip?download=1'
CPP_DB_LINK = 'https://data.open-power-system-data.org/conventional_power_plants/opsd-conventional_power_plants-2020-10-01.zip'

### Basic config

# Countries for which the merging is performed and data saved
COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Switzerland', 'Czechia', 'Germany', 'Denmark', 'Estonia',
    'Greece', 'Spain', 'Finland', 'France', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania',
    'Luxembourg', 'Latvia', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia',
    'Slovakia', 'United Kingdom']

# The map of countries names to their coresponding abbreviations, used in the output excel file
COUNTRIES_NAME_TO_ABBR = {'Austria':'AT', 'Belgium':'BE', 'Bulgaria':'BG', 'Croatia':'HR', 'Czechia':'CZ',
    'Denmark':'DK', 'Estonia':'EE', 'Finland':'FI', 'France':'FR', 'Germany':'DE', 'Greece':'EL',
    'Ireland':'IE', 'Hungary':'HU', 'Italy':'IT', 'Latvia':'LV', 'Lithuania':'LT', 'Luxembourg':'LU',
    'Malta':'MT', 'Netherlands':'NL', 'Norway':'NO', 'Poland':'PL', 'Portugal':'PT', 'Romania':'RO',
    'Slovakia':'SK', 'Slovenia':'SI', 'Spain':'ES', 'Sweden':'SE', 'United Kingdom':'UK',
    'Switzerland': 'CH'}

# Names of all the types of plants/fuels used in the output file
TYPES = ['Bio_CCS', 'Bioenergy', 'Coal', 'Coal_CCS', 'Gas_CCGT', 'Gas_CCS', 'Gas_OCGT',
    'Gas_ST', 'Geothermal', 'Lignite', 'Nuclear', 'OilOther']

# years for which the ouptut is generated
YEARS = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020]

# year of the data
DATA_YEAR = 2020

# Relative paths to original databases' main data files
JRC_FILE_PATH = './jrc_db_original/JRC_OPEN_UNITS.csv'
WRI_FILE_PATH = './wri_db_original/global_power_plant_database.csv'
CPP_FILE_PATH = './cpp_db_original/opsd-conventional_power_plants-2020-10-01/conventional_power_plants_EU.csv'

# name of the file with entsoe data
ENTSOE_FILE_NAME = 'all_countries_entsoe.xlsx'

# the distance, below which two plants in the same type group and in the same country,
# will be considered the same plant regardless of their other characteristics (in km)
UNCONDITIONAL_DISTANCE_CRITERION = 0.5

### Advanced config

ADJUST_UP = False
ADJUST_DOWN = True

# Map of types of plants/fuels used in JRC database and their output file counterparts
TYPES_JRC_DICT = {
    'Fossil Brown coal/Lignite': 'Lignite',
    'Fossil Hard coal': 'Coal',
    'Hydro Run-of-river and poundage': 'Hydro',
    'Biomass': 'Bioenergy',
    'Wind Onshore': 'Wind',
    'Fossil gas': 'Gas_CCGT',
    'Waste': 'Waste',
    'Fossil Gas': 'Gas_CCGT',
    'Fossil Oil shale': 'OilOther',
    'Hydro Pumped Storage': 'Hydro',
    'Fossil Peat': 'Other',
    'Other': 'OilOther',
    'Marine': 'Wave and Tidal',
    'Nuclear': 'Nuclear',
    'Wind Offshore': 'Wind',
    'Fossil Hard Coal': 'Coal',
    'Geothermal': 'Geothermal',
    'Fossil Coal-derived gas': 'Gas_CCGT',
    'Fossil Oil': 'OilOther',
    'Hydro Water Reservoir': 'Hydro',
    'Solar': 'Solar'}

# Map of types of plants/fuels used in WRI database and their output file counterparts
TYPES_WRI_DICT = {
    'Geothermal': 'Geothermal',
    'Biomass': 'Bioenergy',
    'Wind': 'Wind',
    'Nuclear': 'Nuclear',
    'Storage': 'Storage',
    'Hydro': 'Hydro',
    'Cogeneration': 'Cogeneration',
    'Gas': 'Gas_CCGT',
    'Waste': 'Waste',
    'Coal': 'Coal',
    'Wave and Tidal': 'Wave and Tidal',
    'Solar': 'Solar',
    'Other': 'OilOther',
    'Oil': 'OilOther'}

# Map of types of plants/fuels used in CPP database and their output file counterparts
TYPES_CPP_DICT = {
    'Oil Combined cycle': 'OilOther',
    'Hydro Pumped storage': 'Hydro',
    'Biomass and biogas Combustion Engine': 'Bioenergy',
    'Biomass and biogas Steam turbine': 'Bioenergy',
    'Oil Gas turbine': 'OilOther',
    'Lignite Steam turbine': 'Lignite',
    'Natural gas Steam turbine': 'Gas_ST',
    'Hard coal chp': 'Coal',
    'Other fuels Storage technologies': 'Storage',
    'Natural gas Gas turbine': 'Gas_OCGT',
    'Hydro RES': 'Hydro',
    'Other fuels Gas turbine': 'OilOther',
    'Other fuels Combined cycle': 'OilOther',
    'Hard coal Combined cycle': 'Coal',
    'Hard coal Gas turbine': 'Coal',
    'Nuclear Steam turbine': 'Nuclear',
    'Waste Combined cycle': 'Waste',
    'Waste Steam turbine': 'Waste',
    'Other fossil fuels Combustion Engine': 'OilOther',
    'Natural gas Combustion Engine': 'Gas_OCGT',
    'Natural gas Combined cycle': 'Gas_CCGT',
    'Non-renewable waste Combined cycle': 'Waste',
    'Hydro Run-of-river': 'Hydro',
    'Other fuels Steam turbine': 'OilOther',
    'Non-renewable waste Steam turbine': 'Waste',
    'Mixed fossil fuels Steam turbine': 'OilOther',
    'Hydro Reservoir': 'Hydro',
    'Hard coal Steam turbine': 'Coal',
    'Other fossil fuels Steam turbine': 'OilOther',
    'Biomass and biogas Gas turbine': 'Bioenergy',
    'Oil Steam turbine': 'OilOther',
    'Bioenergy Steam turbine': 'Bioenergy',
    'Hydro Pumped storage with natural inflow': 'Hydro'}

# if some, distinct, types of power plants can be merged, they should be marked as the same
# type group. These groups are specified here.
TYPES_TO_GROUPS = {
    'Bio_CCS': 'Bio_CCS',
    'Bioenergy': 'Bioenergy',
    'Coal': 'Coal',
    'Coal_CCS': 'Coal_CCS',
    'Gas_CCGT': 'Gas_CCGT',
    'Gas_CCS': 'Gas_CCS',
    'Gas_OCGT': 'Gas_OCGT',
    'Gas_ST': 'Gas_ST',
    'Geothermal': 'Geothermal',
    'Lignite': 'Lignite',
    'Nuclear': 'Nuclear',
    'OilOther': 'OilOther',
    'Gas_OCGT': 'Gas',
    'Gas_CCS': 'Gas',
    'Gas_CCGT': 'Gas',
    'Gas_ST': 'Gas'}

# the distance, below which two plants in the same type group and in the same country,
# will be considered the same plant, if and only if other conditional criteria are met (in km)
CONDITIONAL_DISTANCE_CRITERION = 5

# the relative difference in capacity, below which two plants in the same type group and in
# the same country, will be considered the same plant,
# if and only if other conditional criteria are met
CONDITIONAL_CAPACITY_CRITERION = 0.1

# the difference in comissioning year, below which two plants in the same type group and in
# the same country, will be considered the same plant,
# if and only if other conditional criteria are met (in years)
CONDITIONAL_COMISSIONING_CRITERION = 3

### Constants based on config

# List of all types groups, constructed according to the dictionary
TYPES_GROUPS = list(set([TYPES_TO_GROUPS.get(t, t) for t in TYPES]))

# Reverse of the COUNTRIES_NAME_TO_ABBR: map of countries abbreviations to their coresponding names
COUNTRIES_ABBR_TO_NAME = {v: k for k, v in COUNTRIES_NAME_TO_ABBR.items()}

GROUPS_TO_TYPES = {}
for k, v in TYPES_TO_GROUPS.items():
    GROUPS_TO_TYPES.setdefault(v, []).append(k)
