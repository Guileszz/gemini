import requests
import re
import concurrent.futures
import urllib3
import time
import random
import os

# Protocolo de Silêncio SSL (Zero Day do Bem)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# CONFIGURAÇÃO DE GUERRA (ENTIDADE 12)
# ==============================================================================
TIMEOUT_EXTRACAO = 15
ARQUIVO_SAIDA = "MUNICAO_TOTAL_MUTANTE.txt"
REGEX_IP_PORTA = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b'

AGENTES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
]

# DICIONÁRIO DE FONTES (EXPANSÃO TOTAL - SEM REPETIÇÕES)
FROTA_PROXIES = {
    "NOVAS_ELITE_SOCKS5": [
        "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/Tuan-Nguyen-Anh/Proxy-List/main/socks5.txt",
        "https://raw.githubusercontent.com/andres-ml/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/elliott00/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/Hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/proxyspace/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/sk5s/proxy/main/socks5.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
        "https://proxyspace.pro/socks5.txt",
        "https://spys.me/socks.txt",
        "https://raw.githubusercontent.com/Obscurely/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/Simatwa/free-proxies/main/files/socks5.txt",
        "https://raw.githubusercontent.com/r00tee/Proxy-List/main/socks5.txt"
    ],
    
    "NOVAS_HTTP_HTTPS_VOLUME": [
        "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/Tuan-Nguyen-Anh/Proxy-List/main/http.txt",
        "https://raw.githubusercontent.com/andres-ml/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/andres-ml/proxy-list/main/https.txt",
        "https://raw.githubusercontent.com/elliott00/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/ob03/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/Ch4r1l3/ProxyList/main/http.txt",
        "https://raw.githubusercontent.com/Mr-R007/Proxy-List/main/http.txt",
        "https://proxyspace.pro/http.txt",
        "https://proxyspace.pro/https.txt",
        "https://raw.githubusercontent.com/Complex-Proxy/free-proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/Simatwa/free-proxies/main/files/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
        "https://raw.githubusercontent.com/r00tee/Proxy-List/main/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=https"
    ],
    
    "NOVAS_SOCKS4_GHOSTS": [
        "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/Tuan-Nguyen-Anh/Proxy-List/main/socks4.txt",
        "https://raw.githubusercontent.com/andres-ml/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/elliott00/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/proxyspace/proxy-list/master/socks4.txt",
        "https://proxyspace.pro/socks4.txt",
        "https://raw.githubusercontent.com/Obscurely/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/Simatwa/free-proxies/main/files/socks4.txt",
        "https://raw.githubusercontent.com/r00tee/Proxy-List/main/socks4.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt"
    ],

    "FONTES_ESTRUTURA_ANTERIOR": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=3000&country=all&ssl=all&anonymity=elite",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=elite",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=3000&country=all&ssl=all&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt"
    ]
}

def get_all_sources():
    """Une todas as listas em um set para garantir URLs únicas."""
    urls = set()
    for categoria in FROTA_PROXIES.values():
        urls.update(categoria)
    return list(urls)

def raspar_site(url):
    headers = {'User-Agent': random.choice(AGENTES)}
    try:
        resposta = requests.get(url, headers=headers, timeout=TIMEOUT_EXTRACAO, verify=False)
        if resposta.status_code == 200:
            # Captura o padrão IP:PORTA no texto bruto
            return re.findall(REGEX_IP_PORTA, resposta.text)
    except:
        pass
    return []

if __name__ == "__main__":
    ALVOS = get_all_sources()
    inicio = time.time()
    
    print(f"\n[+] IMPÉRIO MUTANTE - INICIANDO EXTRAÇÃO EM LARGA ESCALA [+]")
    print(f"[+] TOTAL DE FONTES ÚNICAS: {len(ALVOS)}")

    todos_proxies = set()
    
    # Aumentando o paralelismo para 100 workers para suportar a nova carga
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futuros = {executor.submit(raspar_site, url): url for url in ALVOS}
        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                todos_proxies.update(resultado)

    if todos_proxies:
        # Salva a munição em ordem para facilitar auditoria
        with open(ARQUIVO_SAIDA, "w") as f:
            for p in sorted(todos_proxies):
                f.write(f"{p}\n")
        
        print(f"\n[✔] SOBERANIA: {len(todos_proxies)} proxies extraídos (Deduplicados).")
        print(f"[✔] ARQUIVO GERADO: {ARQUIVO_SAIDA}")
        print(f"[✔] TEMPO DE EXECUÇÃO: {time.time() - inicio:.2f}s")
    else:
        print("[!] ERRO: O arsenal está vazio. Verifique a conexão.")