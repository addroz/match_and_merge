import io
import zipfile

import pandas as pd
import requests

WRI_DB_LINK = "https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip?download=1"
JRC_DB_LINK = "https://zenodo.org/record/3574566/files/JRC-PPDB-OPEN.ver1.0.zip?download=1"


wri_db = requests.get(WRI_DB_LINK)
wri_db_unpacked = zipfile.ZipFile(io.BytesIO(wri_db.content))
wri_db_unpacked.extractall("./wri_db_original")

jrc_db = requests.get(JRC_DB_LINK)
jrc_db_unpacked = zipfile.ZipFile(io.BytesIO(jrc_db.content))
jrc_db_unpacked.extractall("./jrc_db_original")

