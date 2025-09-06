import sqlite3

data = ["Eniola", "27", "female"]
DB_COLUMN = ["name", "age", "gender"]

def write_db():

    with sqlite3.connect("people-db.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL 
            )
        """)

        cursor.execute("""
            SELECT * FROM people_data
                WHERE name = ?
        """ , ([data[0]]))

        existing = cursor.fetchall()

        if existing:
            print(f"This data already exist: {existing}")
            return
        
        placeholder = ", ".join(["?"] * len(DB_COLUMN))

        insert_sql = f"""
            INSERT INTO people_data ({", ".join(DB_COLUMN)})
            VALUES ({placeholder})
        """
        cursor.execute(insert_sql, data)
        conn.commit()

        cursor.execute("""
            SELECT * FROM people_data
        """)
        print(cursor.fetchall())

write_db()