CREATE TABLE IF NOT EXISTS plant_health_checks (
    health_check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER NOT NULL,
    check_date DATE DEFAULT CURRENT_DATE,
    growth_phase VARCHAR(20)
        CHECK (growth_phase IN ('покой', 'вегетация', 'цветение')),
    pests_detected VARCHAR(200),
    diseases_detected VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE
);