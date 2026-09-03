import json
from pathlib import Path


class ArchetypeEngine:

    def __init__(self, config_path):
        self.config_path = Path(config_path)

        with open(self.config_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.archetypes = data["archetypes"]

    def get_archetype(self, archetype_id):
        for archetype in self.archetypes:
            if archetype["archetype_id"] == archetype_id:
                return archetype

        raise ValueError(
            f"Archetype '{archetype_id}' not found."
        )

    def list_archetypes(self):
        return [
            archetype["archetype_id"]
            for archetype in self.archetypes
        ]