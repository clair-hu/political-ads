import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy

Base = declarative_base()
 
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, nullable=False, primary_key=True)
    user_name = Column(String(500), nullable=False)
    is_official = Column(Boolean, nullable=False)


class Regions(Base):
    __tablename__ = 'regions'
    region_id = Column(Integer, nullable=False, primary_key=True)
    region_name = Column(String(100), nullable=False)

class Balances(Base):
    __tablename__ = 'balances'
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False, primary_key=True)
    balance = Column(Integer, nullable=False)

    user = relationship('User', foreign_keys='Balances.user_id')

class Spendings(Base):
    __tablename__ = 'spendings'
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False, primary_key=True)
    region_id = Column(Integer, ForeignKey(Regions.region_id), nullable=False, primary_key=True)
    spending = Column(Integer, nullable=False)

    user = relationship('User', foreign_keys='Spendings.user_id')
    region = relationship('Regions', foreign_keys='Spendings.region_id')

class Mimics(Base):
    __tablename__ = 'mimics'
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False, primary_key=True)
    candidate_id = Column(Integer, ForeignKey(User.user_id), nullable=False, primary_key=True)

    user = relationship('User', foreign_keys='Mimics.user_id')
    candidate = relationship('User', foreign_keys='Mimics.candidate_id')

class FirebaseUsers(Base):
    __tablename__ = 'firebase_users'
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False, primary_key=True)
    firebase_id = Column(String(100), nullable=False)

    user = relationship('User', foreign_keys='FirebaseUsers.user_id')

db_host = "127.0.0.1" 
db_port = 3306
db_user = "root" # os.environ["DB_USER"]
db_pass = "windymarker" # os.environ["DB_PASS"]
db_name = "us_political_ads"  #  os.environ["DB_NAME"]
db_socket_dir = "/cloudsql" #  os.environ.get("DB_SOCKET_DIR", "/cloudsql")
cloud_sql_connection_name = "windy-marker-279018:us-west2:political-db" # os.environ["CLOUD_SQL_CONNECTION_NAME"]

engine = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        database=db_name,  # e.g. "my-database-name"
    ),
    # ... Specify additional properties here.

)

print(engine)
Base.metadata.create_all(engine)
