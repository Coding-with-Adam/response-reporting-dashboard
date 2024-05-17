import mysql.connector as connector
import pandas as pd


def get_connection(logon = "vost_user", pwd = "vost", db = "vost_db"):
	try:
		connection = connector.connect(user = logon, password = pwd, database = db)
		return connection
	except connector.Error as err:
		return err #Won't be used

def handle_query_connections(query_executing_function):
	def wrapper(query_statement):
		connection = get_connection()
		if connection:
			cursor = connection.cursor(buffered=True)
			query_result = query_executing_function(cursor, query_statement)
			cursor.close()
			connection.commit()
			connection.close()
			return query_result
		else:
			return connection #Won't be used
	return wrapper

@handle_query_connections
def write_query(cursor, query_statement):
	try:
		cursor.execute(query_statement)
		return "Success"
	except connector.Error as err:
		return err #Will be used

@handle_query_connections
def read_query(cursor, query_statement):
	try:
		cursor.execute(query_statement)
		column_names = cursor.column_names
		rows = cursor.fetchall()
		df = pd.DataFrame(rows, columns = column_names)
		return df
	except connector.Error as err:
		return err