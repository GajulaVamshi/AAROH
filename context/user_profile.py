import json
from pathlib import Path

PROFILE_PATH = Path("./data/user_profiles")

class UserProfile:
    def __init__(self, user_id):
        self.file = PROFILE_PATH / f"{user_id}.json"
        self.data = self._load()

    def _load(self):
        if self.file.exists():
            return json.loads(self.file.read_text())
        return {}

    def save(self):
        self.file.write_text(json.dumps(self.data))

    def update(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key):
        return self.data.get(key)