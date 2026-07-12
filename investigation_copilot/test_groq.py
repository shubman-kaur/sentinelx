from groq import Groq


api_key = "PASTE YOUR API KEY HERE "

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Say hello in one sentence"}
    ]
)

print(response.choices[0].message.content)