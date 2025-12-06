CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id INTEGER,
    folder_id INTEGER,
    owner_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    genus VARCHAR(50),
    species VARCHAR(50),
    variety VARCHAR(50),
    description TEXT,
    birth_date DATE,
    life_status VARCHAR(20) NOT NULL DEFAULT 'живое'
        CHECK (life_status IN ('живое', 'погибло')),
    death_date DATE,
    death_cause VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);