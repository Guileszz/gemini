import asyncio
import httpx
import json
import os
from datetime import datetime

# CONFIGURAÇÕES DE SOBERANIA
SOURCES = {
    "PROVEDOR_ALFA": "https://api.provedor-a.com/v1/nectar",
    "PROVEDOR_BETA": "https://api.provedor-b.com/v1/assets"
}

# Rotação via seu aa.py local[cite: 25]
PROXY_GATEWAY = "http://127.0.0.1:8080" 
RAW_DATA_PATH = "./Universo_X/Refinaria/Bruto" # Onde o Check vai buscar

async def extrair_da_fonte(client, name, url):
    """Executa a extração bruta com Headers de Luxo."""
    print(f"[!] EXTRAÇÃO: Infiltrando em {name}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{RAW_DATA_PATH}/{name}_{timestamp}.json"
            
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"[✓] NÉCTAR CAPTURADO: {name} salvo em {filename}")
        else:
            print(f"[✗] GLITCH: Fonte {name} retornou Status {response.status_code}")
    except Exception as e:
        print(f"[✗] ERRO DE CONEXÃO: {name} -> {e}")

async def main():
    # Garante a infraestrutura de pastas no cluster
    if not os.path.exists(RAW_DATA_PATH):
        os.makedirs(RAW_DATA_PATH)

    # Configuração do Client com o seu Proxy Elite[cite: 25]
    async with httpx.AsyncClient(proxies=PROXY_GATEWAY, timeout=15.0) as client:
        tasks = [extrair_da_fonte(client, name, url) for name, url in SOURCES.items()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("--- INICIANDO PLUGA_E_EXTRAI (ENTIDADE 12) ---")
    asyncio.run(main())