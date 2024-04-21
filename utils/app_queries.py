from utils.database_connector import read_query, write_query
import pandas as pd

#________________________________________SELECT Queries________________________________________#

def select_all_countries():
	select_countries_query_string = f"""
	SELECT * FROM country;
	"""
	df = read_query(select_countries_query_string)
	return df

def select_all_platforms():
	platform_query_string = f"""
	SELECT * FROM platform
	"""
	df = read_query(platform_query_string)
	return df

def select_all_entities():
	select_entities_query_string = f"""
	SELECT * FROM entity;
	"""
	df = read_query(select_entities_query_string)
	return df

def select_all_users():
	select_users_query_string = f"""
	SELECT * FROM vetted_user;
	"""
	df = read_query(select_users_query_string)
	return df

def verify_user(email_in):
	user_query_string = f"""
	SELECT
		CONCAT(first_name, ' ', last_name) AS full_name
	FROM vetted_user
	WHERE work_email = "{email_in}";
	"""
	df = read_query(user_query_string)
	if not df.empty:
		return df.iloc[0]["full_name"]
	return ""

def select_all_reports():
	reports_query_string = f"""
	SELECT
		rp.timestamp,
		CONCAT(vu.first_name, " ", vu.last_name) AS reporing_user,
		vu.affiliation_name AS reporting_entity,
		rp.platform_name AS platform,
		rp.url,
		rp.report_type,
		rp.screenshot_url,
		rp.answer_date,
		rp.platform_decision,
		rp.policy,
		rp.appeal
	FROM
		report AS rp
		INNER JOIN
		vetted_user AS vu
		ON vu.work_email = rp.reporting_user;
	"""
	df = read_query(reports_query_string)
	return df

def select_user_reports(email_in):
	reports_query_string = f"""
	SELECT
		timestamp,
		platform_name AS platform,
		url,
		report_type,
		screenshot_url,
		answer_date,
		platform_decision,
		policy,
		appeal
	FROM report
	WHERE reporting_user = "{email_in}"
	ORDER BY timestamp DESC;
	"""
	df = read_query(reports_query_string)
	return df

def select_reports_types():
	types_query_string = f"""
	SELECT * FROM report_classification;
	"""
	df = read_query(types_query_string)
	return df

#________________________________________INSERT Queries________________________________________#

def add_entity(in_affiliation, in_website, in_signatory_status, in_country):
	df = select_all_entities()
	if in_affiliation in df["entity_name"].values:
		return "Existing entity"

	add_entity_query_string = f"""
	INSERT INTO entity (entity_name, website, signatory_of_code_of_practice_on_disinformation, country_name)
	VALUES ("{in_affiliation}", "{in_website}", "{in_signatory_status}", "{in_country}");
	"""
	result = write_query(add_entity_query_string)
	return result


def add_user(in_email, in_first_name, in_last_name, in_affiliation):
	df = select_all_users()
	if in_email in df["work_email"].values:
		return "Existing User"

	add_user_query_string = f"""
	INSERT INTO vetted_user(work_email, first_name, last_name, affiliation_name)
	VALUES ("{in_email}", "{in_first_name}", "{in_last_name}", "{in_affiliation}");
	"""
	result = write_query(add_user_query_string)
	return result

#______________________Custom Functions execute multiple queries in a chain______________________#

def register_user(in_email, in_first_name, in_last_name, in_affiliation, 
	in_website, in_signatory_status, in_country):
	add_entity(in_affiliation, in_website, in_signatory_status, in_country)
	return add_user(in_email, in_first_name.title(), in_last_name.title(), in_affiliation)