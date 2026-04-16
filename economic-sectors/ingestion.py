#!/usr/bin/env python
# coding: utf-8

import io
import os

from translate_dicts import map_list

import dlt
import requests
import pandas as pd

# Configurations
OWNER = "DanielIramain"
REPO = "argentina-economic-sectors"
TAG = "v1.0.0"
SECTORS = ['apicola', 'tabaco', 'te', 'trigo', 'maiz', 'energias-alternativas', 'arroz', 'algodonera-textil', 'fruticola-fruta-de-carozo', 'construccion', 'forestal-papel-y-muebles', 'vitivinicultura', 'telecomunicaciones', 'comercio-interno', 'automotriz-y-autopartista', 'maquinaria-agricola', 'servicios-turisticos', 'mineria-metalifera-y-rocas-de-aplicacion', 'hidrocarburos', 'legumbres', 'azucar', 'carnica-porcina', 'limon', 'lactea', 'fruticola-citricos-dulces', 'carnica-vacuna', 'fruticola-manzana-y-pera', 'ovinos-lana-y-carne', 'software-y-servicios-informaticos', 'oleaginosa', 'servicios-de-investigacion-y-desarrollo', 'industrias-culturales', 'petroquimica-plastica', 'carnica-aviar', 'yerba-mate', 'pesca-y-puertos-pesqueros', 'olivicola']
URL_BASE = f'https://github.com/{OWNER}/{REPO}/releases/download/{TAG}/'

# Columns to translate in cleaning process
columns_to_translate = ['sector_name', 'name_frequency', 'coverage_name', 'reach_type']

def clean_format_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and formats data before loading."""
    # Renaming columns
    df.columns = [
        'sector_id', 'sector_name', 'variable_id', 'activity_product_name', 
        'indicator', 'unit_of_measure', 'source', 'name_frequency', 
        'coverage_name', 'reach_type', 'reach_id', 'reach_name', 'index_time', 'value'
    ]

    # Text normalization: lowercase, remove accents, and strip whitespace
    cols = df.select_dtypes(include=[object]).columns
    df[cols] = df[cols].apply(
        lambda x: x.str.normalize('NFKD')
                   .str.encode('ascii', errors='ignore')
                   .str.decode('utf-8')
                   .str.lower()
    )

    # Drop column and fill NaN values
    df = df.drop(columns=['reach_id'], errors='ignore')
    df['value'] = df['value'].fillna(0)
    
    # Round 'value' to 2 decimal places
    df['value'] = df['value'].round(2)

    # Translate columns content using the mapping dictionaries
    mapping_index = 0

    for column in columns_to_translate:    
        m = map_list[mapping_index]

        df[column] = df[column].map(m).fillna(df[column])
        mapping_index += 1
    
    return df

@dlt.resource(name="economic_sectors", write_disposition="replace")
def economic_sectors_resource():
    # Output path for the generated CSV file
    output_path = "data/sectors.csv"
    os.makedirs("data", exist_ok=True)
    
    # If the output file already exists, remove it to avoid appending to old data
    if os.path.exists(output_path):
        os.remove(output_path)

    for i, sector in enumerate(SECTORS):
        filename = f"{sector}.csv"
        download_url = f"{URL_BASE}{filename}"
        
        print(f"Downloading-processing: {filename}...")
        response = requests.get(download_url)
        response.raise_for_status()
        
        # read CSV on memory (encoding=latin1 to handle special characters)
        df = pd.read_csv(io.BytesIO(response.content), encoding='latin1')
        
        # Transform before loading
        df_cleaned = clean_format_data(df)

        # WRITE TO CSV:
        # - mode='a' to sector append to the file (instead of overwriting it).
        # - header=True to keep the header only in the first iteration (avoid repeating it).
        first_row = (i == 0)
        df_cleaned.to_csv(output_path, mode='a', index=False, header=first_row)
        
        yield df_cleaned

pipeline = dlt.pipeline(
    pipeline_name="argentina_economic_sectors",
    destination="postgres",
    dataset_name="sectors",
    )

load_info = pipeline.run(economic_sectors_resource(), table_name="economic_sectors")

print(load_info)