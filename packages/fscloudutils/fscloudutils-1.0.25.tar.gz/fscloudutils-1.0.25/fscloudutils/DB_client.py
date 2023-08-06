
import mysql.connector
import pandas as pd
from pandas import DataFrame

# dir_path = os.path.dirname(sys.argv[0])
# os.chdir(dir_path)
'''tables = ['fruit_variety', 'project', 'project_plot', 'plot', 'customer','caliber']'''


class DBClient:
    def __init__(self, db_server: str, db_user: str, db_password: str, db_name: str):
        self._connector = self.connect(db_server, db_user, db_password, db_name)

    def connect(self, db_server: str, db_user: str, db_password: str, db_name: str) -> mysql.connector.connection.MySQLConnection:
        return mysql.connector.connect(
            host=db_server,
            user=db_user,
            password=db_password,
            database=db_name)

    def execute(self, SQL_command: str, params=()) -> None:
        cursor = self._connector.cursor()
        cursor.execute(SQL_command, params=params)
        self._connector.commit()
        cursor.close()

    def select(self, SQL_command: str, params=()) -> pd.DataFrame:
        cursor = self._connector.cursor()
        cursor.execute(SQL_command, params=params)
        df = DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])
        cursor.close()
        return df

    def close_connection(self):
        self._connector.close()