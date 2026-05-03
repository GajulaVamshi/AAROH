import json
from pathlib import Path
from core.config import config

class SafetyGuard:
    def __init__(self):
        self.permissions_file = config.USER_PROFILES / "permissions.json"
        self.permissions = self._load_permissions()
    
    def _load_permissions(self) -> dict:
        if self.permissions_file.exists():
            with open(self.permissions_file) as f:
                return json.load(f)
        return {"default": {"web": True, "system": False, "email": False}}
    
    def _save_permissions(self):
        with open(self.permissions_file, 'w') as f:
            json.dump(self.permissions, f, indent=2)
    
    def approve(self, intent, user_id: str) -> bool:
        user_perms = self.permissions.get(user_id, self.permissions["default"])
        
        if intent.action in ["open_web"]:
            return user_perms.get("web", True)
        elif intent.action in ["system_info", "volume_control"]:
            return user_perms.get("system", False)
        elif intent.action == "send_email":
            return user_perms.get("email", False)
        
        return True  # Chat always allowed