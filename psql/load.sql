--- feed to your psql cli:
COPY rpki_errors (timestamp, host, error_type, severity, message)
FROM '/path/to/errors.csv'
DELIMITER ','
CSV HEADER;

