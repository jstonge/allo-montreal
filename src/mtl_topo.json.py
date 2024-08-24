import geopandas as gpd
import sys
import json
from topojson import Topology
import requests
from pathlib import Path


# MONTREAL DISTRICTS


mtl_datasets = "https://donnees.montreal.ca/dataset"
fname="districts-electoraux-2021.geojson"
URL=f"{mtl_datasets}/70acec75-c2b4-4d26-a399-facc7b0ad9bf/resource/d0c1467b-a551-42df-98b4-057e00a84275/download/{fname}"
TMPDIR = Path('src/.observablehq/cache/mtl_topo.json')

r = requests.get(url=URL,  headers={'User-Agent': 'Mozilla/5.0'})

if not TMPDIR.exists():
    with open(TMPDIR, 'wb') as f:
        f.write(r.content)

districts = gpd.read_file(TMPDIR)


# MONTREAL HYDRO

URL = f"https://donnees.montreal.ca/dataset/ead1ac6f-f37c-4326-a9b9-4508d94bbc45/resource/73d4571c-fd7a-465a-aa19-05c3b24222cc/download/hydrographie-2020.zip"
TMPDIR_ZIP = Path('src/.observablehq/cache/hydrographie-2020.zip')
TMPDIR = Path('src/.observablehq/cache/mtl_hydro.json')

r = requests.get(url=URL,  headers={'User-Agent': 'Mozilla/5.0'})

if not TMPDIR_ZIP.exists():
    with open(TMPDIR_ZIP, 'wb') as f:
        f.write(r.content)
    
    
hydro = gpd.read_file(TMPDIR_ZIP, layer='CARTO_DRA_EAU_JOUR')
WGS84 = hydro.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
hydro_simplified = hydro.simplify(tolerance=0.001)

# MTL

URL = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/montreal.geojson"
TMPDIR = Path('src/.observablehq/cache/mtl.json')

r = requests.get(url=URL,  headers={'User-Agent': 'Mozilla/5.0'})

if not TMPDIR.exists():
    with open(TMPDIR, 'wb') as f:
        f.write(r.content)
    
city = gpd.read_file(TMPDIR)
city = city.iloc[1:, :]


# MERGE (WIP; not sure i am doing the right thing)

topo_1 = Topology(districts).to_dict()
topo_2 = Topology(hydro_simplified).to_dict()
topo_3 = Topology(city).to_dict()

for key in topo_3['objects']['data']['geometries']:
    key['properties']['created_at'] = str(key['properties']['created_at'])
    key['properties']['updated_at'] = str(key['properties']['updated_at'])

multi_topo = {
    "type": "Topology",
    "objects": {
        "districts": topo_1['objects']['data'],
        "hydro": topo_2['objects']['data'],
        "city": topo_3['objects']['data'],
    },
    "bbox": topo_1['bbox'],
    "transform": topo_1['transform'],
    "arcs": topo_1['arcs']
}

sys.stdout.write(json.dumps(multi_topo))