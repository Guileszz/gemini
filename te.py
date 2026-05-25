import requests

# Endereço do seu 9router
URL = "http://localhost:20128/v1/chat/completions"

# A chave sk- que você criou no painel do 9router
HEADERS = {
    "Authorization": "Bearer SUA_CHAVE_DO_9ROUTER",
    "Content-Type": "application/json"
}

def disparar_comando(prompt, modelo):
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Erro: {response.text}"

# EXEMPLOS DE DISPARO:
# print(disparar_comando("Crie um script de scraping em Python.", "claude-3-5-sonnet-20241022"))
# print(disparar_comando("Analise este banco de dados.", "gemini-2.5-pro"))