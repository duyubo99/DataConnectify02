# -*- codeing = utf-8 -*-
# @Time : 2023-08-15 11:34
# @Autohor : Mr.du
# @File : my_sql_tool.py
# @Software : PyCharm
# pip install mysql-connector-python
import mysql.connector
import configparser


class MySQLTool:
    def __init__(self, config_file):
        self.config_file = config_file
        self.connections = {}

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def connect(self, database):
        if database not in self.connections:
            config = self.read_config()
            if database in config:
                host = config[database]['host']
                user = config[database]['user']
                password = config[database]['password']
                db = config[database]['database']
                connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db
                )
                self.connections[database] = connection

    def disconnect(self, database):
        if database in self.connections:
            connection = self.connections[database]
            if connection and connection.is_connected():
                connection.close()
            del self.connections[database]

    def execute_query(self, database, query):
        connection = self.connections.get(database)
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            return []

    def execute_insert(self, database, table, columns, values):
        connection = self.connections.get(database)
        if connection:
            cursor = connection.cursor()
            columns_str = ', '.join(columns)
            values_placeholder = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_placeholder})"
            cursor.executemany(insert_query, values)
            connection.commit()
            cursor.close()

    def execute_update(self, database, table, columns, values, condition):
        connection = self.connections.get(database)
        if connection:
            cursor = connection.cursor()
            set_list = ', '.join([f"{col} = %s" for col in columns])
            update_query = f"UPDATE {table} SET {set_list} WHERE {condition}"
            cursor.execute(update_query, values)
            connection.commit()
            cursor.close()