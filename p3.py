import requests
import re
import concurrent.futures
import urllib3
import time
import random

# Protocolo de Silêncio SSL (Zero Day do Bem)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# CONFIGURAÇÃO DE GUERRA (ENTIDADE 12 - MOTOR)
# ==============================================================================
TIMEOUT_EXTRACAO = 12
ARQUIVO_SAIDA = "MUNICAO_V3_INFINITA.txt"
REGEX_IP_PORTA = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b'

AGENTES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
]

# NOVAS FONTES V3 - SEM REPETIÇÕES COM O ARSENAL ANTERIOR
FROTA_V3 = {
    "SOCKS5_DEEP": [
        "https://raw.githubusercontent.com/yemreay/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/Isham-G/Proxy-List/main/socks5.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks5.txt",
        "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt"
    ],
    "HTTP_HTTPS_VOLUME_V3": [
        "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/http.txt",
        "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
        "https://rootjazz.com/proxies/proxies.txt"
    ],
    "SOCKS4_SHADOW_V3": [
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt"
    ]
}

def get_targets():
    """Unifica e garante que não há URLs duplicadas no próprio dicionário V3."""
    unificados = set()
    for categoria in FROTA_V3.values():
        unificados.update(categoria)
    return list(unificados)

def raspar_v3(url):
    headers = {'User-Agent': random.choice(AGENTES)}
    try:
        res = requests.get(url, headers=headers, timeout=TIMEOUT_EXTRACAO, verify=False)
        if res.status_code == 200:
            return re.findall(REGEX_IP_PORTA, res.text)
    except:
        pass
    return []

if __name__ == "__main__":
    ALVOS = get_targets()
    inicio = time.time()
    
    print(f"\n[+] {12} - INICIANDO EXPANSÃO V3 (MODO SEM API) [+]")
    print(f"[+] ALVOS DE ELITE: {len(ALVOS)}")

    micao_v3 = set()
    
    # Escala bruta com 100 workers para garantir Margem Infinita
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as motor:
        tasks = {motor.submit(raspar_v3, url): url for url in ALVOS}
        for task in concurrent.futures.as_completed(tasks):
            resultado = task.result()
            if resultado:
                micao_v3.update(resultado)

    if micao_v3:
        with open(ARQUIVO_SAIDA, "w") as f:
            for proxy in sorted(micao_v3):
                f.write(f"{proxy}\n")
        
        print(f"\n[✔] SOBERANIA ALCANÇADA: {len(micao_v3)} novos ativos extraídos.")
        print(f"[✔] ARQUIVO: {ARQUIVO_SAIDA}")
        print(f"[✔] FLOW TIME: {time.time() - inicio:.2f}s")
    else:
        print("[!] ERRO: Fontes V3 inacessíveis ou vazias.")