===// Temporary README.md //===
===// Before following this step you must have installed uv (i.e via pip) and Docker //===

0. run uv sync (to create a isolated environment)
1. Modify the - /workspaces/argentina-economic-sectors/economic-sectors:/files line in Docker Compose according to your setup to make your local files visibles for Docker
2. Create a .dlt folder and a secrets.toml file inside (economic-sectors/.dlt/secrets.toml)
3. Configure the just created secrets.toml
4. Create a secrets folder and a db_password.txt file inside (economic-sectors/secrets/db_password.txt)
5. Create a db_user.txt file (economic-sectors/secrets/db_user.txt)
6. Put the postgres database password inside the db_password.txt file as well the user in db_user.txt (docker compose will read from this file to mount the local database service)
7. Create a .env file in the root directory for enviroments variables (docker compose will also read from this to mount Kestra service)
8. Create a new GCP project
9. Create, download and insert into the root directory the JSON with the service account from GCP using the new project
10. Run the encode.sh to encode the enviroments variables (Kestra will use the encode credentials to running the flows)
11. Import the flows inside Kestra
12. Before running the flows in Kestra, change the .env postgres_user configuration inside the ingestion flow (i.e DESTINATION__POSTGRES__CREDENTIALS__USERNAME: "example")