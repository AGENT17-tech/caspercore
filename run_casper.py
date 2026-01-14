import sys
import threading

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ops.worker import OperatorWorker
from voice.stt import listen
from voice.tts import speak

from brain.llm import LLM
from brain.client_stub import query as llm_query


# ======================================================
# BACKGROUND VOICE LOOP
# ======================================================
def voice_loop(worker, core):
    while True:
        # UI: listening
        core.stateChanged.emit("LISTENING")

        try:
            text = listen()
        except Exception as e:
            print("[VOICE ERROR]", e)
            core.stateChanged.emit("IDLE")
            continue

        if not text.strip():
            core.stateChanged.emit("IDLE")
            continue

        # Forward transcript to operator
        worker.handle_text(text)


# ======================================================
# MAIN APPLICATION
# ======================================================
def main():
    app = QApplication(sys.argv)

    # ---------- UI ----------
    window = MainWindow()
    window.show()
    core = window.core

    # ---------- Operator ----------
    worker = OperatorWorker()

    # ---------- LLM (Stub) ----------
    llm = LLM(llm_query)

    # Operator → UI state passthrough
    worker.state.connect(core.stateChanged.emit)

    # Operator → Result handler
    def on_operator_result(payload: dict):
        # Known command handled directly
        if payload.get("speech"):
            core.stateChanged.emit("SPEAKING")
            speak(payload["speech"])
            core.stateChanged.emit("IDLE")
            return

        # Unknown → defer to LLM
        if payload.get("needs_llm"):
            core.stateChanged.emit("PROCESSING")

            def llm_done(text: str):
                core.stateChanged.emit("SPEAKING")
                speak(text)
                core.stateChanged.emit("IDLE")

            llm.ask_async(payload.get("prompt", ""), llm_done)

    worker.result.connect(on_operator_result)

    # ---------- Start voice thread ----------
    threading.Thread(
        target=voice_loop,
        args=(worker, core),
        daemon=True
    ).start()

    sys.exit(app.exec())


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    main()
