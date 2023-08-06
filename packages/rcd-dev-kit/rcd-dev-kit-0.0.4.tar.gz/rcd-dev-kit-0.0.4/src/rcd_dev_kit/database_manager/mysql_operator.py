import os
from sqlalchemy import create_engine

class MysqlOperator:
    def __init__(self):
        mysql_host = os.environ.get("MYSQL_HOST")
        mysql_db = os.environ.get("MYSQL_DB")
        mysql_port = os.environ.get("MYSQL_PORT")
        mysql_user = os.environ.get("MYSQL_USER")
        mysql_password = os.environ.get("MYSQL_PASSWORD")
        self.engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}")