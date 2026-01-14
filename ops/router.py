def detect_intent(text: str) -> dict:
    t = text.lower()

    # --- OPEN GOOGLE / CHROME ---
    if "google" in t or "chrome" in t or "browser" in t:
        return {
            "intent": "OPEN_GOOGLE",
            "context": {
                "text": text
            }
        }
    t = text.lower().strip()
    t = t.replace("crom", "chrome").replace("get hot", "google")

    if any(w in t for w in ("create repo", "new repo", "github repo")):
        return {"intent": "CREATE_REPO", "text": t}

    if any(w in t for w in ("open", "launch", "start")):
        return {"intent": "OPEN_APP", "text": t}

    if any(w in t for w in ("create file", "new file", "make file")):
        return {"intent": "CREATE_FILE", "text": t}

    if any(w in t for w in ("create folder", "new folder", "make folder")):
        return {"intent": "CREATE_FOLDER", "text": t}

    if "screenshot" in t:
        return {"intent": "SCREENSHOT"}

    if any(w in t for w in ("play", "open image", "open video")):
        return {"intent": "MEDIA", "text": t}

    if any(w in t for w in ("status", "cpu", "ram", "usage")):
        return {"intent": "SYSTEM_STATUS"}

    if any(w in t for w in ("time", "date")):
        return {"intent": "TIME"}

    if any(w in t for w in ("note", "remember")):
        return {"intent": "NOTE", "text": t}

    if any(w in t for w in ("recall", "what did i say")):
        return {"intent": "RECALL_NOTE"}
    
    if t in ("yes", "confirm", "do it"):
        return {"intent": "CONFIRM"}

    if t in ("no", "cancel", "abort"):
        return {"intent": "CANCEL"}

    return {
        "intent": "UNKNOWN",
        "context": {
            "text": text
        }
    }
