import psutil
import platform
import pyautogui
import webbrowser

class SystemActions:
    def info(self) -> dict:
        return {
            "cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%",
            "memory_usage": f"{psutil.virtual_memory().percent:.1f}%",
            "platform": platform.system(),
            "processes": len(psutil.pids())
        }
    
    def volume_control(self, direction: str) -> str:
        try:
            if "up" in direction.lower():
                pyautogui.press("volumeup")
            elif "down" in direction.lower():
                pyautogui.press("volumedown")
            else:
                pyautogui.press("volumemute")
            return f"Volume {direction.lower()}"
        except:
            return "Volume control simulated"