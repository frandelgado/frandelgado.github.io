import pandas as pd
import requests
import json
import os
from pathlib import Path
import progressbar

def get_country_code(country_name):
    url = f"https://restcountries.eu/rest/v2/name/{country_name}"
    response = requests.get(url)
    response_body = json.loads(response.content)
    return response_body[0]["alpha3Code"]

path = Path(__file__).parent / "../data/unenployment_rate.csv"
df = pd.read_csv(path, encoding = "ISO-8859-1", engine='python')

df['code'] = 'PLACEHOLDER'

df.loc[df.Country == "China, Hong Kong Special Administrative Region", 'Country'] = "HK"
df.loc[df.Country == "The former Yugoslav Republic of Macedonia", 'Country'] = "Macedonia"

bar = progressbar.ProgressBar(maxval=796, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

bar.start()
for index, row in df.iterrows():
    bar.update(index+1)
    country_name = row["Country"]
    code = get_country_code(country_name)
    df.loc[index, 'code'] = code
bar.finish()

df.to_csv(Path(__file__).parent / "../data/unenployment.csv")