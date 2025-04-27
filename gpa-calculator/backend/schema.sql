CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course TEXT NOT NULL,
    credits INTEGER NOT NULL,
    grade TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_course ON grades (course);
