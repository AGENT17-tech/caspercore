from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = (
    "You are Casper, a calm, precise AI assistant. "
    "You explain clearly and concisely. "
    "You do not execute system commands."
)

def query(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
