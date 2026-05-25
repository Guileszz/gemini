# =========================================================
# IMPÉRIO MUTANTE - ARSENAL DE FONTES (NÉCTAR BRUTO)
# =========================================================

# FONTES ELITE: Alta probabilidade de SOCKS5 e Baixa Latência
FONTES_ELITE = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/Hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    # [ADICIONE SUAS LISTAS DE SOCKS5 AQUI]
]

# FONTES DE VOLUME: HTTP/S para Scraping Massivo
FONTES_VOLUME = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    # [ADICIONE SUAS LISTAS DE HTTP AQUI]
]

# FONTES GHOST: SOCKS4 e listas mistas
FONTES_GHOST = [
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    # [ADICIONE SUAS LISTAS DE SOCKS4 AQUI]
]

# UNIFICAÇÃO DO ARSENAL (O que a API vai consumir)
TODAS_AS_FONTES = list(set(FONTES_ELITE + FONTES_VOLUME + FONTES_GHOST))

def status_do_arsenal():
    """Auditoria rápida de munição disponível."""
    print(f"[!] MÓDULO FONTES: {len(TODAS_AS_FONTES)} bases de dados prontas para extração.")