import threading

class LLM:
    def __init__(self, client):
        self.client = client

    def ask_async(self, prompt, callback):
        def run():
            try:
                text = self.client(prompt)
                callback(text)
            except Exception as e:
                callback(f"I encountered an error: {e}")
        threading.Thread(target=run, daemon=True).start()
