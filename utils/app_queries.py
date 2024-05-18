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
	user_info = {"full_name":"", "hashed_password":"", "is_admin":False}

	user_query_string = f"""
	SELECT
		CONCAT(first_name, ' ', last_name) AS full_name,
		is_admin,
		hashed_password
	FROM vetted_user
	WHERE work_email = '{email_in}';
	"""
	df = read_query(user_query_string)
	try:
		#The try except elegantly replaces "not df.empty" and, in addition, handles nondataframe results
		user_info["full_name"] = df.iloc[0]["full_name"]
		user_info["hashed_password"] = df.iloc[0]["hashed_password"]
		user_info["is_admin"] = df.iloc[0]["is_admin"]
	except Exception as e:
		return user_info #Unmodified template dict
	return user_info

def select_all_reports(url_in = None):
	reports_query_string = f"""
	SELECT
		rp.open_report_timestamp,
		CONCAT(vu.first_name, " ", vu.last_name) AS reporing_user,
		vu.affiliation_name AS reporting_entity,
		rp.platform_name AS platform,
		rp.url,
		rp.report_type,
		rp.screenshot_url,
		rp.close_report_timestamp,
		rp.platform_decision,
		rp.policy,
		rp.appeal
	FROM
		report AS rp
		INNER JOIN
		vetted_user AS vu
		ON vu.work_email = rp.reporting_user
	"""
	if url_in is not None:
		reports_query_string += f"""
		WHERE url = '{url_in}'
		"""
	reports_query_string += f"""
	ORDER BY rp.open_report_timestamp DESC;
	"""
	df = read_query(reports_query_string)
	return df

def select_user_reports(email_in, url_in = None):
	reports_query_string = f"""
	SELECT
		open_report_timestamp,
		platform_name AS platform,
		url,
		report_type,
		screenshot_url,
		close_report_timestamp,
		platform_decision,
		policy,
		appeal
	FROM report
	WHERE reporting_user = '{email_in}'
	"""
	if url_in is not None:
		reports_query_string += f"""
		WHERE url = '{url_in}'
		"""
	#Add a nonmandatory sorting:
	reports_query_string += f"""
	ORDER BY open_report_timestamp DESC;
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

def add_entity(affiliation_in, website_in, signatory_status_in, country_in):
	df = select_all_entities()
	if affiliation_in in df["entity_name"].values:
		return "Existing entity"

	add_entity_query_string = f"""
	INSERT INTO entity (
		entity_name,
		website,
		signatory_of_code_of_practice_on_disinformation,
		country_name
	)
	VALUES ('{affiliation_in}', '{website_in}', '{signatory_status_in}', '{country_in}');
	"""
	result = write_query(add_entity_query_string)
	return result


def add_user(email_in, hashed_password_in, first_name_in, last_name_in, affiliation_in, date_in):
	df = select_all_users()
	if email_in in df["work_email"].values:
		return "Existing User"

	add_user_query_string = f"""
	INSERT INTO vetted_user(
		work_email,
		hashed_password,
		first_name,
		last_name,
		affiliation_name,
		application_date
	)
	VALUES ('{email_in}', '{hashed_password_in}', '{first_name_in}', '{last_name_in}', '{affiliation_in}', '{date_in}');
	"""

	result = write_query(add_user_query_string)
	return result

def add_report(current_date_in, email_in, platform_in, url_in, type_in, screenshot_url_in,
	answer_date_in, decision_in, policy_in, appeal_in):
	df = select_all_reports(url_in)
	if not df.empty:
		return "A report with the specified url already exists. Submission denied."
	
	add_report_query_string = f"""
	INSERT INTO report(
		open_report_timestamp,
		reporting_user,
		platform_name,
		url,
		report_type,
		screenshot_url,
		close_report_timestamp,
		platform_decision,
		policy,
		appeal
	)
	SELECT
		'{current_date_in}',
		'{email_in}',
		'{platform_in}',
		'{url_in}',
		'{type_in}',
		CASE WHEN '{screenshot_url_in}' = 'None' THEN NULL ELSE '{screenshot_url_in}' END,
		CASE WHEN '{answer_date_in}' = 'None' THEN NULL ELSE '{answer_date_in}' END,
		CASE WHEN '{decision_in}' = 'None' THEN NULL ELSE '{decision_in}' END,
		CASE WHEN '{policy_in}' = 'None' THEN NULL ELSE '{policy_in}' END,
		CASE WHEN '{appeal_in}' = 'None' THEN NULL ELSE '{appeal_in}' END;
	"""
	result = write_query(add_report_query_string)
	return result

#________________________________________UPDATE Queries________________________________________#

def update_report(platform_in, url_in, type_in, screenshot_in,
	answer_date_in, decision_in, policy_in, appeal_in):
	update_report_query_string = f"""
	UPDATE report
	SET
		platform_name = '{platform_in}',
		url = CASE WHEN '{url_in}' = '' THEN url ELSE '{url_in}' END,
		report_type = NULLIF('{type_in}', ''),
		screenshot_url = NULLIF('{screenshot_in}', ''),
		close_report_timestamp = NULLIF('{answer_date_in}', ''),
		platform_decision = NULLIF('{decision_in}', ''),
		policy = NULLIF('{policy_in}', ''),
		appeal = NULLIF('{appeal_in}', '')
	WHERE url = '{url_in}';
	"""
	result = write_query(update_report_query_string)
	return result

#________________________________________DELETE Queries________________________________________#
def delete_report(url_in):
	delete_report_query = f"""
	DELETE FROM report
	WHERE url = '{url_in}'
	"""
	result = write_query(delete_report_query)
	return result

#______________________Custom Functions execute multiple queries in a chain______________________#

def register_user(email_in, hashed_password_in, first_name_in, last_name_in, affiliation_in, 
	date_in, website_in, signatory_status_in, country_in):
	add_entity(affiliation_in, website_in, signatory_status_in, country_in)
	return add_user(email_in, hashed_password_in, first_name_in.title(), last_name_in.title(), affiliation_in, date_in)