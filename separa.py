import os
import glob
from multiprocessing import Pool, cpu_count

# ARSENAL CONSOLIDADO (Soberania Total)

RAW_KEYWORDS = [

    ".edu", ".gov", "1xbet", "777", "abbott", "activision", "ada", "adobe", "adsense", "adspy", "advcash", "ahrefs", "airbnb", "aliexpress", "alipay", "amazon", "amex", "anthropic", "anydesk", "api", "apple", "atomic", "avast", "aviator", "aws", "azure", "badoo", "banxa", "battlenet", "bazaar", "bdo", "bet", "bit", "blaze", "blizzard", "bnb", "booking", "bradesco", "braintree", "bridge", "btc", "buff163", "bumble", "bustabit", "bybit", "caixa", "cam4", "canva", "captcha", "cashapp", "casino", "char", "chatgpt", "chaturbate", "checkout", "cipsoft", "claude", "clickbank", "cloudflare", "coin", "copyai", "cosmote", "crackrevenue", "crunchyroll", "csmoney", "cupon", "dazn", "dell", "descript", "digitalocean", "disney", "dmarket", "dofus", "doge", "dollar", "dot", "dropispy", "duelbits", "eagames", "ebay", "eduzz", "eldorado", "elevenlabs", "eneba", "envato", "epic", "esxi", "estatisticas", "eth", "exchan", "exodus", "facebook", "fansly", "faucet", "figma", "firebase", "fiverr", "freelancer", "g2a", "gamepass", "gamdom", "gate.io", "gcloud", "genshin", "github", "glove", "godaddy", "gog", "google", "growth", "habbo", "hbo", "hellcase", "heroku", "hetzner", "highlevel", "hostinger", "hotmart", "hoyoverse", "huggingface", "ibm", "icard", "icloud", "idrive", "imvu", "instagram", "intel", "inter", "inventory", "itau", "jasper", "key-drop", "kinguin", "kiwify", "knife", "konami", "kraken", "kucoin", "ledger", "leonardo", "lineage", "linode", "linux", "logmein", "market", "matic", "maxbounty", "medivia", "membros", "mercadopago", "mercuryo", "metamask", "metin2", "microsoft", "midjourney", "minecraft", "miner", "moonpay", "mql5", "namecheap", "netflix", "neteller", "nintendo", "noones", "notion", "nubank", "nvidia", "okx", "onlyfans", "openai", "option", "orange", "oracle", "otserv", "outbrain", "ovh", "pancake", "panel", "paxful", "paxum", "pay", "perfectmoney", "phantom", "pika", "playstation", "plesk", "plex", "poker", "pokemon", "prize", "proton", "proxmox", "proxy", "quora", "rdp", "replicate", "reseller", "revolut", "reward", "riot", "roblox", "rockstar", "rollbit", "ronin", "runway", "samsung", "santander", "scaleai", "seed", "semrush", "shopify", "skin", "skrill", "slot", "smm", "smtp", "sol", "spin", "spotify", "ssh", "steam", "stripe", "supercell", "swap", "synthesia", "taboola", "tarkov", "telegram", "tidal", "tibia", "tinder", "toloka", "trade", "trezor", "trust", "tutanota", "twitter", "ubisoft", "unity", "uniswap", "unreal", "upwork", "valorant", "venmo", "vibe", "vps", "vultr", "wallet", "walmart", "webhook", "whm", "wise", "workana", "xbox", "xrp", "yahoo", "zelle", "zoho"
]

# /CARRASCO: Prioridade para os termos mais longos (mais específicos)
KEYWORDS = sorted(list(set(RAW_KEYWORDS)), key=len, reverse=True)
OUTPUT_FOLDER = "RESULTADOS_40GB"

# FLUSH PROTOCOL: Buffer reduzido para você ver os arquivos "nascendo" na pasta
BUFFER_SIZE = 1000 

def triagem_streaming(arquivo):
    print(f"[*] ALVO IDENTIFICADO: {arquivo}")
    buffer_local = {key: [] for key in KEYWORDS}
    
    try:
        # Lendo em modo streaming (linha por linha) - Gasto zero de RAM
        with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                linha = linha.strip()
                # Critério de Pureza: Precisa ter ":" e não ser uma linha de código gigante
                if not linha or ":" not in linha or len(linha) > 500:
                    continue
                
                low_line = linha.lower()
                for key in KEYWORDS:
                    # Se a palavra-chave estiver na linha, capturamos o ativo
                    if key in low_line:
                        buffer_local[key].append(linha)
                        
                        # Se o balde encher, descarrega no SSD
                        if len(buffer_local[key]) >= BUFFER_SIZE:
                            path = os.path.join(OUTPUT_FOLDER, key.upper())
                            os.makedirs(path, exist_ok=True)
                            with open(os.path.join(path, f"{key}_LIVE.txt"), 'a', encoding='utf-8') as out:
                                out.write("\n".join(buffer_local[key]) + "\n")
                            buffer_local[key] = [] 
                        break # /SINCRO: Evita que a mesma linha salve em duas pastas
                        
        # Limpeza Final: Garante que os últimos dados saiam da RAM para o disco
        for key, linhas in buffer_local.items():
            if linhas:
                path = os.path.join(OUTPUT_FOLDER, key.upper())
                os.makedirs(path, exist_ok=True)
                with open(os.path.join(path, f"{key}_LIVE.txt"), 'a', encoding='utf-8') as out:
                    out.write("\n".join(linhas) + "\n")
                    
    except Exception as e:
        print(f"[!] Erro no setor {arquivo}: {e}")

def executar_soberania():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Pega todos os .txt, exceto o que já foi processado
    arquivos = [f for f in glob.glob("*.txt") if OUTPUT_FOLDER not in f]
    
    print(f"[*] MOTOR ATIVADO: {cpu_count()} núcleos detectados.")
    print(f"[*] OPERAÇÃO: Extração de Ativos em 40GB.")

    with Pool(processes=cpu_count()) as pool:
        pool.map(triagem_streaming, arquivos)

    print(f"\n[+] DOMINAÇÃO CONCLUÍDA. Verifique a pasta '{OUTPUT_FOLDER}'.")

if __name__ == "__main__":
    executar_soberania()