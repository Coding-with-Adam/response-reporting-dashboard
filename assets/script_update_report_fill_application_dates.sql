USE vost_db;

UPDATE vetted_user SET application_date = NOW()
WHERE work_email != '';