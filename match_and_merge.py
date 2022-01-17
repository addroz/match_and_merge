import sys

import geopy.distance
import pandas as pd

import config


def remove_trailing_whitespaces(df):
    return df.replace({"^\s*|\s*$":""}, regex = True)

def show_progress_bar(i, n):
    j = (i + 1) / n
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %d%%' % ('='*(int(50*j)), 100*j))
    sys.stdout.flush()

def remove_nans(db):
    db = db[db['country'].notna()]
    db = db[db['type'].notna()]
    db = db[db['lat'].notna()]
    db = db[db['lon'].notna()]
    db = db[db['cap'].notna()]
    return db

def get_type_category(types):
    return types.replace(config.TYPES_TO_GROUPS)

def read_and_prepare_data():
    jrc_db = remove_trailing_whitespaces(pd.read_csv(config.JRC_FILE_PATH, low_memory = False))
    wri_db = remove_trailing_whitespaces(pd.read_csv(config.WRI_FILE_PATH, low_memory = False))
    cpp_db = remove_trailing_whitespaces(pd.read_csv(config.CPP_FILE_PATH, low_memory = False))

    jrc_db = jrc_db[(jrc_db['year_commissioned'].isna()) |
                    (jrc_db['year_commissioned'] <= config.DATA_YEAR)]
    jrc_db = jrc_db[(jrc_db['year_decommissioned'].isna()) |
                    (jrc_db['year_decommissioned'] >= config.DATA_YEAR)]
    jrc_db = jrc_db[['eic_p', 'country', 'type_g', 'lat', 'lon', 'capacity_g', 'year_commissioned']]
    wri_db = wri_db[['country_long', 'primary_fuel', 'latitude', 'longitude', 'capacity_mw',
        'commissioning_year']]

    cpp_db = cpp_db[['country', 'energy_source', 'technology', 'lat', 'lon', 'capacity', 'commissioned']]
    cpp_db = cpp_db.replace(config.COUNTRIES_ABBR_TO_NAME)
    cpp_db['energy_source'] = cpp_db['energy_source'] + ' ' + cpp_db['technology']
    cpp_db.drop(columns=['technology'], inplace=True)
    cpp_db = cpp_db[~cpp_db['energy_source'].isna()]

    jrc_db = jrc_db.groupby(by=['eic_p', 'country', 'type_g']).agg({'lat': 'mean', 'lon': 'mean',
        'capacity_g': 'sum', 'year_commissioned': 'min'})
    jrc_db.reset_index(inplace=True)
    jrc_db.drop(columns=['eic_p'], inplace=True)

    jrc_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned']
    wri_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned']
    cpp_db.columns = ['country', 'type', 'lat', 'lon', 'cap', 'commissioned']

    wri_db.loc[wri_db['country'] == 'Czech Republic', 'country'] = 'Czechia'

    wri_db = wri_db[wri_db['country'].isin(config.COUNTRIES)]
    jrc_db = jrc_db[jrc_db['country'].isin(config.COUNTRIES)]
    cpp_db = cpp_db[cpp_db['country'].isin(config.COUNTRIES)]

    jrc_db = jrc_db.replace({'type': config.TYPES_JRC_DICT})
    wri_db = wri_db.replace({'type': config.TYPES_WRI_DICT})
    cpp_db = cpp_db.replace({'type': config.TYPES_CPP_DICT})

    return jrc_db, wri_db, cpp_db

def is_the_same(plant1, plant2):
    coord1 = (plant1['lat'], plant1['lon'])
    coord2 = (plant2['lat'], plant2['lon'])

    distance = geopy.distance.distance(coord1, coord2).km

    if distance < config.UNCONDITIONAL_DISTANCE_CRITERION:
        return True

    if distance > 5:
        return False

    if plant1['cap'] == 0 and plant2['cap'] != 0:
        return False
    elif plant2['cap'] == 0 and plant1['cap'] != 0:
        return False
    elif plant1['cap']/plant2['cap'] < (1 - config.CONDITIONAL_CAPACITY_CRITERION) or \
        plant1['cap']/plant2['cap'] > (1 + config.CONDITIONAL_CAPACITY_CRITERION):
        return False

    if plant1['commissioned'] is not None and \
        plant2['commissioned'] is not None and \
        abs(plant1['commissioned'] - plant2['commissioned']) < \
            config.CONDITIONAL_COMISSIONING_CRITERION:
        return False

    return True

def get_row_with_better_information(row1, row2):
    if row1['commissioned'] is not None:
        return row1
    return row2

def merge_two_db(db1, db2, prefered_second_type = False):
    result = pd.DataFrame(columns = db1.columns)

    for _, row in db1.iterrows():
        id_to_remove = []
        row2_to_append = None
        for index2, row2 in db2.iterrows():
            if is_the_same(row, row2):
                row2_to_append = row2
                id_to_remove.append(index2)

        if row2_to_append is None:
            result = result.append(row)
        elif prefered_second_type:
            result = result.append(row2_to_append)
        else:
            result = result.append(get_row_with_better_information(row, row2_to_append))

        db2.drop(id_to_remove, inplace = True)

    result = result.append(db2)
    return result

