USE vost_db;

ALTER TABLE report
RENAME COLUMN timestamp TO open_report_timestamp,
RENAME COLUMN answer_date TO close_report_timestamp;