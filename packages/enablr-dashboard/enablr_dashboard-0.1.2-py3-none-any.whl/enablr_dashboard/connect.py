from sqlalchemy import create_engine
import toml
import psycopg2


class Connect:
    def __init__(self, conf_path, server='DB_STAGING') -> None:
        conf = toml.load(conf_path)[server]
        self.database = conf['DATABASE']
        self.user = conf['USER']
        self.password = conf['PASSWORD']
        self.host = conf['HOST']
        self.port = 5432
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
        )
        self.cur = self.conn.cursor()

    def engine(self):
        return create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

    def execute(self, query):
        self.cur.execute(query=query)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
