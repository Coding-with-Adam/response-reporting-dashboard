USE vost_db;

ALTER TABLE vetted_user
ADD COLUMN hashed_password VARCHAR(100) NOT NULL AFTER work_email;