
# Countries for which the merging is performed and data saved
COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Ireland', 'Hungary', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain',
    'Sweden', 'United Kingdom']

# The map of countries names and their coresponding abbreviations, used in the output excel file
COUNTRIES_NAME_TO_ABBR = {'Austria':'AT', 'Belgium':'BE', 'Bulgaria':'BG', 'Croatia':'CH', 'Czechia':'CZ',
    'Denmark':'DK', 'Estonia':'ET', 'Finland':'FI', 'France':'FR', 'Germany':'DE', 'Greece':'HL',
    'Ireland':'IR', 'Hungary':'HU', 'Italy':'IT', 'Latvia':'LV', 'Lithuania':'LI', 'Luxembourg':'LU',
    'Malta':'MT', 'Netherlands':'NT', 'Norway':'NO', 'Poland':'PL', 'Portugal':'PT', 'Romania':'RO',
    'Slovakia':'SK', 'Slovenia':'SO', 'Spain':'ES', 'Sweden':'SW', 'United Kingdom':'UK'}

# Names of all the types of plants/fuels used in the output file
TYPES = ['Bio_CCS', 'Bioenergy', 'Coal', 'Coal_CCS', 'Gas_CCGT', 'Gas_CCS', 'Gas_OCGT',
    'Gas_ST', 'Geothermal', 'Lignite', 'Nuclear', 'OilOther']

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

# years for which the ouptut is generated
YEARS = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020]

# year of the data
DATA_YEAR = 2020

# Relative paths to original databases
JRC_FILE_PATH = './jrc_db_original/JRC_OPEN_UNITS.csv'
WRI_FILE_PATH = './wri_db_original/global_power_plant_database.csv'

# links to the websites from which we download both databases
WRI_DB_LINK = "https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip?download=1"
JRC_DB_LINK = "https://zenodo.org/record/3574566/files/JRC-PPDB-OPEN.ver1.0.zip?download=1"
