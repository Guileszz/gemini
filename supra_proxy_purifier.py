
import asyncio
import aiohttp
import time
from flask import Flask, jsonify

app = Flask(__name__)

# CONFIGURAÇÃO TÁTICA
TARGET_TEST = "http://google.com"  # Alvo para validar o Hit
CHECK_TIMEOUT = 5                  # Segundos para descartar proxy lento
UPDATE_INTERVAL = 600              # Recarregar novas fontes a cada 10 min (600s)

# FONTES DE NÉCTAR (SOCKS4/5 e HTTP)
SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"
]

valid_proxies = set()

async def check_proxy(session, proxy, protocol):
    """Detecta se o proxy está funcional e remove se for inválido."""
    proxy_url = f"{protocol}://{proxy}"
    try:
        async with session.get(TARGET_TEST, proxy=proxy_url, timeout=CHECK_TIMEOUT) as response:
            if response.status == 200:
                return proxy
    except:
        return None

async def refresh_and_clean():
    """Motor de Absorção e Purificação."""
    global valid_proxies
    while True:
        print("[ENTIDADE 12] Iniciando ciclo de purificação...")
        all_raw = []
        
        # Coleta
        async with aiohttp.ClientSession() as session:
            for url in SOURCES:
                try:
                    async with session.get(url) as r:
                        text = await r.text()
                        all_raw.extend(text.strip().split('\n'))
                except:
                    continue
            
            # Limpeza e Teste (Darwinismo Digital)
            raw_list = list(set(all_raw)) # Remove duplicatas brutas
            tasks = []
            # Tentamos como socks4 e socks5 para maximizar aproveitamento
            for p in raw_list:
                tasks.append(check_proxy(session, p, "socks4"))
                tasks.append(check_proxy(session, p, "socks5"))
            
            results = await asyncio.gather(*tasks)
            new_valid = {r for r in results if r is not None}
            
            valid_proxies = new_valid
            print(f"[HIT] Ciclo concluído. {len(valid_proxies)} proxies de elite ativos.")
        
        await asyncio.sleep(UPDATE_INTERVAL)

@app.route('/api/nectar')
def serve_proxies():
    """Endpoint que o seu Runner vai ler."""
    return "\n".join(list(valid_proxies))

if __name__ == "__main__":
    from threading import Thread
    # Inicia o motor de limpeza em segundo plano
    loop = asyncio.new_event_loop()
    t = Thread(target=lambda: loop.run_until_complete(refresh_and_clean()))
    t.start()
    
    # Inicia a API na porta 8000
    app.run(host='0.0.0.0', port=8000)
