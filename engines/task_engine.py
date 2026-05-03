from actions.web_actions import WebActions
from actions.system_actions import SystemActions
from actions.messaging import EmailActions
from core.intent import AAROHIntent


class TaskEngine:

    def __init__(self):
        self.web = WebActions()
        self.system = SystemActions()
        self.email = EmailActions()

    async def execute(self, intent: AAROHIntent, user_id: str, context: dict) -> dict:

        try:
            # 🌐 OPEN
            if intent.action == "open_web":
                result = self.web.open(intent.target)
                return {"success": True, "message": result}

            # 🎵 PLAY (ONLY WHEN "play")
            elif intent.action == "play_media":
                result = self.web.play_media(intent.target)
                return {"success": True, "message": result}

            # ⚙️ SYSTEM
            elif intent.action == "system_info":
                result = self.system.info()
                return {"success": True, "data": result}

            # 📧 EMAIL
            elif intent.action == "send_email":
                result = await self.email.send_demo(intent.target, context)
                return {"success": True, "message": result}

            return {"success": False, "message": "Unknown action"}

        except Exception as e:
            return {"success": False, "error": str(e)}