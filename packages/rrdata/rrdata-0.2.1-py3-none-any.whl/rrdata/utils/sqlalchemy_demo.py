from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from rrdata.utils.rqSetting import setting
import psycopg2

from rrdata.utils.rqLogs import rq_util_log_info

passwd_postgres = setting["PGSQL_PASSWORD"]
host_ip = setting["IP_DATABASE_ALIYUN"]
db_name = setting["DATABASE"]
table_name = "cities"

DATABASE_URL = f"postgresql+psycopg2://postgres:{passwd_postgres}@{host_ip}:5432/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)
rq_util_log_info(engine)
# declarative base class
Base = declarative_base()

# an example mapping using the base
class City(Base):
    __tablename__ = table_name

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    population = Column(Integer)
   
def add_city(session: engine, name: str, population: int):
    new_city = City(name=name, population=population)
    rq_util_log_info(f" add new_city: name: {name}, population: {population}")
    session.add(new_city)
    return new_city

if __name__ == '__main__':
    add_city(engine,"shenzhen",1700)