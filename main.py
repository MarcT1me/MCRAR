from database_control import *

# List of modifications to check
required_modifications = ['Create', 'Big Cannons']

# Query to find API-version pairs where all required modifications are enabled
mod_ids = []
for mod_name in required_modifications:
    cursor.execute("SELECT modification_id FROM Modifications WHERE modification_name = ?", (mod_name,))
    row = cursor.fetchone()
    if row:
        mod_ids.append(row[0])

if mod_ids:
    query = f'''
    SELECT api_name, version_name
    FROM Modification_API_Version m
    JOIN APIs a ON m.api_id = a.api_id
    JOIN Versions v ON m.version_id = v.version_id
    WHERE m.enabled = 1 AND m.modification_id IN ({','.join(map(str, mod_ids))})
    GROUP BY api_name, version_name
    HAVING COUNT(DISTINCT m.modification_id) = {len(mod_ids)}
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    for api, version in results:
        print(f"API: {api}, Version: {version} has all modifications.")
else:
    print("No required modifications found in the database.")

# Close the connection
conn.close()
