FROM apache/superset:4.1.1

# Postgres driver so Superset can read the gold marts
USER root
RUN pip install --no-cache-dir psycopg2-binary==2.9.10
COPY superset_config.py /app/pythonpath/superset_config.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
USER superset

CMD ["/app/start.sh"]
