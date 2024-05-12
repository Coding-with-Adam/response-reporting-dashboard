USE vost_db;

ALTER TABLE vetted_user
ADD COLUMN is_admin BIT NOT NULL DEFAULT 0 AFTER last_name;