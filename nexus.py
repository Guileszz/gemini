import os
import shutil

# --- CONFIGURAÇÃO DO NEXUS V2 (INTELIGÊNCIA DE OURO) ---
# Adicionei os novos vetores de busca para refinar o garimpo.

DIRETRIZES = {
    # --- NOVAS CATEGORIAS DE ELITE (PRIORIDADE) ---
    "99_NECTAR_SUPREMO": [
        "néctar", "copy de guerra", "equity", "checklist", "qap", 
        "pote de ouro", "suprassumo", "resultado final", "pronto para venda",
        "lucro máximo", "caminho dourado"
    ],
    "05_CARRASCO_FILTRO": [
        "descartar", "descarte", "minerar", "seco", "sem palestrinha", 
        "sem enrolação", "cortar gordura", "direto ao ponto", "auditoria",
        "lixo", "jogar fora", "resumo brutal"
    ],

    # --- CATEGORIAS ESTRUTURAIS (ANTIGAS) ---
    "01_CEREBRO_ESTRATEGIA": [
        "estratégia", "visão", "mentalidade", "mindset", "plano de negócio", 
        "nível 21", "nível 23", "nível 24", "axioma", "fundação do sul"
    ],
    "02_CACADOR_VENDAS": [
        "vendas", "lucro", "dinheiro", "copywriting", "oferta", "funil",
        "ganha grana", "renda extra", "ticket", "comissão", "kiwify"
    ],
    "10_NEXUS_TECNOLOGIA": [
        "python", "script", "código", "automação", "bot", "selenium", "api",
        "terminal", "cmd", "instalar", "pip install"
    ],
    "11_SOMBRA_UNDERGROUND": [
        "hack", "crack", "pirata", "black hat", "onehack", "vazado", "espião",
        "engenharia reversa", "burlar", "anônimo", "proxy", "vpn"
    ],
    "12_TOTAL_SISTEMA": [
        "entidade", "codex", "singularidade", "trindade", "protocolo", "comando",
        "prompt", "persona", "arquiteto", "general", "voz de cria"
    ],
    "PRODUTOS_DO_IMPERIO": [
        "infra zero", "arsenal visual", "drop 2026", "algoritmo i.a", "gestor de império",
        "ebook", "curso", "módulo", "bônus"
    ]
}

PASTA_PADRAO = "00_ARQUIVO_GERAL"

def executar_protocolo_nexus_v2():
    origem = os.getcwd()
    print(f"--- 🦅 INICIANDO NEXUS V2 (MODO GARIMPEIRO) EM: {origem} ---")
    
    arquivos_processados = 0
    
    for arquivo in os.listdir(origem):
        # Ignora o próprio script
        if arquivo == os.path.basename(__file__) or not arquivo.endswith(".txt"):
            continue
            
        caminho_arquivo = os.path.join(origem, arquivo)
        
        try:
            # Leitura Blindada (UTF-8 ou Latin-1)
            conteudo = ""
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read().lower()
            except UnicodeDecodeError:
                with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                    conteudo = f.read().lower()

            destino_final = PASTA_PADRAO
            pontuacao_maxima = 0
            
            # --- ALGORITMO DE PONTUAÇÃO ---
            # Ele conta qual categoria tem mais palavras presentes no texto.
            for pasta, keywords in DIRETRIZES.items():
                pontos = 0
                for word in keywords:
                    if word in conteudo:
                        pontos += 1
                
                # Critério de Desempate: Se empatar, prefere as pastas novas (99 e 05)
                # Adicionamos um peso extra se for categoria especial
                if "99_" in pasta or "05_" in pasta:
                    pontos = pontos * 1.5 

                if pontos > pontuacao_maxima:
                    pontuacao_maxima = pontos
                    destino_final = pasta
            
            # Se a pontuação for muito baixa, joga na geral
            if pontuacao_maxima < 1:
                destino_final = PASTA_PADRAO

            # Infra: Cria a pasta
            caminho_destino = os.path.join(origem, destino_final)
            if not os.path.exists(caminho_destino):
                os.makedirs(caminho_destino)
            
            # Movimentação Tática
            shutil.move(caminho_arquivo, os.path.join(caminho_destino, arquivo))
            print(f"[✓] {arquivo} -> {destino_final} (Score: {pontuacao_maxima:.1f})")
            arquivos_processados += 1
            
        except Exception as e:
            print(f"[X] Falha na Matrix com {arquivo}: {e}")

    print(f"\n--- OPERAÇÃO FINALIZADA. {arquivos_processados} ARQUIVOS CLASSIFICADOS. ---")
    input("Pressione ENTER para encerrar...")

if __name__ == "__main__":
    executar_protocolo_nexus_v2()