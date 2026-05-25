import os
import glob
import mmap
from multiprocessing import Pool, cpu_count

# --- ARSENAL DE ATIVOS (Dicionário Consolidado) ---
ativos_imperio = {
    "GAMING_HIGH_TICKET": ["habbo", "konami", "nintendo", "pokemon", "playstation", "supercell", "minecraft", "eagames", "ubisoft", "activision", "valorant", "rockstar", "imvu", "roblox", "robux", "riot", "steam", "epic", "battlenet", "tarkov", "gog", "genshin", "hoyoverse", "xbox", "gamepass", "tencent", "moonton", "garena", "freefire", "pubg", "csgo", "origin", "discord", "faceit", "esea", "skinport", "bitskins", "dmarket", "buff163", "pathofexile"],
    "INFRA_ELITE_NETWORK": ["rdp", "vps", "vpn", "proxy", "aws", "azure", "gcloud", "digitalocean", "linode", "nordvpn", "expressvpn", "surfshark", "cyberghost", "hetzner", "vultr", "ovh", "hostinger", "namecheap", "godaddy", "cloudflare", "smtp", "cpanel", "whm", "ssh", "dedicate", "domain", "ssl", "ngrok", "tailscale", "proxmox", "vmware", "akamai", "fastly", "shodan", "censys", "dehashed"],
    "FINTECH_GLOBAL_ARBITRAGE": ["exchan", "neteller", "pay", "eth", "exodus", "faucet", "miner", "blockchain", "wallet", "btc", "coin", "doge", "dollar", "skrill", "payoneer", "trust", "metamask", "binance", "stripe", "kucoin", "okx", "phantom", "ronin", "payeer", "advcash", "perfectmoney", "wise", "revolut", "kraken", "mexc", "gateio", "trezor", "ledger", "coinbase", "venmo", "cashapp", "zelle", "braintree", "adyen", "paypal", "picpay", "mercadopago", "pix", "usdt", "solana", "polygon", "ltc", "defi", "dex", "bingx", "phemex", "coinex", "changelly", "changenow", "paxum", "epayments", "mercury", "revolutbusiness", "wirex", "blackcatcard"],
    "ECOMMERCE_INFOPRODUTOS_LUXO": ["kiwify", "gumroad", "hotmart", "eduzz", "ticto", "braip", "kirvano", "monetizze", "payt", "kajabi", "teachable", "thinkific", "clickfunnels", "gohighlevel", "skool"],
    "GREY_MARKET_POWER": ["g2a", "eneba", "eldorado", "playerauctions", "kinguin", "cdkeys", "zeerk", "igvault", "z2u", "epicnpc", "ogusers", "crackedio", "nulledio", "breachforums", "ownedcore"],
    "IA_BIO_WEALTH_AGENTS": ["chatgpt", "openai", "claude", "elevenlabs", "runway", "midjourney", "anthropic", "replicate", "huggingface", "leonardo", "synthesia", "descript", "copyai", "pika", "scaleai", "gemini", "jasper", "ollama", "anythingllm", "langchain", "copilot", "perplexity", "stablediffusion", "mistral", "sora", "characterai", "perceive", "neuroama", "biorender", "pubmed", "dnaweekly"],
    "STREAMING_PREMIUM": ["dazn", "plex", "netflix", "spotify", "crunchyroll", "hbo", "disney", "tidal", "primevideo", "youtube", "twitch", "paramount", "appletv", "deezer", "kick", "ufcfightpass", "nba-leaguepass", "f1tv", "peacock", "mubi"],
    "ENTERPRISE_SAAS_DEV": ["adobe", "canva", "envato", "figma", "github", "notion", "shopify", "wordpress", "wix", "trello", "slack", "docker", "vscode", "framer", "webflow", "monday", "asana", "salesforce", "hubspot", "jira", "confluence", "bitbucket"],
    "MARKETING_BLACKHAT_ADTECH": ["smm", "semrush", "ahrefs", "adsense", "taboola", "outbrain", "propellerads", "adsterra", "clickbank", "digistore24", "maxbounty", "crackrevenue", "cpa", "seo", "backlink", "traffic", "fbads", "googleads", "tiktokads", "tracker", "keitaro", "cpagrip", "cpalead", "mylead", "lospollos", "monetag", "adspirit", "voluum", "bemob", "adsbridge", "spyover", "adplexity"],
    "SOCIAL_DATING_ELITE": ["onlyfans", "fansly", "chaturbate", "cam4", "badoo", "tinder", "tindergold", "bumble", "instagram", "tiktok", "privacy", "patreon", "telegram", "discordnitro", "seeking", "raya", "luxy", "okcupid", "fetlife", "loyalfans"],
    "RISK_PRO_BETTING": ["giftcard", "option", "captcha", "prize", "reward", "buy", "shop", "spin", "vip", "stake", "bcgame", "gamdom", "csgoroll", "aviator", "blaze", "roleta", "cassino", "crash", "slots", "aposta", "lootbox", "bet365", "betfair", "pinnacle", "1xbet", "ggbet", "stake-us", "rollbit"],
    "DATA_SCRAPING_EXTRACTORS": ["playwright", "puppeteer", "selenium", "apify", "brightdata", "scrapy", "beautifulsoup", "zenrows", "scrapingbee", "oxylabs", "smartproxy", "crawlbase"],
    "NET_DA_RUA_NDR": ["starlink", "ipfs", "ubiquiti", "unifi", "helium", "zerotier"],
    "CYBER_OSINT_AUDIT": ["maltego", "spiderfoot", "intelx", "hunterio", "builtwith"],
    "BIO_WEALTH_ELITE": ["insidetracker", "levels", "ouraring", "whoop"],
    "CLUSTER_ORCHESTRATION": ["n8n", "kubernetes", "terraform", "ansible", "docker-swarm"],
    "LUXURY_DIGITAL_VAULT": ["sothebys", "opensea-pro", "superrare", "foundation"]
}

