import psycopg2
import pandas as pd


class ConnectionToPostgres:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Connected to the PostgreSQL database")
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)
    
    def execute(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as error:
            print("Error while executing query", error)
            return None

    
    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("PostgreSQL connection is closed")