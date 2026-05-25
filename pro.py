import asyncio
import aiohttp
import re
import os

# Fontes de Néctar - Escala Total e Repositórios Zero Day
SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite",
    "https://www.proxy-list.download/api/v1/get?type=http&anon=elite",
    "https://www.proxyscan.io/download?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/rooster666/proxy-list/main/http.txt"
]

# Configurações de Soberania
TARGET_COUNTRIES = ['BR', 'PT', 'GB'] # Alvos: Brasil, Portugal, UK
TEST_URL = "http://httpbin.org/get"
ELITE_FILE = "elite.txt"
LATENCY_LIMIT = 1.5 # Filtro de Latência Brutal para Flow máximo

async def check_geo_and_save(session, proxy):
    try:
        # 1. Validação de Elite L1 com Timeout de 1.5s (Latência Negativa)
        async with session.get(TEST_URL, proxy=f"http://{proxy}", timeout=LATENCY_LIMIT) as res:
            if res.status == 200:
                data = await res.json()
                headers = data.get("headers", {})
                
                # Critério Elite: Sem rastro do IP real
                if "Via" not in headers and "X-Forwarded-For" not in headers:
                    
                    # 2. Identificação de Território (Geolocalização)
                    async with session.get(f"http://ip-api.com/json/{proxy.split(':')[0]}", timeout=2) as geo_res:
                        geo_data = await geo_res.json()
                        country_code = geo_data.get('countryCode')
                        
                        if country_code in TARGET_COUNTRIES:
                            print(f"[+] NÉCTAR {country_code} RÁPIDO IDENTIFICADO: {proxy}")
                            with open(ELITE_FILE, "a") as f:
                                # Salva com comentário para fácil auditoria manual
                                f.write(f"{proxy} # {country_code}\n")
    except:
        pass # Ignora falhas para manter a fluidez

async def ciclo_mineracao():
    while True:
        print("\n" + "="*40)
        print("[!] IMPÉRIO MUTANTE: INICIANDO CICLO DE MINERAÇÃO GLOBAL")
        print(f"[*] Alvos: {TARGET_COUNTRIES} | Latência Máx: {LATENCY_LIMIT}s")
        print("="*40)
        
        # Auto-Purge: Limpa a lista antiga para garantir apenas ativos frescos
        if os.path.exists(ELITE_FILE):
            open(ELITE_FILE, 'w').close() 

        async with aiohttp.ClientSession() as session:
            all_proxies = []
            for url in SOURCES:
                try:
                    async with session.get(url, timeout=10) as res:
                        text = await res.text()
                        # Extração via Regex de todos os IPs e portas
                        found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text)
                        all_proxies.extend(found)
                except: continue
            
            unique_proxies = list(set(all_proxies))
            print(f"[*] {len(unique_proxies)} IPs brutos capturados. Iniciando Auditoria...")
            
            # Disparo em massa das tarefas de validação
            tasks = [check_geo_and_save(session, proxy) for proxy in unique_proxies]
            await asyncio.gather(*tasks)
            
        print("\n[*] Ciclo finalizado. Dormindo 15 min para evitar ban...")
        await asyncio.sleep(900) # Loop de 15 minutos

if __name__ == "__main__":
    try:
        asyncio.run(ciclo_mineracao())
    except KeyboardInterrupt:
        print("\n[!] Operação encerrada pelo Imperador.")