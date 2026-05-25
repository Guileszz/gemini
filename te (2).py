import requests

# Sua URL do 9router
url = "http://localhost:20128/v1/chat/completions"

# A chave que você criou no painel do 9router (aquela sk-...)
headers = {
    "Authorization": "Bearer sk-2c32642518d646de-53cddr-edf9febfI",
    "Content-Type": "application/json"
}

# Payload ajustado para o Gemini 1.5 Flash
data = {
    "model": "gemini-1.5-flash",
    "messages": [{"role": "user", "content": "Status da rede do Império?"}]
}

try:
    print("--- Iniciando Conexão ---")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("RESPOSTA DO SISTEMA:")
        print(response.json()['choices'][0]['message']['content'])
    else:
        print(f"ERRO TÁTICO: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"FALHA DE HARDWARE/REDE: {e}")