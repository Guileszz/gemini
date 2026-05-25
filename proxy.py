import concurrent.futures
import requests

# Arsenal de Endpoints (As 15 fontes de SOCKS5)
URLS = [
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
]

# Camuflagem de Navegador (Evita o block do GitHub)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def extrair_proxies(url):
    """Puxa a lista bruta de cada URL com bypass de segurança."""
    proxies_encontradas = set()
    try:
        # Adicionado timeout menor e headers reais
        resposta = requests.get(url, headers=HEADERS, timeout=8)
        if resposta.status_code == 200:
            linhas = resposta.text.splitlines()
            for linha in linhas:
                linha = linha.strip()
                if ":" in linha and not linha.startswith("#"):
                    proxies_encontradas.add(linha)
            print(f"[+] Sucesso: {url.split('/')[-2] if 'master' not in url else url.split('/')[-1]}")
    except Exception as e:
        print(f"[-] Falha ao acessar {url.split('/')[-1]}: {e}")
    return proxies_encontradas


def main():
    todas_proxies = set()

    print("[*] Iniciando extração em massa (Paralelismo Ativado)...")

    # 15 workers para puxar tudo ao mesmo tempo no talo
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        resultados = executor.map(extrair_proxies, URLS)

        for resultado in resultados:
            todas_proxies.update(resultado)

    arquivo_saida = "socks5_extraidas.txt"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for proxy in sorted(todas_proxies):
            f.write(f"{proxy}\n")

    print("---")
    print(f"[!] Operação Concluída. Arquivo gerado: {arquivo_saida}")
    print(f"[!] Total de Proxies Únicas Extraídas: {len(todas_proxies)}")

    print("\n" + "=" * 50)
    input("[!] Pressione ENTER para fechar a janela...")


if __name__ == "__main__":
    main()