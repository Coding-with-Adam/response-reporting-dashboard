from utils.database_connector import read_query, write_query
import pandas as pd

def select_countries():
	select_countries_query_string = f"""
	SELECT * FROM country;
	"""
	df = read_query(select_countries_query_string)
	return df
	
#___To be removed once countries table is populated in the database___#
def add_country(in_country_name):
	df = select_countries()
	if in_country_name in df["country_name"].values:
		return "Existing country"

	add_country_query_string = f"""
	INSERT INTO country(country_name)
	VALUES("{in_country_name}");
	"""
	result = write_query(add_country_query_string)
	return result


def select_entities():
	select_entities_query_string = f"""
	SELECT * FROM entity;
	"""
	df = read_query(select_entities_query_string)
	return df

def add_entity(in_affiliation, in_website, in_signatory_status, in_country):
	df = select_entities()
	if in_affiliation in df["entity_name"].values:
		return "Existing entity"

	add_entity_query_string = f"""
	INSERT INTO entity (entity_name, website, signatory_of_code_of_practice_on_disinformation, country_name)
	VALUES ("{in_affiliation}", "{in_website}", "{in_signatory_status}", "{in_country}");
	"""
	result = write_query(add_entity_query_string)
	return result


def select_users():
	select_users_query_string = f"""
	SELECT * FROM vetted_user;
	"""
	df = read_query(select_users_query_string)
	return df

def add_user(in_email, in_first_name, in_last_name, in_affiliation):
	df = select_users()
	if in_email in df["work_email"].values:
		return "Existing User"

	add_user_query_string = f"""
	INSERT INTO vetted_user(work_email, first_name, last_name, affiliation_name)
	VALUES ("{in_email}", "{in_first_name}", "{in_last_name}", "{in_affiliation}");
	"""
	result = write_query(add_user_query_string)
	return result


def register_user(in_email, in_first_name, in_last_name, in_affiliation, in_website, in_signatory_status, in_country):
	add_country(in_country)
	add_entity(in_affiliation, in_website, in_signatory_status, in_country)
	return add_user(in_email, in_first_name, in_last_name, in_affiliation)