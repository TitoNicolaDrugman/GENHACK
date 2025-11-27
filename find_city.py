import geopandas as gpd
import pandas as pd
import os
import sys

GADM_FILE_PATH = os.path.join("data", "gadm_410_europe.gpkg")

def find_city_info(search_term):
    print(f"--- Ricerca di '{search_term}' in GADM ---")
    
    if not os.path.exists(GADM_FILE_PATH):
        print(f"errore: File non trovato in: {GADM_FILE_PATH}")
        return

    try:
        gdf = gpd.read_file(GADM_FILE_PATH, ignore_geometry=True)
    except TypeError:
        gdf = gpd.read_file(GADM_FILE_PATH)
        
    print(f"   database caricato. Totale record: {len(gdf)}")
    print(f"2. cerco corrispondenze per '{search_term}'")
    
    mask_city = gdf['NAME_2'].str.contains(search_term, case=False, na=False)
    mask_region = gdf['NAME_1'].str.contains(search_term, case=False, na=False)
    
    results = gdf[mask_city | mask_region]

    if results.empty:
        print(f"nessuna corrispondenza trovata per '{search_term}'.")
    else:
        print(f"trovati {len(results)} risultati:\n")
        
        columns_to_show = ['GID_0', 'NAME_0', 'NAME_1', 'NAME_2', 'TYPE_2']
        columns_to_show = [c for c in columns_to_show if c in results.columns]
        
        display_df = results[columns_to_show].copy()
        
        rename_map = {
            'GID_0': 'CODICE_PAESE',
            'NAME_0': 'PAESE',
            'NAME_1': 'REGIONE',
            'NAME_2': 'CITTÀ',
            'TYPE_2': 'TIPO'
        }
        display_df = display_df.rename(columns=rename_map)
        
        print(display_df.to_string(index=False))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city_to_find = sys.argv[1]
        find_city_info(city_to_find)
    else:
        city_to_find = input("inserisci il nome della città da cercare: ")
        find_city_info(city_to_find)