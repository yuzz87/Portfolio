USE sort_portfolio;

-- ==========================================
-- users
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,

  is_active BOOLEAN DEFAULT TRUE,

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  deleted_at DATETIME DEFAULT NULL,

  UNIQUE KEY uq_username (username)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


-- ==========================================
-- algorithms (master table)
-- ==========================================

CREATE TABLE IF NOT EXISTS algorithms (
  id INT AUTO_INCREMENT PRIMARY KEY,

  name VARCHAR(30) NOT NULL,
  complexity VARCHAR(50) COMMENT 'Time complexity',

  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  UNIQUE KEY uq_algorithm_name (name)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


-- ==========================================
-- battles
-- ==========================================

CREATE TABLE IF NOT EXISTS battles (
  id INT AUTO_INCREMENT PRIMARY KEY,

  user_id INT NULL,

  array_size INT NOT NULL,
  benchmark_size INT NOT NULL,

  status VARCHAR(20) DEFAULT 'COMPLETED',

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

  -- index
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at),

  -- foreign key
  CONSTRAINT fk_battles_user
    FOREIGN KEY (user_id)
    REFERENCES users(id),

  -- validation
  CONSTRAINT chk_array_size
    CHECK (array_size BETWEEN 5 AND 100),

  CONSTRAINT chk_benchmark_size
    CHECK (benchmark_size BETWEEN 100 AND 10000)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


-- ==========================================
-- battle_results
-- ==========================================

CREATE TABLE IF NOT EXISTS battle_results (
  id INT AUTO_INCREMENT PRIMARY KEY,

  battle_id INT NOT NULL,
  algorithm_id INT NOT NULL,

  duration_ms DOUBLE NOT NULL,

  rank_position INT NOT NULL,

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  -- unique constraints
  UNIQUE KEY uq_battle_rank (battle_id, rank_position),
  UNIQUE KEY uq_battle_algorithm (battle_id, algorithm_id),

  -- indexes
  INDEX idx_battle_id (battle_id),
  INDEX idx_algorithm (algorithm_id),
  INDEX idx_rank (rank_position),
  INDEX idx_duration (duration_ms),

  -- foreign keys
  CONSTRAINT fk_battle
    FOREIGN KEY (battle_id)
    REFERENCES battles(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_algorithm
    FOREIGN KEY (algorithm_id)
    REFERENCES algorithms(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

  -- validation
  CONSTRAINT chk_duration_positive
    CHECK (duration_ms >= 0)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;