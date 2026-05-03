import re
from typing import Dict

class HybridClassifier:

    DANGEROUS_PATTERNS = [
        r'delete.*file', r'shutdown', r'reboot', r'format',
        r'rm\s+-rf', r'call.*phone', r'send.*money'
    ]

    @staticmethod
    def classify(query: str) -> Dict[str, str]:
        q = query.lower()

        # 🚫 Safety
        for pattern in HybridClassifier.DANGEROUS_PATTERNS:
            if re.search(pattern, q):
                return {"type": "blocked", "reason": "dangerous_command"}

        # 🎵 PRIORITY MEDIA (IMPORTANT)
        if "play" in q:
            return {"type": "task", "intent": "media"}

        # 🌐 Web
        if any(word in q for word in ["open", "launch", "go to"]):
            return {"type": "task", "intent": "web"}

        # 📧 Email
        if "email" in q:
            return {"type": "task", "intent": "email"}

        # 🔍 Search fallback
        if any(word in q for word in ["search", "find", "what", "who"]):
            return {"type": "search", "intent": "search"}

        return {"type": "chat", "intent": "general"}