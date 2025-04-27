def create_tables(db):
    db.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            credits INTEGER NOT NULL,
            grade TEXT NOT NULL
        );
    ''')
    db.execute('CREATE INDEX IF NOT EXISTS idx_course ON grades (course);')
    db.commit()
