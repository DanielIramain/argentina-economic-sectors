FROM kestra/kestra:latest

USER root
RUN pip install requests pandas "dlt[postgres]" "dlt[parquet]" psycopg2-binary 

CMD ["server", "standalone"]