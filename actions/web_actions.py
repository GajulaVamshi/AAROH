import webbrowser
import platform
import pywhatkit


class WebActions:

    URL_MAP = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "gmail": "https://gmail.com",
        "calculator": "calc" if platform.system() == "Windows" else "Calculator"
    }

    # 🌐 OPEN WEBSITE / APP
    def open(self, target: str) -> str:
        target = target.lower().strip()

        try:
            url = self.URL_MAP.get(
                target,
                f"https://www.google.com/search?q={target.replace(' ', '+')}"
            )

            webbrowser.open(url)
            print(f"🌐 DEBUG: Opening → {url}")

            return f"🌐 Opened {target.title()}"

        except Exception as e:
            print(f"❌ ERROR opening {target}: {e}")
            return f"❌ Failed to open {target}"

    # 🎵 PLAY MEDIA (STRICT FOR "play")
    def play_media(self, query: str) -> str:
        query = query.strip()

        print(f"🎵 DEBUG: Play request → {query}")

        if not query:
            query = "music"

        try:
            # 🔥 TRY AUTO PLAY
            pywhatkit.playonyt(query)
            print("✅ pywhatkit executed")

            return f"🎵 Playing '{query.title()}' on YouTube"

        except Exception as e:
            print(f"❌ pywhatkit failed: {e}")

            # 🔥 FALLBACK (ALWAYS WORKS)
            try:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(url)

                print(f"🔁 Fallback opened → {url}")

                return f"🎵 Showing results for '{query}' on YouTube"

            except Exception as e2:
                print(f"❌ Fallback failed: {e2}")
                return "❌ Could not open YouTube"