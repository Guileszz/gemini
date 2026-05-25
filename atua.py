import os
import shutil

def mover_arquivos_force():
    # TRUQUE DE MESTRE: Pega o caminho exato de onde este arquivo .py está salvo
    caminho_real = os.path.dirname(os.path.abspath(__file__))
    
    print(f"--- 📍 LOCALIZANDO ARQUIVOS EM: {caminho_real} ---\n")
    
    # Lista tudo que tem nessa pasta
    itens = os.listdir(caminho_real)
    arquivos = [f for f in itens if os.path.isfile(os.path.join(caminho_real, f))]
    
    print(f"🔎 Arquivos detectados: {len(arquivos)}")
    
    if len(arquivos) < 2:
        print("⚠️ ALERTA: Nenhum arquivo encontrado (além do script).")
        print("Certifique-se de que este script está salvo DENTRO da pasta 03_CONFIGS.")
        input("Enter para sair...")
        return

    # Definição das Categorias
    categorias = {
        "01_FINANCE_CRYPTO": ["paypal", "stripe", "binance", "coin", "wallet", "bank", "cc ", "card", "braintree", "crypto", "money", "invest", "pagseguro", "mercadopago", "nubank", "picpay", "cash", "cvv", "metamask"],
        "02_BET_CASINO": ["bet", "casino", "blaze", "stake", "win", "spin", "poker", "vegas", "sorte", "gamehag", "aviator", "lottery", "jogos", "roleta"],
        "03_ADULTO_18": ["porn", "sex", "xvideos", "beeg", "adult", "cam", "hentai", "brazzers", "onlyfans", "strip", "bonga", "chaturbate", "redtube", "erotic", "flirt", "bongamodels"],
        "04_HOSTING_RDP": ["host", "cloud", "azure", "vps", "rdp", "server", "dedicado", "domain", "godaddy", "namecheap", "bluehost", "cpanel", "hetzner", "digitalocean", "aws", "webmail"],
        "05_GAMES": ["steam", "roblox", "fortnite", "xbox", "playstation", "psn", "ubisoft", "epic", "game", "minecraft", "riot", "lol", "konami", "nintendo", "freefire", "cod", "warzone"],
        "06_SOCIAL_MEDIA": ["facebook", "instagram", "twitter", "tiktok", "discord", "telegram", "linkedin", "pinterest", "reddit", "snapchat", "tinder", "badoo", "bumble", "social", "what"],
        "07_STREAMING_MUSIC": ["netflix", "disney", "spotify", "hulu", "crunchyroll", "prime", "hbo", "tv", "plus", "play", "music", "deezer", "globo", "paramount", "youtube", "twitch", "iptv", "plex"],
        "08_VIAGEM": ["booking", "airbnb", "uber", "99", "flight", "airline", "trip", "hotel", "travel", "milhas", "latam", "azul", "gol", "expedia", "trivago"],
        "09_FOOD": ["food", "delivery", "ifood", "glovo", "rappi", "mcdonald", "burger", "pizza", "eat", "fome", "subway", "kfc"],
        "10_EMAIL_ACCESS": ["hotmail", "outlook", "yahoo", "gmail", "mail", "inbox", "access", "proton", "bol", "uol", "terra"],
        "11_VPN_PROXY": ["vpn", "proxy", "ip2", "socks", "nord", "express", "security", "hma", "tunnel", "surfshark", "cyberghost", "hide"],
        "12_SHOPPING": ["amazon", "walmart", "shop", "store", "mercado", "bahia", "magalu", "express", "ali", "shopee", "ebay", "bestbuy", "target", "nike", "adidas"],
        "13_TOOLS_AI": ["gpt", "ai", "chat", "bot", "labs", "sonic", "midjourney", "write", "udemy", "coursera", "brainly", "duolingo", "chegg", "scribe"],
        "99_OUTROS": [] 
    }

    movidos_count = 0

    print("🚀 INICIANDO MOVIMENTAÇÃO...\n")

    for arquivo in arquivos:
        nome_lower = arquivo.lower()
        
        # Pula o próprio script e o arquivo de lista
        if arquivo in ["mover_arquivos.py", "organizar.py", "LISTA_ORGANIZADA.txt"]:
            continue

        pasta_destino = "99_OUTROS"
        
        # Lógica de Classificação
        categorizado = False
        for pasta, keywords in categorias.items():
            if pasta == "99_OUTROS": continue
            if any(key in nome_lower for key in keywords):
                pasta_destino = pasta
                categorizado = True
                break
        
        # Caminho completo
        caminho_pasta_dest = os.path.join(caminho_real, pasta_destino)
        
        # Cria a pasta SE não existir
        if not os.path.exists(caminho_pasta_dest):
            try:
                os.makedirs(caminho_pasta_dest)
            except:
                pass # Ignora erro de pasta já existente

        # Tenta mover
        try:
            shutil.move(os.path.join(caminho_real, arquivo), os.path.join(caminho_pasta_dest, arquivo))
            movidos_count += 1
            # Feedback visual a cada 50 arquivos pra não travar a tela
            if movidos_count % 50 == 0:
                print(f"⚡ {movidos_count} arquivos processados...")
        except Exception as e:
            print(f"❌ Erro ao mover {arquivo}: {e}")

    print("\n" + "="*40)
    print(f"✅ MISSÃO CUMPRIDA!")
    print(f"📂 Total Movido: {movidos_count}")
    print("="*40)

if __name__ == "__main__":
    mover_arquivos_force()
    input("\nPressione ENTER para fechar...")