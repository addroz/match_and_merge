
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
TYPES = ['Lignite', 'Coal', 'Hydro', 'Biomass', 'Wind', 'Gas', 'Waste', 'Oil', 'Storage', 'Other',
    'Wave and Tidal', 'Nuclear', 'Geothermal', 'Solar', 'Cogeneration']

# Map of types of plants/fuels used in JRC database and their output file counterparts
TYPES_JRC_DICT = {
    'Fossil Brown coal/Lignite': 'Lignite',
    'Fossil Hard coal': 'Coal',
    'Hydro Run-of-river and poundage': 'Hydro',
    'Biomass': 'Biomass',
    'Wind Onshore': 'Wind',
    'Fossil gas': 'Gas',
    'Waste': 'Waste',
    'Fossil Gas': 'Gas',
    'Fossil Oil shale': 'Oil',
    'Hydro Pumped Storage': 'Hydro',
    'Fossil Peat': 'Other',
    'Other': 'Other',
    'Marine': 'Wave and Tidal',
    'Nuclear': 'Nuclear',
    'Wind Offshore': 'Wind',
    'Fossil Hard Coal': 'Coal',
    'Geothermal': 'Geothermal',
    'Fossil Coal-derived gas': 'Gas',
    'Fossil Oil': 'Oil',
    'Hydro Water Reservoir': 'Hydro',
    'Solar': 'Solar'}

# Map of types of plants/fuels used in WRI database and their output file counterparts
TYPES_WRI_DICT = {
    'Geothermal': 'Geothermal',
    'Biomass': 'Biomass',
    'Wind': 'Wind',
    'Nuclear': 'Nuclear',
    'Storage': 'Storage',
    'Hydro': 'Hydro',
    'Cogeneration': 'Cogeneration',
    'Gas': 'Gas',
    'Waste': 'Waste',
    'Coal': 'Coal',
    'Wave and Tidal': 'Wave and Tidal',
    'Solar': 'Solar',
    'Other': 'Other',
    'Oil': 'Oil'}

# Relative paths to original databases
JRC_FILE_PATH = './jrc_db_original/JRC_OPEN_UNITS.csv'
WRI_FILE_PATH = './wri_db_original/global_power_plant_database.csv'
