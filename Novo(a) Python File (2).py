import os
import re

# --- CONFIGURAÇÃO DO PENTE FINO ---
# Focado em extrair ESTRUTURAS, PREÇOS e DEFINIÇÕES TÉCNICAS que podem ter escapado.

ALVOS_ESPECIFICOS = {
    "💎 PRODUTOS & PREÇOS (A Grana)": [
        "preço", "valor", "R$", "27,90", "497,00", "cupom", "ticket", 
        "escada de", "cobrança", "receita", "venda", "oferta"
    ],
    "🧬 ESTRATÉGIA AVANÇADA (O Conceito)": [
        "doppelgänger", "predador", "sequestro de intenção", "brand jacking",
        "media for equity", "exit", "milionário", "holding", "fase 2"
    ],
    "🛠️ FERRAMENTAS & INFRA (O Técnico)": [
        "infra zero", "arsenal visual", "gestor de império", "drop 2026",
        "semrush", "foreplay", "oracle", "cloudflare", "github", "student pack"
    ]
}

NOME_SAIDA = "PEPITAS_DO_IMPERIO_FINAL.txt"

def limpar(texto):
    return texto.replace("**", "").replace("###", "").strip()

def executar_pente_fino():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    print(f"--- 🕵️ INICIANDO PENTE FINO EM: {pasta_atual} ---")
    
    coleta = {k: [] for k in ALVOS_ESPECIFICOS.keys()}
    arquivos_alvo = ["Novo Documento de Texto (26).txt", "Novo Documento de Texto (27).txt", "DOSSIÊ_FINAL_ELITE.txt"]
    
    for arquivo in arquivos_alvo:
        caminho = os.path.join(pasta_atual, arquivo)
        if not os.path.exists(caminho): continue
        
        print(f"Escanerando: {arquivo}...")
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            i = 0
            while i < len(linhas):
                linha_lower = linhas[i].lower()
                
                capturou = False
                for categoria, keywords in ALVOS_ESPECIFICOS.items():
                    for key in keywords:
                        if key in linha_lower:
                            # TÁTICA DE CONTEXTO ESTENDIDO
                            # Pega a linha anterior (se for título) e as 3 próximas (detalhes)
                            bloco = []
                            bloco.append(f"📂 [FONTE: {arquivo}]")
                            
                            # Se tiver linha anterior com texto, pega (pode ser título)
                            if i > 0 and len(linhas[i-1].strip()) > 3:
                                bloco.append(f"   ⬆️ {limpar(linhas[i-1])}")
                            
                            bloco.append(f"   👉 {limpar(linhas[i])}") # A Pepita
                            
                            # Pega as próximas 3 linhas para garantir que pegamos a lista/preço
                            for offset in range(1, 4):
                                if i + offset < len(linhas):
                                    prox = limpar(linhas[i+offset])
                                    if prox: bloco.append(f"   ↳ {prox}")
                            
                            bloco.append("-" * 40)
                            
                            # Evita duplicatas exatas dentro da mesma categoria
                            bloco_str = "\n".join(bloco)
                            if not any(b in bloco_str for b in coleta[categoria]): # Checagem simples
                                coleta[categoria].append(bloco_str)
                            
                            capturou = True
                            break
                    if capturou: break
                
                # Se capturou, pula algumas linhas para não pegar o mesmo contexto repetido
                if capturou:
                    i += 3
                else:
                    i += 1
                    
        except Exception as e:
            print(f"[ERRO] {arquivo}: {e}")

    # --- RELATÓRIO FINAL ---
    with open(os.path.join(pasta_atual, NOME_SAIDA), 'w', encoding='utf-8') as f_out:
        f_out.write("=== AS ÚLTIMAS PEPITAS (MATEMÁTICA E TÁTICA FINA) ===\n\n")
        for cat, itens in coleta.items():
            if itens:
                f_out.write(f"\n{'='*10} {cat} {'='*10}\n")
                for item in itens:
                    f_out.write(item + "\n")
    
    print(f"\n✅ PENTE FINO CONCLUÍDO.")
    print(f"💎 Verifique o arquivo: {NOME_SAIDA}")
    input("Enter para fechar...")

if __name__ == "__main__":
    executar_pente_fino()