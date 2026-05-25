import requests
import re
import concurrent.futures
import urllib3
import time
import random

# Protocolo de Silêncio SSL - Ignora avisos de certificados em fontes instáveis
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# CONFIGURAÇÃO DE GUERRA (ENTIDADE 12)
# ==============================================================================
TIMEOUT_EXTRACAO = 15
ARQUIVO_SAIDA = "MUNICAO_TOTAL_MUTANTE.txt"
REGEX_IP_PORTA = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{2,5}\b'

AGENTES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
]

# A TRINDADE DAS FROTAS UNIFICADAS
ALVOS_RAW = list(set([
    # --- FROTA EXPANSÃO & APOGEU ---
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/wiki/gfpcom/free-proxy-list/lists/socks5.txt",
    "https://raw.githubusercontent.com/Ian-Lusule/Proxies/main/proxies/all_proxies.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/Toffanello/Free-Proxy-List/main/proxies.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    
    # --- FROTA SOCKS5 ---
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&proxy_format=ipport&format=text",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/B4RC0DE-7/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=3000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
    "https://raw.githubusercontent.com/uProxy/public-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    
    # --- FROTA HTTP/HTTPS ---
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/shiftytr/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/http.txt",
    "https://alexa.lr2b.com/proxylist.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://proxy-list.download/api/v1/get?type=https",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt"
]))

def raspar_site(url):
    headers = {'User-Agent': random.choice(AGENTES)}
    try:
        # Aumentamos o tempo de espera para fontes mais lentas, mas mantemos o fluxo
        resposta = requests.get(url, headers=headers, timeout=TIMEOUT_EXTRACAO, verify=False)
        if resposta.status_code == 200:
            ips = re.findall(REGEX_IP_PORTA, resposta.text)
            return ips
    except Exception:
        pass
    return []

if __name__ == "__main__":
    inicio = time.time()
    print(f"\n[+] IMPÉRIO MUTANTE - PROTOCOLO /SINCRO ATIVADO [+]")
    print(f"[+] ALVOS DE EXTRAÇÃO: {len(ALVOS_RAW)} fontes detectadas.\n")

    proxies_crus = set()
    
    # Operação de Alta Performance com Threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futuros = {executor.submit(raspar_site, url): url for url in ALVOS_RAW}
        for futuro in concurrent.futures.as_completed(futuros):
            res = futuro.result()
            if res:
                proxies_crus.update(res)

    # Registro do Ativo de Luxo
    if proxies_crus:
        with open(ARQUIVO_SAIDA, "w") as f:
            for proxy in sorted(proxies_crus):
                f.write(f"{proxy}\n")
        
        fim = time.time()
        print(f"[✔] SOBERANIA ALCANÇADA: {len(proxies_crus)} proxies únicos extraídos.")
        print(f"[✔] ARQUIVO: {ARQUIVO_SAIDA}")
        print(f"[✔] TEMPO DE EXECUÇÃO: {fim - inicio:.2f} segundos.")
    else:
        print("[!] FALHA NO FLUXO: Nenhuma munição encontrada. Verifique a conexão.")