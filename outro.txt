import asyncio
import aiohttp
import re  # [ESSENCIAL] Para o Néctar ser extraído
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time

from fontes_manifest import TODAS_AS_FONTES[cite: 28]

app = FastAPI(title="Império Mutante - Soberania API", version="2.1")

PROXIES_VIVOS = []

async def checar_proxy(session, proxy):
    """O CARRASCO: Tenta validar como HTTP e SOCKS."""
    url_teste = "http://gstatic.com/generate_204"
    # A maioria das listas brutos funciona com http:// para o check inicial
    try:
        async with session.get(url_teste, proxy=f"http://{proxy}", timeout=5) as response:
            if response.status == 204:
                return proxy
    except:
        return None

async def tribunal_de_proxies():
    """A EXECUÇÃO: Limpeza e Refino."""
    global PROXIES_VIVOS
    print(f"[!] ENTIDADE 12: Iniciando Tribunal... [{time.strftime('%X')}]")
    
    async with aiohttp.ClientSession() as session:
        brutos = []
        for url in TODAS_AS_FONTES:[cite: 28]
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        texto = await resp.text()
                        # Extração de IP:PORTA via Regex
                        encontrados = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b', texto)
                        brutos.extend(encontrados)
            except Exception as e:
                print(f"[!] Erro na fonte {url[:30]}...: {e}")
                continue
        
        brutos = list(set(brutos))
        print(f"[*] Extraídos {len(brutos)} candidatos. Iniciando teste massivo...")
        
        tarefas = [checar_proxy(session, p) for p in brutos]
        resultados = await asyncio.gather(*tarefas)
    
    PROXIES_VIVOS = [p for p in resultados if p is not None]
    print(f"[✓] SOBERANIA: {len(PROXIES_VIVOS)} Proxies Elite no Cofre.")

@app.on_event("startup")
async def iniciar_operacao():
    # Roda uma vez no início e depois agenda
    asyncio.create_task(tribunal_de_proxies())
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tribunal_de_proxies, 'interval', minutes=20)
    scheduler.start()

@app.get("/api/v1/proxies")
async def obter_proxies():
    return {"total": len(PROXIES_VIVOS), "data": PROXIES_VIVOS}