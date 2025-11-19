
import json
import oracledb
from pandas import DataFrame


class OracleQueries:

    def __init__(self, can_write: bool = False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = "XEPDB1"

        
        with open("src/conexion/passphrase/authentication.oracle", "r") as f:
            self.user, self.passwd = f.read().strip().split(",")

        
        oracledb.init_oracle_client()

        self.conn = None
        self.cur = None

    def __del__(self):
        if hasattr(self, "cur") and self.cur:
            self.close()

    def connectionString(self):
        """
        Cria uma string de conexão Oracle usando service_name.
        """
        return oracledb.makedsn(
            host=self.host,
            port=self.port,
            service_name=self.service_name
        )

    def connect(self):
        """
        Realiza a conexão com o banco de dados Oracle.
        """
        self.conn = oracledb.connect(
            user=self.user,
            password=self.passwd,
            dsn=self.connectionString()
        )
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query: str) -> DataFrame:
        """
        Executa uma query e retorna os resultados em um DataFrame do Pandas.
        """
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])

    def sqlToMatrix(self, query: str) -> tuple:
        """
        Executa uma query e retorna uma matriz (lista de listas) e os nomes das colunas.
        """
        self.cur.execute(query)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query: str):
        """
        Executa uma query e retorna os resultados no formato JSON.
        """
        self.cur.execute(query)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query: str):
        """
        Executa um comando DML (INSERT, UPDATE, DELETE).
        """
        if not self.can_write:
            raise Exception("Can't write using this connection")

        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        if hasattr(self, "cur") and self.cur:
            try:
                self.cur.close()
            except Exception:
                pass


    def executeDDL(self, query: str):
        """
        Executa um comando DDL (CREATE, DROP, ALTER).
        """
        self.cur.execute(query)
