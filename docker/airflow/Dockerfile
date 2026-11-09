FROM apache/airflow:2.10.5-python3.11

# Spark needs Java
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
# works on both Intel and Apple Silicon machines
RUN ln -s "$(dirname "$(dirname "$(readlink -f "$(which java)")")")" /usr/lib/jvm/default-java
ENV JAVA_HOME=/usr/lib/jvm/default-java

USER airflow
# folder for Spark's downloaded jars; open permissions so any user id can write to it
RUN mkdir -p /home/airflow/.ivy2 && chmod 777 /home/airflow/.ivy2
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# dbt gets its own virtual environment so its packages never clash with Airflow's.
# dbt-core is pinned on purpose: dbt-postgres alone can pull in an incompatible dbt-core release.
RUN python -m venv /home/airflow/dbt-venv \
 && /home/airflow/dbt-venv/bin/pip install --no-cache-dir dbt-core==1.8.9 dbt-postgres==1.8.2
ENV PATH="${PATH}:/home/airflow/dbt-venv/bin"
