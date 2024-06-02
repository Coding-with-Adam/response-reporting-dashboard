USE vost_db;

UPDATE vetted_user
SET is_admin = 1, application_decision = 'Approved', decision_date = NOW()
WHERE work_email = 'nyv.mondele@vost.com';