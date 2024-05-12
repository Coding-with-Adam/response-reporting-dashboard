USE vost_db;

ALTER TABLE vetted_user
ADD COLUMN application_date TIMESTAMP(6) NOT NULL AFTER affiliation_name,
ADD COLUMN approval_date TIMESTAMP(6) AFTER application_date;