def merge_db_by_type_and_country(db1, db2, db3):
    db12 = merge_two_db(db1, db2)
    result = merge_two_db(db12, db3, prefered_second_type = True)

    return result

def fill_dictionary(dictionary, keys_list, filler):
    for key in keys_list:
        if key not in dictionary.keys():
            dictionary[key] = filler

    return dictionary

def merge_db_by_type(db1, db2, db3):
    db1_by_country = dict([(y, x) for y, x in db1.groupby(db1['country'])])
    db2_by_country = dict([(y, x) for y, x in db2.groupby(db2['country'])])
    db3_by_country = dict([(y, x) for y, x in db3.groupby(db3['country'])])

    db1_by_country = fill_dictionary(db1_by_country, config.COUNTRIES, pd.DataFrame(columns = db1.columns))
    db2_by_country = fill_dictionary(db2_by_country, config.COUNTRIES, pd.DataFrame(columns = db1.columns))
    db3_by_country = fill_dictionary(db3_by_country, config.COUNTRIES, pd.DataFrame(columns = db1.columns))

    db_merged_by_country = pd.DataFrame(columns = db1.columns)
    for country in config.COUNTRIES:
        db_merged_by_country = pd.concat([db_merged_by_country,
            merge_db_by_type_and_country(db1_by_country[country], db2_by_country[country], db3_by_country[country])])

    return db_merged_by_country



def get_dbs_by_type(t, db1, db2, db3):
    if t == 'Nuclear':
        return (db1, pd.DataFrame(columns = db1.columns), pd.DataFrame(columns = db1.columns))
    if t in ('Coal', 'Lignite'):
        return (db1, pd.DataFrame(columns = db1.columns), db3)
    return (db1, db2, db3)

def merge_db(db1, db2, db3):
    n = len(config.TYPES_GROUPS)
    show_progress_bar(0, n + 1)

    db1 = remove_nans(db1)
    db2 = remove_nans(db2)
    db3 = remove_nans(db3)

    db1_by_type = dict([(y, x) for y, x in db1.groupby(get_type_category(db1['type']))])
    db2_by_type = dict([(y, x) for y, x in db2.groupby(get_type_category(db2['type']))])
    db3_by_type = dict([(y, x) for y, x in db3.groupby(get_type_category(db3['type']))])

    db1_by_type = fill_dictionary(db1_by_type, config.TYPES_GROUPS, pd.DataFrame(columns = db1.columns))
    db2_by_type = fill_dictionary(db2_by_type, config.TYPES_GROUPS, pd.DataFrame(columns = db1.columns))
    db3_by_type = fill_dictionary(db3_by_type, config.TYPES_GROUPS, pd.DataFrame(columns = db1.columns))

    db_merged_by_type = pd.DataFrame(columns = db1.columns)

    for (t, i) in zip(config.TYPES_GROUPS, list(range(n))):
        db1_of_type, db2_of_type, db3_of_type = get_dbs_by_type(t, db1_by_type[t], db2_by_type[t], db3_by_type[t])
        db_merged_by_type = pd.concat([db_merged_by_type,
                merge_db_by_type(db1_of_type, db2_of_type, db3_of_type)])
        show_progress_bar(i + 1, n + 1)

    print('\n')
    return db_merged_by_type

def group_db(db, years):
    cap_by_year = pd.DataFrame(columns=['year', 'ID-year'] + config.TYPES)
    previous_row = None
    for year in years:
        row = (db[(db['commissioned'].isna()) | (db['commissioned'] <= year)]\
                .groupby(['type']).sum())['cap']/1000
        if previous_row is not None:
            row, previous_row = row - previous_row, row
        else:
            previous_row = row

        row['ID-year'] = year
        cap_by_year = cap_by_year.append(row)

    cap_by_year = cap_by_year.fillna(0)
    cap_by_year['year'] = config.DATA_YEAR
    return cap_by_year

if __name__ == '__main__':
    print('Merging databases')
    jrc_db, wri_db, cpp_db = read_and_prepare_data()

    merged = merge_db(jrc_db, wri_db, cpp_db)
    merged = merged.reset_index()
    merged = merged.drop(columns = ['index'])
    merged.to_csv('merged.csv')

    writer = pd.ExcelWriter('grouped.xlsx', engine='xlsxwriter')
    for country in config.COUNTRIES:
        print(f'Preparing output for {country}')
        grouped = group_db(merged[merged['country'] == country], config.YEARS)
        grouped = grouped.reset_index()
        grouped = grouped.drop(columns = ['index'])
        sum_for_country = grouped.drop(['year', 'ID-year'], axis=1).to_numpy().sum()
        print(f'Sum of all available capacity for {country}: {sum_for_country}')
        grouped.to_excel(writer, sheet_name = config.COUNTRIES_NAME_TO_ABBR[country], index = False)

    print('Results saved to: grouped.xlsx')
    writer.save()
