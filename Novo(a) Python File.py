import os

# --- CONFIGURAÇÃO DA ALQUIMIA (EXTRAÇÃO DE NÉCTAR) ---
# Define quais arquivos ler e o que procurar dentro deles.

ARQUIVOS_ALVO = [
    "01_BÍBLIA_DO_IMPÉRIO.txt",
    "02_ARSENAL_DE_GUERRA.txt",
    "03_STUDIO_VOZ_DE_CRIA.txt",
    "04_SYSTEM_KERNEL_CODE.txt"
]

# O script caça linhas que tenham esses gatilhos
GATILHOS_DE_VALOR = [
    # ALTA HIERARQUIA
    "axioma", "lei ", "regra", "mandamento", "princípio", "definição",
    
    # AÇÃO PURA
    "passo a passo", "checklist", "como fazer", "tática", "estratégia", 
    "executar", "ação", "comando", "prompt",
    
    # CÓDIGO E TECH
    "void ", "class ", "import ", "def ", "system.", "code",
    
    # VALOR
    "néctar", "ouro", "segredo", "pulo do gato", "importante", "atenção", "nota:"
]

NOME_FINAL = "00_MANUAL_DE_ELITE_RESUMIDO.txt"

def executar_alquimia():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    print(f"--- ⚗️ INICIANDO PROTOCOLO ALQUIMIA EM: {pasta_atual} ---")
    
    conteudo_resumido = []
    
    # Cabeçalho do Resumo
    conteudo_resumido.append("=== MANUAL DE ELITE: O RESUMO OPERACIONAL ===\n")
    conteudo_resumido.append("[SOMENTE O ESSENCIAL - LEITURA RÁPIDA]\n\n")

    arquivos_processados = 0

    for arquivo in ARQUIVOS_ALVO:
        caminho = os.path.join(pasta_atual, arquivo)
        
        # Verifica se o arquivo existe antes de tentar ler
        if not os.path.exists(caminho):
            print(f"[!] Arquivo não encontrado: {arquivo} (Pulando...)")
            continue
            
        print(f"Destilando: {arquivo}...")
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            # Adiciona Título da Seção
            conteudo_resumido.append(f"\n{'='*30}\n🔎 FONTE: {arquivo}\n{'='*30}\n")
            
            i = 0
            while i < len(linhas):
                linha_lower = linhas[i].lower().strip()
                
                # Se a linha for vazia, pula
                if not linha_lower:
                    i += 1
                    continue

                capturar = False
                for gatilho in GATILHOS_DE_VALOR:
                    if gatilho in linha_lower:
                        capturar = True
                        break
                
                if capturar:
                    # TÁTICA DE CONTEXTO:
                    # Se achou algo importante, pega a linha atual e as próximas 3 linhas
                    # para não pegar a frase solta sem explicação.
                    
                    bloco = []
                    bloco.append(f"👉 {linhas[i].strip()}") # Linha principal
                    
                    # Pega até 3 linhas seguintes de contexto (se existirem)
                    for k in range(1, 4):
                        if i + k < len(linhas):
                            prox_linha = linhas[i+k].strip()
                            if prox_linha: # Só adiciona se tiver texto
                                bloco.append(f"   ↳ {prox_linha}")
                    
                    conteudo_resumido.append("\n".join(bloco))
                    conteudo_resumido.append("\n" + "-"*20 + "\n")
                    
                    # Pula as linhas que já capturamos para não duplicar
                    i += 3 
                
                i += 1
            
            arquivos_processados += 1

        except Exception as e:
            print(f"[ERRO] Falha ao processar {arquivo}: {e}")

    # Gravação Final
    caminho_final = os.path.join(pasta_atual, NOME_FINAL)
    with open(caminho_final, 'w', encoding='utf-8') as f_out:
        f_out.writelines(conteudo_resumido)

    print(f"\n--- ALQUIMIA COMPLETA. {arquivos_processados} FONTES DESTILADAS. ---")
    print(f"💎 ARQUIVO FINAL: {NOME_FINAL}")
    input("Pressione ENTER para abrir o Manual de Elite...")

if __name__ == "__main__":
    executar_alquimia()