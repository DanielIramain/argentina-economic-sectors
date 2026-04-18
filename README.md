# Argentina Economic Sectors

## Problem description
This year, Argentina is facing an economic crisis (this is nothing new, regardless of when you read it). In a country with significant infrastructure deficiencies related to IT, public information and even the legal system, among many other examples, there is a constant need to assess the economic situation at an aggregated level. 

This project aims to solve that problem: using data from public institutions sources (but now consolidated in a single data system: https://datos.gob.ar/), it gives users a rapid overview of the real economic situation.  

1. Check the sector and activity with the highest value.
2. Check the sector and activity with the lowest value.
3. See how the real economy is distributed in Argentina (principal sectors and their production, and the main activities in each one).
4. Observe the evolution of a sector over time since the beginning of data collection in the 20th century.
5. Filter by region and time to narrow down the economic period of interest.

These functions and others are available via the data product in this project: a dashboard that shows the economic status of the country on a single page.

## System architecture

The system is based in a ETL pipeline: dlt is used to extract data from GitHub Release* and load it inside a local postgres database as backup or for testing. The transformed data is also uploaded to GCP Storage (using one bucket) and accesed via GCP BigQuery. The information is visualized then in a Looker Studio (now Data Studio) dashboard. The infrastructure is managed via Docker Compose which also contains Kestra as orchestrator for the stack and tasks process.

<div>
  <img src="https://github.com/DanielIramain/argentina-economic-sectors/blob/cloud/economic-sectors/diagrams/argentina-economic-sectors-arc.png"/>
</div>

The data flows is showed in this flowchart:

## Configuration (local setup)

### Basic requirements
Before following this step you must have installed:
- uv (i.e via pip) 
- Docker (if you are in Windows you will need WSL or Hyper-V backend to run Docker in that O.S)

### Setup
0. run uv sync (to create a isolated environment with required dependencies)
1. Modify the - /workspaces/argentina-economic-sectors/economic-sectors:/files line in Docker Compose according to your setup to make your local files visibles for Docker

### Configure dlt
2. Create a .dlt folder and a secrets.toml file inside (economic-sectors/.dlt/secrets.toml)
3. Configure the just created secrets.toml with this structure:

    [destination.postgres.credentials]\
    database = "sectors"\
    username = "example"\
    password = "example"\
    host = "localhost"\
    port = 5432

### Configure Docker Compose with secrets
4. Create a secrets folder and a db_user.txt file inside (economic-sectors/secrets/db_user.txt)
5. Create a db_password.txt file inside (economic-sectors/secrets/db_password.txt)
6. Put the postgres database password inside the db_password.txt file as well the user in db_user.txt (docker compose will read from this file to mount the local database service. There is no need for special characters as "" in the user or password)

### Enviroment variables
7. Create a .env file (or rename de .env_example) in the root directory for enviroments variables (docker compose will also read from this to mount Kestra service). The configuration is as it follows:

    POSTGRES_USER=example\
    POSTGRES_PASSWORD=example\
    KESTRA_POSTGRES_USER=example\
    KESTRA_POSTGRES_PASSWORD=Example1234\
    KESTRA_USER=example@example.com\
    KESTRA_PASSWORD=Example1234

### Cloud configuration (GCP)
8. Create a new GCP project
9. Create, download and insert into the root directory the JSON with the service account from GCP using the new project (it has to be created in GCP before running the flow in the next steps). The service account will need permisssions to GCP Storage and GCP BigQuery.

### Encode
10. Run the encode.sh (or copy-paste in terminal inside root directory) to encode the enviroments variables (Kestra will use the encode credentials to running the flows)

### Configure Kestra
11. Import the flows from ./flows folder inside Kestra (via terminal or using the UI)

With this, the data will be loaded in the local database (you can check it using uvx pgcli in a new terminal) and also will be avalible in GCP. If you followed the steps, the structure of the project should look as it follows:

    .
    ├── Dockerfile
    ├── README.md
    ├── diagrams
    │   └── argentina-economic-sectors-arc.png
    ├── docker-compose.yml
    ├── encode.sh
    ├── flows
    │   ├── economic-sectors.gcp_kv.yaml
    │   └── economic-sectors.load_economic_sectors.yaml
    ├── ingestion.py
    ├── pyproject.toml
    ├── queries
    │   └── data-studio-query.sql
    ├── secrets
    │   ├── db_password.txt
    │   └── db_user.txt
    ├── service-account.json
    ├── translate_dicts.py
    └── uv.lock

## Data product 
The dashboard is currently avalible in lecture mode at: [Argentina economic sectors dashboard](https://datastudio.google.com/reporting/7a47d125-83b1-48e0-a689-a9bed02a2e93)

## Considerations
* The original data was obtained in [this source from Argentina public data](https://datos.gob.ar/dataset/ssprys-indicadores-sectoriales-provinciales). To avoid security issues, the data was 'moved' from the original source to a GitHub Release repository for demo purposes, as the source didn't have an SSL certificate during the development of the project. To avoid excessive complexity, the automation script used to check and load the data into the release is not part of the project. 
