USE vost_db;

ALTER TABLE report
ADD CONSTRAINT report_date_conflicts CHECK (close_report_timestamp >= open_report_timestamp);