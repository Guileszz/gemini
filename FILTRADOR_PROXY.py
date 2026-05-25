import requests, socks, socket, threading, time, os
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)
ARQUIVO_OUTPUT = "proxy_validos.txt"
FONTES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=1000&country=all&ssl=all&anonymity=all"
]

lock = threading.Lock()

def validar_e_salvar(proxy):
    try:
        ip, porta = proxy.split(':')
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, ip, int(porta))
        s.settimeout(5) # Aumentado levemente para maior precisão
        s.connect(("8.8.8.8", 53))
        s.close()
        
        with lock:
            with open(ARQUIVO_OUTPUT, "a") as f:
                f.write(f"{proxy}\n")
                f.flush()
                os.fsync(f.fileno())
        print(f"{Fore.GREEN}[+] SOCKS5 VIVO: {proxy}")
    except: pass

def motor_filtro():
    print(f"{Fore.CYAN}--- INICIANDO CAÇA AOS PROXIES (IMPÉRIO MUTANTE) ---")
    # Não removemos mais o arquivo para não interromper o IMAP.py
    
    while True:
        brutos = set()
        print(f"{Fore.YELLOW}[!] Coletando munição fresca...")
        for url in FONTES:
            try:
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    linhas = [p.strip() for p in r.text.splitlines() if ":" in p]
                    brutos.update(linhas)
            except: pass
        
        print(f"{Fore.MAGENTA}[#] Testando {len(brutos)} alvos com 150 Workers...")
        with ThreadPoolExecutor(max_workers=150) as exe: 
            exe.map(validar_e_salvar, list(brutos))
        
        print(f"{Fore.GREEN}[V] Ciclo completo. Reiniciando varredura em 5 segundos...")
        time.sleep(5) # Respiro tático para evitar sobrecarga

if __name__ == "__main__":
    motor_filtro()