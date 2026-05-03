class AAROHRouter:

    def __init__(self):
        from core.intent import IntentExtractor
        from engines.chat_engine import ChatEngine
        from engines.task_engine import TaskEngine
        from core.safety import SafetyGuard

        self.intent_extractor = IntentExtractor()
        self.chat_engine = ChatEngine()
        self.task_engine = TaskEngine()
        self.safety = SafetyGuard()

    async def route(self, query: str, user_id: str, context: dict) -> dict:

        intent = self.intent_extractor.extract(query)

        # 🚫 Safety
        if intent.type == "blocked":
            return {
                "type": "response",
                "response": "⚠️ Blocked for safety",
                "intent": intent
            }

        # 🎯 TASK
        if intent.type == "task":
            result = await self.task_engine.execute(intent, user_id, context)

            return {
                "type": "task",
                "response": result.get("message", "Task executed"),
                "intent": intent
            }

        # 💬 CHAT
        response = await self.chat_engine.process(query, user_id, context)

        return {
            "type": "chat",
            "response": response,
            "intent": intent
        }