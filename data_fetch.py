import io
import zipfile

import pandas as pd
import requests
import config

wri_db = requests.get(config.WRI_DB_LINK)
wri_db_unpacked = zipfile.ZipFile(io.BytesIO(wri_db.content))
wri_db_unpacked.extractall("./wri_db_original")

jrc_db = requests.get(config.JRC_DB_LINK)
jrc_db_unpacked = zipfile.ZipFile(io.BytesIO(jrc_db.content))
jrc_db_unpacked.extractall("./jrc_db_original")

