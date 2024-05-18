USE vost_db;

ALTER TABLE vetted_user
RENAME COLUMN approval_date TO decision_date;

ALTER TABLE vetted_user
ADD COLUMN application_decision VARCHAR(20) DEFAULT 'Pending' AFTER application_date;

ALTER TABLE vetted_user
ADD COLUMN decision_author VARCHAR(50) AFTER decision_date;