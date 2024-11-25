import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('modifications.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Modifications (
    modification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    modification_name TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS APIs (
    api_id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_name TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Versions (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_name TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Modification_API_Version (
    modification_id INTEGER,
    api_id INTEGER,
    version_id INTEGER,
    enabled BOOLEAN,
    FOREIGN KEY (modification_id) REFERENCES Modifications(modification_id),
    FOREIGN KEY (api_id) REFERENCES APIs(api_id),
    FOREIGN KEY (version_id) REFERENCES Versions(version_id)
)
''')

# Function to get or create an entry in the Modifications table
def get_modification_id(mod_name):
    cursor.execute("SELECT modification_id FROM Modifications WHERE modification_name = ?", (mod_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO Modifications (modification_name) VALUES (?)", (mod_name,))
        return cursor.lastrowid

# Function to get or create an entry in the APIs table
def get_api_id(api_name):
    cursor.execute("SELECT api_id FROM APIs WHERE api_name = ?", (api_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO APIs (api_name) VALUES (?)", (api_name,))
        return cursor.lastrowid

# Function to get or create an entry in the Versions table
def get_version_id(version_name):
    cursor.execute("SELECT version_id FROM Versions WHERE version_name = ?", (version_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO Versions (version_name) VALUES (?)", (version_name,))
        return cursor.lastrowid

# Function to add a new record to Modification_API_Version
def AddNew(mod_name, api_name, version_name, enabled):
    mod_id = get_modification_id(mod_name)
    api_id = get_api_id(api_name)
    version_id = get_version_id(version_name)
    cursor.execute('''
    INSERT INTO Modification_API_Version (modification_id, api_id, version_id, enabled)
    VALUES (?, ?, ?, ?)
    ''', (mod_id, api_id, version_id, int(enabled)))
    conn.commit()  # Commit the transaction after insertion
