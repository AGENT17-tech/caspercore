import webbrowser
import os
import subprocess


# ======================================================
# COMMAND IMPLEMENTATIONS
# ======================================================

def open_google(context):
    webbrowser.open("https://www.google.com")
    return {
        "speech": "Opening Google."
    }


def open_chrome(context):
    subprocess.Popen(["google-chrome"])
    return {
        "speech": "Opening Google Chrome."
    }


def unknown(context):
    # IMPORTANT: unknown does NOT speak
    # It defers to the LLM
    return {
        "speech": None,
        "needs_llm": True,
        "prompt": context.get("text", "")
    }


# ======================================================
# COMMAND REGISTRY (THIS WAS MISSING)
# ======================================================

commands = {
    "OPEN_GOOGLE": open_google,
    "OPEN_CHROME": open_chrome,
    "UNKNOWN": unknown,
}
