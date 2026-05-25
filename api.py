import asyncio
import aiohttp
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time

app = FastAPI(title="Império Mutante - Proxy API API", version="1.0")

# O Cofre: Armazena os proxies vivos em tempo real
PROXIES_VIVOS = []

# Néctar: Suas fontes antigas de proxy (coloque as URLs reais aqui)
FONTES_RAW = [
    "http://api-fornecedor-1.com/proxies",
    "http://api-fornecedor-2.com/proxies"
]

async def coletar_proxies_raw():
    """O Coletor: Puxa as listas sujas das APIs parceiras."""
    print("[ENTIDADE 12] Coletando proxies brutos...")
    # Simulando a coleta (aqui você faria requests reais pras suas APIs fontes)
    # Exemplo de formato: "ip:porta"
    proxies_sujos = ["192.168.1.1:8080", "10.0.0.1:3128", "8.8.8.8:80"] 
    return proxies_sujos

async def checar_proxy(session, proxy):
    """O Carrasco: Testa se o proxy está vivo com timeout brutal."""
    url_teste = "http://gstatic.com/generate_204"
    proxy_url = f"http://{proxy}"
    try:
        async with session.get(url_teste, proxy=proxy_url, timeout=5) as response:
            if response.status == 204:
                return proxy
    except Exception:
        return None
    return None

async def tribunal_de_proxies():
    """A Execução: Roda a cada 20 minutos. Coleta, checa e atualiza o Cofre."""
    print(f"[ENTIDADE 12] Iniciando ciclo de checagem. [{time.strftime('%X')}]")
    global PROXIES_VIVOS
    
    proxies_sujos = await coletar_proxies_raw()
    
    # Execução assíncrona: Testa todos de uma vez (Latência Negativa)
    async with aiohttp.ClientSession() as session:
        tarefas = [checar_proxy(session, p) for p in proxies_sujos]
        resultados = await asyncio.gather(*tarefas)
    
    # Filtra apenas os que sobreviveram
    proxies_aprovados = [p for p in resultados if p is not None]
    PROXIES_VIVOS = proxies_aprovados
    
    print(f"[ENTIDADE 12] Ciclo completo. {len(PROXIES_VIVOS)} Proxies prontos para guerra.")

# --- INICIALIZAÇÃO DO MOTOR ---

@app.on_event("startup")
async def iniciar_operacao():
    """Inicia o relógio que vai girar a máquina a cada 20 minutos."""
    # Roda a primeira vez ao ligar o servidor
    await tribunal_de_proxies() 
    
    # Configura o Scheduler para rodar de 20 em 20 min
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tribunal_de_proxies, 'interval', minutes=20)
    scheduler.start()

# --- A SUA NOVA API (A ROTA DE FUGA) ---

@app.get("/api/v1/proxies")
async def obter_proxies():
    """Endpoint da sua Nova API. Retorna Margem Infinita."""
    return {
        "status": "sucesso",
        "total_ativos": len(PROXIES_VIVOS),
        "proxies": PROXIES_VIVOS
    }