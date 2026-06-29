# -> Importation du module sqlalchemy pour interagir avec une base de données SQLite locale via SQLAlchemy
from sqlalchemy import create_engine
DATABASE_URL = "sqlite:///sqlalchemy_training.db"
engine = create_engine(DATABASE_URL, echo=True)

