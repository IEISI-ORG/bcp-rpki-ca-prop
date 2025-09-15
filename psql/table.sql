CREATE TABLE rpki_errors (
    id SERIAL PRIMARY KEY,
    timestamp VARCHAR(50),
    host VARCHAR(255),
    error_type VARCHAR(100),
    severity VARCHAR(10),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for common queries
CREATE INDEX idx_rpki_errors_timestamp ON rpki_errors(timestamp);
CREATE INDEX idx_rpki_errors_host ON rpki_errors(host);
CREATE INDEX idx_rpki_errors_error_type ON rpki_errors(error_type);
CREATE INDEX idx_rpki_errors_severity ON rpki_errors(severity);

