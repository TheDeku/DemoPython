import mysql.connector

class DBConnection:
    """Class to connect to the database"""

    def __init__(self, host, user, password, bd):
        """Builder of the class"""
        self.host = host
        self.user = user
        self.password = password
        self.bd = bd

    def connect(self):
        """Method to connect to the database"""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.bd
            )
        except mysql.connector.Error as err:
            print("Error al conectar a la base de datos: {}".format(err))
            return False
        return True

    def disconnect(self):
        """Method to disconnect from the database"""
        self.conexion.close()

    def execute_query(self, sql):
        """Method to execute a query"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql)
            datos = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error al ejecutar la sentencia SQL: {}".format(err))
            return False
        return datos