import re
from typing import Dict, Any
from dataclasses import dataclass
from core.classifier import HybridClassifier


@dataclass
class AAROHIntent:
    type: str
    action: str
    target: str
    params: Dict[str, Any] = None
    confidence: float = 1.0


class IntentExtractor:

    @staticmethod
    def extract(query: str) -> AAROHIntent:
        classifier = HybridClassifier().classify(query)

        if classifier["type"] == "blocked":
            return AAROHIntent("blocked", "", "")

        if classifier["type"] == "task":
            return IntentExtractor._extract_task_intent(query, classifier["intent"])

        return AAROHIntent("chat", "converse", query)

    @staticmethod
    def _extract_task_intent(query: str, intent_type: str) -> AAROHIntent:
        q = query.lower()

        # 🌐 OPEN
        if intent_type == "web":
            target = re.search(r'(google|youtube|gmail|calculator)', q)
            return AAROHIntent(
                "task",
                "open_web",
                target.group(1) if target else "google"
            )

        # 🎵 PLAY (STRICT)
        elif intent_type == "media":
            # remove "play"
            song = q.replace("play", "").strip()

            return AAROHIntent(
                "task",
                "play_media",
                song if song else "music"
            )

        # 📧 EMAIL
        elif intent_type == "email":
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', query)
            return AAROHIntent(
                "task",
                "send_email",
                email_match.group() if email_match else ""
            )

        return AAROHIntent("task", intent_type, q)