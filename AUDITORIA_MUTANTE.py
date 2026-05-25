import os
import shutil
import string

# ==========================================
# MOTOR DE EXTRAÇÃO V4 - MODO DEUS (VARREDURA GLOBAL)
# ==========================================

# 1. ZONAS DE CAÇA (Discos Completos)
ZONAS_DE_BUSCA = [
    r"C:\\",
    r"D:\\"
]

# 2. O COFRE (Destino Final no Disco D)
DIRETORIO_DESTINO = r"D:\COFRE_IMPERIO_V4"

# 3. BLINDAGEM DO SISTEMA (Impede a máquina de quebrar o Windows)
PASTAS_PROIBIDAS = {
    "windows", "program files", "program files (x86)", 
    "appdata", "programdata", "$recycle.bin", "system volume information",
    "temp", "msocache", "cofre_imperio_v4"
}

# 4. MATRIZ DE CATEGORIAS (Expansão Extrema)
CATEGORIAS = {
    "01_Nucleo_Musical_Lyria": [
        "rap", "funk", "beat", "refrão", "verso", "flow", "lyria", "música", 
        "letra", "rima", "mc", "punchline", "boom bap", "trap", "vocal", "bpm"
    ],
    
    "02_Copys_e_Engenharia_Mental": [
        "vsl", "funil", "conversão", "roi", "oferta", "cta", "copywriting", 
        "script de vendas", "gatilho mental", "página de vendas", "upsell", "checkout"
    ],

    "03_Maquina_Trafego_Viral": [
        "tiktok", "instagram", "reels", "shorts", "retenção", "gancho", "algoritmo", 
        "viral", "tráfego orgânico", "tráfego pago", "ctr"
    ],
    
    "04_Projetos_High_Ticket": [
        "protocolo infra zero", "o gestor de império", "império ganha grana", 
        "protocolos secretos do drop 2026", "algoritmo i.a", "o arsenal visual", 
        "escala", "esteira de produtos", "plr"
    ],
    
    "05_Codigos_e_Automacao_Python": [
        "python", "script", "bot", "scraping", "import", "def ", "automação", 
        "selenium", "pandas", "requests", "beautifulsoup"
    ],

    "06_Operacoes_Data_Cleaning": [
        "merge", "split", "limpeza de dados", "extração de texto", "manipulação", 
        "filtrar linhas", "txt", "csv", "arquivos fundidos"
    ],

    "07_Infraestrutura_Black_Hat": [
        "proxy", "vpn", "anonimato", "segurança", "socks5", "http proxy", 
        "camuflagem", "invisibilidade", "ip", "mascarar", "contingência"
    ],

    "08_Arsenal_Visual_e_Prompts": [
        "prompt", "midjourney", "stable diffusion", "canva pro", "geração de imagem", 
        "design", "criativos", "nano banana", "renderização", "aspect ratio"
    ],

    "09_Caixa_e_Estrategia_Poker": [
        "poker", "pokerstars", "bankroll", "banca", "gestão de risco", "fichas", 
        "lucro", "cash game", "torneio"
    ]
}

def resolver_conflito(caminho_destino, nome_arquivo):
    """Adiciona (A), (B), (C) se o arquivo já existir."""
    nome_base, extensao = os.path.splitext(nome_arquivo)
    letras = string.ascii_uppercase 
    
    for letra in letras:
        novo_nome = f"{nome_base}({letra}){extensao}"
        novo_caminho = os.path.join(caminho_destino, novo_nome)
        if not os.path.exists(novo_caminho):
            return novo_nome, novo_caminho
            
    contador = 1
    while True:
        novo_nome = f"{nome_base}({contador}){extensao}"
        novo_caminho = os.path.join(caminho_destino, novo_nome)
        if not os.path.exists(novo_caminho):
            return novo_nome, novo_caminho
        contador += 1

def executar_extracao():
    if not os.path.exists(DIRETORIO_DESTINO):
        os.makedirs(DIRETORIO_DESTINO)

    arquivos_extraidos = 0

    for zona in ZONAS_DE_BUSCA:
        if not os.path.exists(zona):
            print(f"[/] Zona cega. Pulando: {zona}")
            continue

        for root, dirs, files in os.walk(zona):
            # O ESCUDO: Força o script a ignorar pastas proibidas
            dirs[:] = [d for d in dirs if d.lower() not in PASTAS_PROIBIDAS]

            for nome_arquivo in files:
                if nome_arquivo.lower().endswith((".txt", ".py")):
                    caminho_completo = os.path.join(root, nome_arquivo)
                    categoria_definida = "Ideias_Soltas_Submundo"

                    try:
                        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                            linhas = [next(f) for _ in range(20)]
                            conteudo_inicial = "".join(linhas).lower()

                        for categoria, palavras in CATEGORIAS.items():
                            if any(palavra in conteudo_inicial for palavra in palavras):
                                categoria_definida = categoria
                                break

                        caminho_categoria = os.path.join(DIRETORIO_DESTINO, categoria_definida)
                        if not os.path.exists(caminho_categoria):
                            os.makedirs(caminho_categoria)

                        caminho_destino_final = os.path.join(caminho_categoria, nome_arquivo)

                        if os.path.exists(caminho_destino_final):
                            novo_nome, caminho_destino_final = resolver_conflito(caminho_categoria, nome_arquivo)
                            print(f"[!] Mutação de Conflito: {nome_arquivo} -> {novo_nome}")

                        shutil.move(caminho_completo, caminho_destino_final)
                        print(f"[✓] Capturado: {nome_arquivo} -> {categoria_definida}")
                        arquivos_extraidos += 1

                    except StopIteration:
                        pass 
                    except Exception as e:
                        # Modo silencioso para erros de sistema, para não poluir a tela
                        pass

    print(f"\n[APOGEU ALCANÇADO] {arquivos_extraidos} arquivos arrancados da origem e blindados no Cofre.")

if __name__ == "__main__":
    print("Ativando varredura tática GLOBAL nos discos C:\\ e D:\\ ...")
    executar_extracao()