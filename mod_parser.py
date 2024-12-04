from database_control import ModListDatabase
import requests
import json
from loguru import logger


def parse(database: ModListDatabase, url: str, upstream_list: list[str], refresh: bool) -> None:
    for name in upstream_list:
        if database.get_modification_id(name) and not refresh:
            continue
        try:
            full_url = f"{url}{name.lower().replace(' ', '-')}"
            response = requests.get(full_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            logger.info(f"Successfully parsed data from {full_url}...")

            # Extract loaders and game_versions
            loaders = data.get('loaders', [])
            game_versions = data.get('game_versions', [])

            # Assuming data contains mod_name, api_name, version_name, and enabled
            for loader in loaders:
                for version in game_versions:
                    database.add_new(name, loader, version, True)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error {e}")
        except Exception as e:
            logger.error(f"Unexpected Error {e}")
