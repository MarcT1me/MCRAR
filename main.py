from database_control import ModListDatabase
from mod_parser import parse
import json
from loguru import logger


def get_mod_to_scan(db: ModListDatabase, mod_name: str) -> tuple[bool, int]:
    row = db.get_modification_id(mod_name)
    return bool(row), row[0] if row else -1


def main():
    with ModListDatabase() as db:
        with open("Data/mods.json") as mods_f:
            data = json.loads(mods_f.read())

        # Assuming data["Upstream"] contains URLs to Modrinth API endpoints
        parse(db, data["Upstream"]["Source"], data["Upstream"]["List"], data["Upstream"]["Refresh"])
        required_modifications: list[str] = data["Scan"]

        mod_ids: list[int] = []
        for mod_name in required_modifications:
            counted_variants = mod_name.count('/')
            versions: list[str] = mod_name.split('/')
            if counted_variants:
                for i in range(counted_variants):
                    success, mod_id = get_mod_to_scan(db, versions[i])
                    if success:
                        mod_ids.append(mod_id)
                        break
                else:
                    logger.warning(f"Dont exist mod with name {mod_name}")

        if mod_ids:
            query = '''
            SELECT a.api_name, v.version_name
            FROM Modification_API_Version m
            JOIN APIs a ON m.api_id = a.api_id
            JOIN Versions v ON m.version_id = v.version_id
            WHERE m.enabled = 1 AND m.modification_id IN ({})
            GROUP BY a.api_name, v.version_name
            HAVING COUNT(DISTINCT m.modification_id) = {}
            '''.format(','.join(map(str, mod_ids)), len(mod_ids))

            db.cursor.execute(query)
            results = db.cursor.fetchall()
            for api, version in results:
                print(f"Mod Puck scanned on API: {api}, Version: {version}")
        else:
            print("No required modifications found in the database.")


if __name__ == "__main__":
    main()
    input("\nProgram finished. Press Enter to exit")
