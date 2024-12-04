import sqlite3


class ModListDatabase:
    def __init__(self):
        # Connect to SQLite database (or create it)
        self.conn = sqlite3.connect('Data/modifications.db')
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        # Mods
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Modifications (
            modification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            modification_name TEXT UNIQUE
        )
        ''')
        # API`s
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS APIs (
            api_id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT UNIQUE
        )
        ''')
        # Versions
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Versions (
            version_id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_name TEXT UNIQUE
        )
        ''')
        # Links
        self.cursor.execute('''
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

    def get_modification_id(self, mod_name: str) -> list[int] | None:
        """
        Search db row with Mod ID in DB from her name
        :param mod_name: Mod
        :return: list[ID] or None
        """
        self.cursor.execute("SELECT modification_id FROM Modifications WHERE modification_name = ?", (mod_name,))
        return self.cursor.fetchone()

    # Function to get or create an entry in the Modifications table
    def get_modification_id_s(self, mod_name: str) -> int:
        """
        Search Mod ID in DB from her name
        :param mod_name: Mod
        :return: ID
        """
        row = self.get_modification_id(mod_name)
        if row:
            return row[0]
        else:
            self.cursor.execute("INSERT INTO Modifications (modification_name) VALUES (?)", (mod_name,))
            return self.cursor.lastrowid

    def get_api_id(self, api_name: str) -> int:
        """
        Search Minecraft Mod API ID in DB from her name
        :param api_name: Mod API name
        :return:
        """
        self.cursor.execute("SELECT api_id FROM APIs WHERE api_name = ?", (api_name,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            self.cursor.execute("INSERT INTO APIs (api_name) VALUES (?)", (api_name,))
            return self.cursor.lastrowid

    def get_version_id(self, version_name: str) -> int:
        """
        Search Minecraft Version ID in DB from her name
        :param version_name: Version name
        :return: Version ID
        """
        self.cursor.execute("SELECT version_id FROM Versions WHERE version_name = ?", (version_name,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            self.cursor.execute("INSERT INTO Versions (version_name) VALUES (?)", (version_name,))
            return self.cursor.lastrowid

    def add_new(self, mod_name: str, api_name: str, version_name: str, enabled: bool) -> None:
        """
        Add new mod link to DB
        :param mod_name: Mod name
        :param api_name: API name
        :param version_name: Version
        :param enabled: TRUE/FALSE flag to change ID links
        :return: Nothing
        """

        # Found ID`s
        mod_id = self.get_modification_id_s(mod_name)
        api_id = self.get_api_id(api_name)
        version_id = self.get_version_id(version_name)

        # Insert Mod in Links List
        self.cursor.execute('''
        INSERT INTO Modification_API_Version (modification_id, api_id, version_id, enabled)
        VALUES (?, ?, ?, ?)
        ''', (mod_id, api_id, version_id, int(enabled)))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        return True