OUTPUT_FOLDER = "RESULTADOS_ORGANIZADOS"
FLUSH_LIMIT = 50000

def descarregar_pro_disco(buffer):
    """Refinaria: Salva por Categoria E por Keyword específica."""
    for categoria, hits_por_keyword in buffer.items():
        path_cat = os.path.join(OUTPUT_FOLDER, categoria)
        os.makedirs(path_cat, exist_ok=True)
        
        for keyword, linhas in hits_por_keyword.items():
            if linhas:
                output_file = os.path.join(path_cat, f"{keyword}_PARCIAL.txt")
                with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
                    f.write("\n".join(linhas) + "\n")

def processo_blindado(arquivo):
    """Leitura mmap com injeção direta por Keyword."""
    try:
        tamanho_arquivo = os.path.getsize(arquivo)
        if tamanho_arquivo == 0: return f"[-] Ignorado: {arquivo} (Vazio)"

        buffer = {cat: {kw: [] for kw in palavras} for cat, palavras in ativos_imperio.items()}
        hits_totais = 0

        with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for linha_bytes in iter(mm.readline, b""):
                    linha = linha_bytes.decode('utf-8', errors='ignore').strip()
                    if not linha: continue
                    
                    linha_lower = linha.lower()
                    encontrado = False
                    
                    for categoria, palavras in ativos_imperio.items():
                        for p in palavras:
                            if p in linha_lower:
                                buffer[categoria][p].append(linha)
                                hits_totais += 1
                                encontrado = True
                                break
                        if encontrado: break
                            
                    if hits_totais >= FLUSH_LIMIT:
                        descarregar_pro_disco(buffer)
                        buffer = {cat: {kw: [] for kw in palavras} for cat, palavras in ativos_imperio.items()}
                        hits_totais = 0
                        
        descarregar_pro_disco(buffer)
        return f"[+] REFINADO: {arquivo}"
    except Exception as e:
        return f"[!] FALHA em {arquivo}: {e}"

def apogeu_merge():
    """/CARRASCO: Deduplicação Nativa Windows (Pure Python)."""
    print("[*] EXECUTANDO PROTOCOLO /CARRASCO: Purga de Duplicatas...")
    for categoria, palavras in ativos_imperio.items():
        path = os.path.join(OUTPUT_FOLDER, categoria)
        if not os.path.exists(path): continue
        
        for kw in palavras:
            arquivo_parcial = os.path.join(path, f"{kw}_PARCIAL.txt")
            if not os.path.exists(arquivo_parcial): continue
            
            arquivo_final = os.path.join(path, f"{kw}_TOTAL.txt")
            
            # --- MOTOR DE DEDUPLICAÇÃO NATIVO ---
            try:
                with open(arquivo_parcial, 'r', encoding='utf-8', errors='ignore') as f:
                    # Usamos set para garantir unicidade com Custo Zero de complexidade
                    conteudo_unico = sorted(list(set(f.read().splitlines())))
                
                with open(arquivo_final, 'w', encoding='utf-8') as f:
                    f.write("\n".join(conteudo_unico) + "\n")
                
                os.remove(arquivo_parcial) # Purga do rastro
            except Exception as e:
                print(f"[!] Erro ao processar {kw}: {e}")

def executar_soberania():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    # Busca todos os TXTs, ignorando a pasta de output para evitar loop
    arquivos = [f for f in glob.glob("*.txt") if OUTPUT_FOLDER not in f]
    
    if not arquivos:
        print("[!] Nenhum alvo encontrado na zona de operação.")
        return

    nucleos = cpu_count()
    print(f"[*] MOTOR WINDOWS ATIVADO: {nucleos} núcleos em Ponto de Ignição.")
    
    with Pool(processes=nucleos) as pool:
        for resultado in pool.imap_unordered(processo_blindado, arquivos):
            print(resultado)

    apogeu_merge()
    print("\n[+] SUCESSO: Refinaria Windows operacional. Ativos de Luxo consolidados.")

if __name__ == "__main__":
    executar_soberania()