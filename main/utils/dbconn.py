import pymysql
import main.utils.config as config

class Database():

    def __init__(self):

        self.db = pymysql.connect(host=config.DB_HOST,
                                  db=config.DB_DATABASE,
                                  user=config.DB_USR,
                                  port=config.DB_PORT,
                                  password=config.DB_PASSWORD,
                                  charset='utf8mb4',
                                  connect_timeout=15
                                  )

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)    # DictCursor를 써야 Dictionary형태로 리턴한다.

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()
