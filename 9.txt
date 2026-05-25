import asyncio
import aiohttp
import time

# O Alvo: Testar se o proxy esconde nosso IP real e se está vivo
TEST_URL = "http://httpbin.org/get"
ELITE_POOL = set()

async def testar_proxy_elite(session, proxy):
    try:
        # Define um timeout brutal: se demorar mais de 3s, é Carrasco (descarta)
        async with session.get(TEST_URL, proxy=f"http://{proxy}", timeout=3) as response:
            if response.status == 200:
                data = await response.json()
                headers = data.get("headers", {})
                
                # Regra de Ouro L1 (Elite): Sem rastro
                if "Via" not in headers and "X-Forwarded-For" not in headers:
                    print(f"[+] NÉCTAR PURO: {proxy}")
                    ELITE_POOL.add(proxy)
                    return proxy
    except Exception:
        pass # Latência Negativa: Falhou, ignora silenciosamente e passa pro próximo
    return None

async def minerar_lista(lista_de_proxies):
    print("[!] Iniciando Auditoria Rival: Varrendo Lista...")
    async with aiohttp.ClientSession() as session:
        tasks = [testar_proxy_elite(session, proxy) for proxy in lista_de_proxies]
        await asyncio.gather(*tasks)
    
    print(f"[*] Operação concluída. Ativos Elite capturados: {len(ELITE_POOL)}")

# Exemplo: O Supra-Codex raspa os sites e joga aqui
# asyncio.run(minerar_lista(["ip:porta", "ip:porta", ...]))