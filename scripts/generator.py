import json
import os
from typing import Dict, Any
from datetime import datetime

class JsonGenerator:
    def __init__(self):
        self.api_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api', 'v1')
        self._ensure_directories()

    def _ensure_directories(self):
        """Creates necessary directories if they don't exist"""
        os.makedirs(self.api_dir, exist_ok=True)

    def generate_political_data(self, data: Dict[str, Any]):
        """
        Generates separate JSON files for different types of political data
        """
        # Generate federal and congress data
        dynamic_data = {
            "federal": data["federal"],
            "congress": data["congress"],
            "last_updated": datetime.utcnow().isoformat()
        }
        self._write_json("dynamic_data.json", dynamic_data)

        # Generate state data
        states_data = {
            "states": data["states"],
            "last_updated": datetime.utcnow().isoformat()
        }
        self._write_json("states_data.json", states_data)

        # Generate ZIP code data in chunks to keep file sizes manageable
        self._generate_zip_chunks(data["zip_data"])

    def generate_version_data(self, version_data: Dict[str, Any]):
        """
        Generates version information file
        """
        self._write_json("version.json", version_data)

    def _generate_zip_chunks(self, zip_data: Dict[str, Any]):
        """
        Splits ZIP code data into manageable chunks by state
        """
        # Group ZIP codes by state
        state_groups = {}
        for zip_code, data in zip_data.items():
            state = data["state"]
            if state not in state_groups:
                state_groups[state] = {}
            state_groups[state][zip_code] = data

        # Generate separate files for each state
        for state, state_zip_data in state_groups.items():
            filename = f"zip_data_{state.lower()}.json"
            data = {
                "state": state,
                "zip_codes": state_zip_data,
                "last_updated": datetime.utcnow().isoformat()
            }
            self._write_json(filename, data)

        # Generate index file
        index = {
            "states": list(state_groups.keys()),
            "file_pattern": "zip_data_{state}.json",
            "last_updated": datetime.utcnow().isoformat()
        }
        self._write_json("zip_data_index.json", index)

    def _write_json(self, filename: str, data: Dict[str, Any]):
        """
        Writes data to a JSON file with proper formatting
        """
        filepath = os.path.join(self.api_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Generated {filename}")

    def _read_json(self, filename: str) -> Dict[str, Any]:
        """
        Reads data from a JSON file
        """
        filepath = os.path.join(self.api_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
