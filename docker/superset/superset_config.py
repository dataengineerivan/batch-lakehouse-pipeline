import os

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]
# Superset keeps its own settings in a small SQLite file inside its volume
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"
