CREATE TABLE IF NOT EXISTS plant_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER NOT NULL,
    event_type VARCHAR(20) NOT NULL
        CHECK (event_type IN ('полив', 'пересадка', 'удобрение', 'обработка', 'обрезка', 'болезнь')),
    event_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_description TEXT,
    FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE
);