from utils.database_connector import read_query, write_query
import pandas as pd

def _add_country(in_country_name):
	select_countries_query_string = f"""
	SELECT * FROM country;
	"""
	df = read_query(select_countries_query_string)
	if in_country_name in df["country_name"].values:
		return "Success"

	add_country_query_string = f"""
	INSERT INTO country(country_name)
	VALUES("{in_country_name}");
	"""
	result = write_query(add_country_query_string)
	return result

def _add_affiliation(in_affiliation, in_website, in_signatory_status, in_country):
	select_entities_query_string = f"""
	SELECT * FROM entity WHERE entity_name = "{in_affiliation}";
	"""
	df = read_query(select_entities_query_string)
	if in_affiliation in df["entity_name"].values:
		return "Success"

	add_entity_query_string = f"""
	INSERT INTO entity (entity_name, website, signatory_of_code_of_practice_on_disinformation, country)
	VALUES ("{in_affiliation}", "{in_website}", "{in_signatory_status}", "{in_country}");
	"""
	result = write_query(add_entity_query_string)
	return result

def _add_user(in_email, in_first_name, in_last_name, in_affiliation):
	select_users_query_string = f"""
	SELECT * FROM vetted_user;
	"""
	df = read_query(select_users_query_string)
	if in_email in df["work_email"].values:
		return "Existing User"

	add_user_query_string = f"""
	INSERT INTO vetted_user(work_email, first_name, last_name, affiliation_name)
	VALUES ("{in_email}", "{in_first_name}", "{in_last_name}", "{in_affiliation}");
	"""
	result = write_query(add_user_query_string)
	return result

def register_user(in_email, in_first_name, in_last_name, in_affiliation, in_website, in_signatory_status, in_country):
	country_add_result = _add_country(in_country)
	entity_result = _add_affiliation(in_affiliation, in_website, in_signatory_status, in_country)
	user_add_result = _add_user(in_email, in_first_name, in_last_name, in_affiliation)

	return user_add_result