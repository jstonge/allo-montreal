import geopandas as gpd
import sys
import json
from topojson import Topology
import requests

mtl_datasets = "https://donnees.montreal.ca/dataset"
fname="districts-electoraux-2021.geojson"
URL=f"{mtl_datasets}/70acec75-c2b4-4d26-a399-facc7b0ad9bf/resource/d0c1467b-a551-42df-98b4-057e00a84275/download/{fname}"
TMPDIR = 'src/.observablehq/cache/mtl.json'

r = requests.get(url=URL,  headers={'User-Agent': 'Mozilla/5.0'})

with open(TMPDIR, 'wb') as f:
    f.write(r.content)

districts = gpd.read_file(TMPDIR)
topology = Topology({"districts": districts})
sys.stdout.write(json.dumps(topology.to_dict()))



# Example: Dissolve arrondissements to ensure they don't overlap within themselves
# arrondissement_dissolved = districts.dissolve(by='arrondissement').reset_index()

# city
# if not Path("src/data/Montreal.geojson").exists():
#     pass

# city = gpd.read_file("Montreal.geojson")

# drop kanawake
# city = city.iloc[1:, :]

# hydro comes as a shp file

# if not Path("hydrographie-2020.zip").exists():
#     url = f"https://donnees.montreal.ca/dataset/ead1ac6f-f37c-4326-a9b9-4508d94bbc45/resource/73d4571c-fd7a-465a-aa19-05c3b24222cc/download/hydrographie-2020.zip"
#     filename = wget.download(url)
    
# hydro = gpd.read_file("hydrographie-2020.zip", layer='CARTO_DRA_EAU_JOUR')
# WGS84 = hydro.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
# hydro_simplified = hydro.simplify(tolerance=0.001)

