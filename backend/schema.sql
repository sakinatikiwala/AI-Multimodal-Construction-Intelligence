CREATE DATABASE IF NOT EXISTS constructai
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE constructai;

CREATE TABLE IF NOT EXISTS analysis_history (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  feature VARCHAR(150) NOT NULL,
  request_data JSON NOT NULL,
  response_data JSON NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_analysis_history_created_at (created_at)
);
