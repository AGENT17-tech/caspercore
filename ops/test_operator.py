from ops.router import detect_intent
from ops.executor import execute

print("CASPER OPERATOR HARDENED TEST — type 'exit' to quit\n")

while True:
    text = input("You: ")
    if text.lower() in ("exit", "quit"):
        break

    intent = detect_intent(text)
    response = execute(intent)

    print(f"Casper: {response['speech']}\n")
