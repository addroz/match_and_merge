import geopy.distance
import numpy as np
import pandas as pd

JRC_FILE_PATH = './jrc_db_original/JRC_OPEN_UNITS.csv'
WRI_FILE_PATH = './wri_db_original/global_power_plant_database.csv'

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Ireland', 'Hungary', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain',
    'Sweden', 'United Kingdom']

COUNTRIES_NAME_TO_ABBR = {'Austria':'AT', 'Belgium':'BE', 'Bulgaria':'BG', 'Croatia':'CH', 'Czechia':'CZ',
    'Denmark':'DK', 'Estonia':'ET', 'Finland':'FI', 'France':'FE', 'Germany':'DE', 'Greece':'HL',
    'Ireland':'IR', 'Hungary':'HU', 'Italy':'IT', 'Latvia':'LV', 'Lithuania':'LI', 'Luxembourg':'LU',
    'Malta':'MT', 'Netherlands':'NT', 'Norway':'NO', 'Poland':'PO', 'Portugal':'PT', 'Romania':'RO',
    'Slovakia':'SK', 'Slovenia':'SO', 'Spain':'ES', 'Sweden':'SW', 'United Kingdom':'UK'}

TYPES = ['Lignite', 'Coal', 'Hydro', 'Biomass', 'Wind', 'Gas', 'Waste', 'Oil', 'Storage', 'Other',
    'Wave and Tidal', 'Nuclear', 'Geothermal', 'Solar', 'Cogeneration']

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
    'Hydro Pumped Storage': 'Storage',
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


def read_and_prepare_data():

    jrc_db = pd.read_csv(JRC_FILE_PATH)
    wri_db = pd.read_csv(WRI_FILE_PATH)

    jrc_db = jrc_db[['country', 'type_g', 'lat', 'lon', 'capacity_p', 'year_commissioned', 'year_decommissioned']]
    wri_db = wri_db[['country_long', 'primary_fuel', 'latitude', 'longitude', 'capacity_mw', 'commissioning_year']]

    jrc_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned', 'decommissioned']
    wri_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned']
    wri_db['decommissioned'] = np.NaN

    wri_db.loc[wri_db['country'] == 'Czech Republic', 'country'] = 'Czechia'

    wri_db = wri_db[wri_db['country'].isin(COUNTRIES)]
    jrc_db = jrc_db[jrc_db['country'].isin(COUNTRIES)]

    jrc_db = jrc_db.replace({"type": TYPES_JRC_DICT})
    wri_db = wri_db.replace({"type": TYPES_WRI_DICT})

    return jrc_db, wri_db


def merge_db_by_type_and_country(db1, db2):
    pass

def merge_db_by_type(db1, db2):
    db1_by_country = dict([(y, x) for y, x in db1.groupby(db1['country'])])
    db2_by_country = dict([(y, x) for y, x in db1.groupby(db1['country'])])

    for country in COUNTRIES:
        if country not in db1_by_country.keys():
            if country not in db2_by_country.keys():
                return None
            return db2_by_country[country]

        elif country not in db2_by_country.keys():
            return db1_by_country[country]
        else:
            return merge_db_by_type(db1_by_country[country], db2_by_country[country])

def merge_db(db1, db2):
    db1_by_type = dict([(y, x) for y, x in db1.groupby(db1['type'])])
    db2_by_type = dict([(y, x) for y, x in db1.groupby(db1['type'])])

    for type in TYPES:
        if type not in db1_by_type.keys():
            if type not in db2_by_type.keys():
                return None
            return db2_by_type[type]

        elif type not in db2_by_type.keys():
            return db1_by_type[type]
        else:
            return merge_db_by_type(db1_by_type[type], db2_by_type[type])

if __name__ == '__main__':
    jrc_db, wri_db = read_and_prepare_data()

    print(set(jrc_db['type']))
    print(set(wri_db['type']))
    print(len(jrc_db['type']))
    print(len(wri_db['type']))

    print(wri_db.head())
    print(jrc_db.head())
