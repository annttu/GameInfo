# encoding: utf-8
import psycopg2
from config import config
import logging

logger = logging.getLogger()

class ConnectionError(Exception):
    pass

class OTTDStats(object):
    def __init__(self):
        self._connection = None
        self._server = config.get('database', 'server')
        self._database = config.get('database', 'database')
        self._user = config.get('database', 'username')
        self._password = config.get('database', 'password')
        self._port = config.get('database', 'port')


    def get_cursor(self):
        if not self._connection:
            self._connect()
        if self._connection:
            return self._connection.cursor()
        return None

    def commit(self):
        if self._connection:
            self._connection.commit()
            return
        else:
            raise ConnectionError("Cannot commit without connection")

    def _connect(self):
        try:
            self._connection = psycopg2.connect(dbname=self._database, host=self._server,
                                                user=self._user, port=self._port,
                                                password=self._password)
        except Exception as e:
            logger.exception(e)
            logger.error("Connection to database failed")
            raise ConnectionError(e)

    def addGameStats(self, clients_on, spectators_on, companies_on, server, start_date, game_date, alive=True):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO gameinfo_openttd_game (clients, spectators, companies, alive, server, start_date, game_date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                       (clients_on, spectators_on, companies_on, alive, server, start_date, game_date))
        self.commit()
        cursor.close()

    def addCompanyStats(self, company_name, clients, inaugurated_year, company_value, money, income, performance, password_protected):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO gameinfo_openttd_company (name, clients, inaunguarated_year, value, money, income, performance, password_protected) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (company_name, clients, inaugurated_year, company_value, money, income, performance,password_protected))
        self.commit()
        cursor.close()
