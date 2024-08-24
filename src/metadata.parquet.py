import pandas as pd
import sys
import requests
import pyarrow as pa
import pyarrow.parquet as pq

fname = "55637C4923B8B03EE0530A930132B03E"
URL = f"http://ville.montreal.qc.ca/pls/portal/url/ITEM/{fname}"
TMPDIR = 'src/.observablehq/cache/metadata.xlsx'

r = requests.get(url=URL,  headers={'User-Agent': 'Mozilla/5.0'})

def normalize_name(name):
    name = name.replace('–', '-')  # Replace en dash with hyphen
    name = name.replace('’', "'")   # Replace different apostrophes with standard apostrophe
    return name

with open(TMPDIR, 'wb') as f:
    f.write(r.content)

df = pd.read_excel(TMPDIR, sheet_name="01_Population, Densité", skiprows=2).iloc[:-4, :]
df.rename(columns={'Unnamed: 0': 'arrondissement', 'Population en 2016': '2016', 'Population en 2011': '2011'}, inplace=True)
df = df[~df.arrondissement.isin(['Autres villes', 'Ville de Montréal','AGGLOMÉRATION DE MONTRÉAL'])]
df['arrondissement'] = df['arrondissement'].apply(normalize_name)
df_long = df[['arrondissement', '2016', '2011']].melt(id_vars='arrondissement', var_name='year', value_name='population')

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()
table = pa.Table.from_pandas(df_long)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)