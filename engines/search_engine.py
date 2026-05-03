import webbrowser

class SearchEngine:
    def search(self, query):
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"🔍 Searching for {query}"