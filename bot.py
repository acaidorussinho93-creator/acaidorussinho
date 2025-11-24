# chatbot_openai.py
from openai import OpenAI

client = OpenAI(api_key="sua-api-key-aqui")  # pegue em https://platform.openai.com

print("🤖 ChatGPT no Python! (digite 'sair' para encerrar)\n")

historico = [{"role": "system", "content": "Você é um assistente brasileiro simpático e engraçado."}]

while True:
    user = input("Você: ")
    if user.lower() == "sair":
        break
        
    historico.append({"role": "user", "content": user})
    
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",  # ou gpt-3.5-turbo
        messages=historico
    )
    
    bot = resposta.choices[0].message.content
    print("Bot:", bot, "\n")
    
    historico.append({"role": "assistant", "content": bot})