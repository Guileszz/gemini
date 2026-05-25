import concurrent.futures
import requests
import os

# Arsenal de Endpoints Multiprocedural (HTTP, HTTPS, SOCKS4, SOCKS5)
URLS = [
    # --- SOCKS5 (Elite) ---
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
    # --- SOCKS4 ---
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
    # --- HTTP ---
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
    # --- HTTPS ---
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    # --- Mix/Global Sources ---
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/main/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=http"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def extrair_proxies(url):
    proxies_encontradas = set()
    try:
        # Latência Negativa: timeout de 10s para não travar o flow
        resposta = requests.get(url, headers=HEADERS, timeout=10)
        if resposta.status_code == 200:
            linhas = resposta.text.splitlines()
            for linha in linhas:
                linha = linha.strip()
                if ":" in linha and not linha.startswith(("#", "//")):
                    # Limpeza básica de protocolos escritos na linha (ex: socks5://)
                    limpa = linha.split("//")[-1] if "//" in linha else linha
                    proxies_encontradas.add(limpa)
            print(f"[+] Alvo Dominado: {url[:50]}...")
    except:
        pass 
    return proxies_encontradas

def main():
    todas_proxies = set()
    print(f"[*] /MUTAR: Iniciando extração híbrida em {len(URLS)} fontes...")

    # 50 Workers para execução instantânea
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        resultados = executor.map(extrair_proxies, URLS)
        for resultado in resultados:
            todas_proxies.update(resultado)

    # Salvando o Ativo de Luxo
    arquivo_saida = "proxy_master_hibrida.txt"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for proxy in sorted(todas_proxies):
            f.write(f"{proxy}\n")

    print("\n" + "---" * 15)
    print(f"[!] SOBERANIA ALCANÇADA: {len(todas_proxies)} proxies híbridas no deck.")
    print(f"[!] Arquivo mestre gerado: {arquivo_saida}")
    print(f"[*] Localização: {os.getcwd()}")
    input("\n[?] Deck carregado. Pronto para iniciar o checker de latência? (Enter)")

if __name__ == "__main__":
    main()