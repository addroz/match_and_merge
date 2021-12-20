import geopy.distance
import numpy as np
import pandas as pd
from pandas.core.reshape import concat
import config
import sys

def read_and_prepare_data():
    jrc_db = pd.read_csv(config.JRC_FILE_PATH, low_memory = False)
    wri_db = pd.read_csv(config.WRI_FILE_PATH, low_memory = False)

    jrc_db = jrc_db[['eic_p', 'country', 'type_g', 'lat', 'lon', 'capacity_g', 'year_commissioned',
        'year_decommissioned']]
    wri_db = wri_db[['country_long', 'primary_fuel', 'latitude', 'longitude', 'capacity_mw',
        'commissioning_year']]

    jrc_db = jrc_db.groupby(by=['eic_p', 'country', 'type_g']).agg({'lat': 'mean', 'lon': 'mean',
        'capacity_g': 'sum', 'year_commissioned': 'min', 'year_decommissioned': 'max'})
    jrc_db.reset_index(inplace=True)
    jrc_db = jrc_db.drop(columns=['eic_p'])

    jrc_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned', 'decommissioned']
    wri_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned']
    wri_db['decommissioned'] = np.NaN

    wri_db.loc[wri_db['country'] == 'Czech Republic', 'country'] = 'Czechia'

    wri_db = wri_db[wri_db['country'].isin(config.COUNTRIES)]
    jrc_db = jrc_db[jrc_db['country'].isin(config.COUNTRIES)]

    jrc_db = jrc_db.replace({'type': config.TYPES_JRC_DICT})
    wri_db = wri_db.replace({'type': config.TYPES_WRI_DICT})

    return jrc_db, wri_db

def is_the_same(plant1,  plant2):
    coord1 = (plant1.iloc[0]['lat'], plant1.iloc[0]['lon'])
    coord2 = (plant2.iloc[0]['lat'], plant2.iloc[0]['lon'])

    distance = geopy.distance.distance(coord1, coord2).km

    if distance > 1:
        return False

    if plant1.iloc[0]['cap']/plant2.iloc[0]['cap'] < 0.9 or \
        plant1.iloc[0]['cap']/plant2.iloc[0]['cap'] > 1.1:
        return False

    if plant1.iloc[0]['commissioned'] is not None and \
        plant2.iloc[0]['commissioned'] is not None and \
        plant1.iloc[0]['commissioned'] != plant2.iloc[0]['commissioned']:
        return False

    return(True)

def get_row_with_better_information(row1, row2):
    if row1.iloc[0]['commissioned'] is not None:
        if row1.iloc[0]['decommissioned'] is not None or \
            row2.iloc[0]['decommissioned'] is None:
            return row1
    elif row2.iloc[0]['commissioned'] is not None:
        return row2
    elif row2.iloc[0]['decommissioned'] is not None:
        return row2
    return row1

def merge_db_by_type_and_country(db1, db2):
    result = pd.DataFrame(columns = db1.columns)

    db1 = db1.sort_values(by = ['lat'])
    db2 = db2.sort_values(by = ['lat'])

    i = 0
    j = 0
    while i < db1.shape[0] and j < db2.shape[0]:
        row1 = db1.iloc[[i]]
        row2 = db2.iloc[[j]]

        if(is_the_same(row1, row2)):
            result.append(get_row_with_better_information(row1, row2))
            i = i + 1
            j = j + 1
        elif row1.iloc[0]['lat'] < row2.iloc[0]['lat']:
            result = result.append(row1)
            i = i + 1
        else:
            result = result.append(row2)
            j = j + 1

    return db1

def merge_db_by_type(db1, db2):
    db1_by_country = dict([(y, x) for y, x in db1.groupby(db1['country'])])
    db2_by_country = dict([(y, x) for y, x in db2.groupby(db2['country'])])

    db_merged_by_country = pd.DataFrame(columns = db1.columns)
    for country in config.COUNTRIES:
        if country not in db1_by_country.keys():
            if country in db2_by_country.keys():
                db_merged_by_country = pd.concat([db_merged_by_country, db2_by_country[country]])
        elif country not in db2_by_country.keys():
            db_merged_by_country = pd.concat([db_merged_by_country, db1_by_country[country]])
        else:
            db_merged_by_country = pd.concat([db_merged_by_country,
                merge_db_by_type_and_country(db1_by_country[country], db2_by_country[country])])

    return db_merged_by_country

def show_progress_bar(i, n):
    j = (i + 1) / n
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %d%%' % ('='*(int(50*j)), 100*j))
    sys.stdout.flush()

def merge_db(db1, db2):
    db1 = db1[db1['country'].notna()]
    db1 = db1[db1['type'].notna()]
    db1 = db1[db1['lat'].notna()]
    db1 = db1[db1['lon'].notna()]
    db1 = db1[db1['cap'].notna()]

    db2 = db2[db2['country'].notna()]
    db2 = db2[db2['type'].notna()]
    db2 = db2[db2['lat'].notna()]
    db2 = db2[db2['lon'].notna()]
    db2 = db2[db2['cap'].notna()]

    db1_by_type = dict([(y, x) for y, x in db1.groupby(db1['type'])])
    db2_by_type = dict([(y, x) for y, x in db2.groupby(db2['type'])])

    db_merged_by_type = pd.DataFrame(columns = db1.columns)

    n = len(config.TYPES)
    for (type, i) in zip(config.TYPES, list(range(n))):
        show_progress_bar(i, n)
        if type not in db1_by_type.keys():
            if type in db2_by_type.keys():
                db_merged_by_type = pd.concat([db_merged_by_type, db2_by_type[type]])
        elif type not in db2_by_type.keys():
            db_merged_by_type = pd.concat([db_merged_by_type, db1_by_type[type]])
        else:
            db_merged_by_type = pd.concat([db_merged_by_type,
                merge_db_by_type(db1_by_type[type], db2_by_type[type])])

    print('\n')
    return db_merged_by_type

def group_db(db, years):
    cap_by_year = pd.DataFrame(columns=['year', 'ID-year'] + config.TYPES)
    for year in years:
        row = (db[((db['commissioned'].isna()) | (db['commissioned'] <= year)) &
            ((db['decommissioned'].isna()) | (db['decommissioned'] >= year))]\
                .groupby(['type']).sum())['cap']
        row['ID-year'] = year
        cap_by_year = cap_by_year.append(row)

    cap_by_year = cap_by_year.fillna(0)
    cap_by_year['year'] = config.DATA_YEAR
    return cap_by_year

if __name__ == '__main__':
    print('Merging databases')
    jrc_db, wri_db = read_and_prepare_data()

    merged = merge_db(jrc_db, wri_db)
    merged = merged.reset_index()
    merged = merged.drop(columns = ['index'])
    merged.to_csv('merged.csv')

    writer = pd.ExcelWriter('grouped.xlsx', engine='xlsxwriter')
    for country in config.COUNTRIES:
        print(f'Preparing output for {country}')
        grouped = group_db(merged[merged['country'] == country], config.YEARS)
        grouped = grouped.reset_index()
        grouped = grouped.drop(columns = ['index'])
        grouped.to_excel(writer, sheet_name = config.COUNTRIES_NAME_TO_ABBR[country], index = False)

    print('Results saved to: grouped.xlsx')
    writer.save()
