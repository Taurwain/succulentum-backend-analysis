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
    price DECIMAL(10,2),
    source VARCHAR(100),
    location VARCHAR(100),
    life_status VARCHAR(20) NOT NULL DEFAULT 'живое'
        CHECK (life_status IN ('живое', 'погибло')),
    status VARCHAR(20) NOT NULL DEFAULT 'активное'
        CHECK (status IN ('активное', 'на обмен', 'подарено', 'продано')),
    death_date DATE,
    death_cause VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    care_difficulty VARCHAR(20)
        CHECK (care_difficulty IN ('легкий', 'средний', 'сложный')),
    light_requirements VARCHAR(30)
        CHECK (light_requirements IN ('тень', 'полутень', 'рассеянный свет', 'прямое солнце')),
    watering_frequency VARCHAR(20)
        CHECK (watering_frequency IN ('редко', 'умеренно', 'часто'))
);
