#!/usr/bin/env python
# coding: utf-8

import os
import glob
import subprocess

import requests
import pandas as pd

sectors = ['apicola', 'tabaco', 'te', 'trigo', 'maiz', 'energias-alternativas', 'arroz', 'algodonera-textil', 'fruticola-fruta-de-carozo', 'construccion', 'forestal-papel-y-muebles', 'vitivinicultura', 'telecomunicaciones', 'comercio-interno', 'automotriz-y-autopartista', 'maquinaria-agricola', 'servicios-turisticos', 'mineria-metalifera-y-rocas-de-aplicacion', 'hidrocarburos', 'legumbres', 'azucar', 'carnica-porcina', 'limon', 'lactea', 'fruticola-citricos-dulces', 'carnica-vacuna', 'fruticola-manzana-y-pera', 'ovinos-lana-y-carne', 'software-y-servicios-informaticos', 'oleaginosa', 'servicios-de-investigacion-y-desarrollo', 'industrias-culturales', 'petroquimica-plastica', 'carnica-aviar', 'yerba-mate', 'pesca-y-puertos-pesqueros', 'olivicola']
url_base = 'https://github.com/DanielIramain/argentina-economic-sectors/releases/download/v1.0.0/'
download_dir = './data'

if not os.path.exists(download_dir):
    os.makedirs(download_dir)
    print(f"Created directory: {download_dir}")

def download_file(url_base, download_dir):
    for s in sectors:
        filename = s + '.csv'
        download_url = url_base + filename 
        
        # Local path for data storage (./data + filename)
        local_path = os.path.join(download_dir, filename)

        try:
            print(f"Downloading: {download_url}...")
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                
                # Open the file in binary mode and write the content in chunks
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Successfully downloaded: {filename} to {local_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")
        except IOError as e:
            print(f"Error saving file {filename} locally: {e}")

def create_dataframe(files_path: str) -> pd.DataFrame:
    # Get all csv files names in a list
    csv_files = glob.glob(files_path + "/*.csv")

    # Concat all csv files (sectors) in a single Pandas DataFrame
    # Files encoding: latin1
    df_sectors = pd.concat((pd.read_csv(f, encoding='latin1') for f in csv_files), ignore_index=True)
    # Sectors .csv
    sectors_data = df_sectors.to_csv(os.path.join(files_path, 'sectors.csv'), index=False, encoding='latin1')

    return df_sectors, sectors_data

if __name__ == "__main__":
    download_file(url_base, download_dir)
    df = create_dataframe(download_dir)