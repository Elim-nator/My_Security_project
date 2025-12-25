CREATE DATABASE IF NOT EXISTS intel_db;
USE intel_db;

CREATE TABLE IF NOT EXISTS intel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target VARCHAR(255) NOT NULL,
    ip VARCHAR(45),
    ports TEXT,
    os_info VARCHAR(255),
    collected_at DATETIME
);
