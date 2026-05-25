import re

def mineracao_contextual(input_file, output_file):
    print("📡 INICIANDO PROTOCOLO DE MINERAÇÃO CONTEXTUAL...")
    
    # === 1. CONFIGURAÇÕES DE ALVO ===
    # Quantas linhas pegar APÓS encontrar a palavra-chave?
    LINES_TO_EXPAND = 12 
    
    # Palavras-chave que indicam valor (Adicione ou remova conforme necessário)
    keywords = [
        "NÉCTAR", "COPY", "FERRAMENTA", "SCRIPT", "PYTHON", 
        "INFRA", "ORACLE", "CLOUDFLARE", "VENDAS", "PREÇO", 
        "ESTRATÉGIA", "CHECKLIST", "PRODUTO", "HACK", "IA",
        "BLACK", "JURISDIÇÃO", "NOTION", "API", "CODEX"
    ]

    # === 2. LEITURA DO ARQUIVO BRUTO ===
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{input_file}' não encontrado.")
        return

    extracted_blocks = []
    current_source = "Fonte Desconhecida"
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # A. RASTREAMENTO DA FONTE
        # Tenta identificar linhas que indicam o nome do arquivo original
        # Ajuste o padrão regex abaixo se o formato da sua fonte for diferente
        if "[FONTE:" in line or "Novo Documento" in line:
            current_source = line.replace("----------------------------------------", "").strip()
        
        # B. DETECÇÃO DE VALOR
        # Verifica se alguma keyword está nesta linha
        is_relevant = any(key.lower() in line.lower() for key in keywords)
        
        # Se achou ouro, inicia a extração do bloco
        if is_relevant:
            block_content = []
            
            # Cabeçalho do Bloco
            block_content.append(f"\n📂 {current_source}") 
            block_content.append(f"⬇️ CONTEXTO ENCONTRADO (Gatilho: Linha {i})")
            
            # Captura a linha atual e as próximas X linhas
            for j in range(LINES_TO_EXPAND):
                if (i + j) < len(lines):
                    # Adiciona a linha ao bloco
                    block_content.append(f"   👉 {lines[i+j].rstrip()}")
            
            block_content.append("-" * 50) # Separador visual
            
            # Salva o bloco
            extracted_blocks.append("\n".join(block_content))
            
            # Avança o índice para não pegar a mesma conversa repetida
            # Se já pegamos 12 linhas, pulamos 12 linhas.
            i += LINES_TO_EXPAND
        else:
            # Se não achou nada, vai para a próxima linha
            i += 1

    # === 3. EXPORTAÇÃO DO NÉCTAR ===
    if extracted_blocks:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== RELATÓRIO DE MINERAÇÃO EXPANDIDA ===\n")
            f.write(f"Total de Blocos Extraídos: {len(extracted_blocks)}\n\n")
            f.write("\n".join(extracted_blocks))
        print(f"✅ SUCESSO. {len(extracted_blocks)} blocos extraídos para '{output_file}'.")
        print("⚡ Verifique o arquivo para dar as ordens.")
    else:
        print("⚠️ Nenhuma pepita encontrada com as palavras-chave atuais.")

# === EXECUÇÃO ===
# Substitua 'SEU_ARQUIVO_COMPLETO.txt' pelo nome do seu arquivo gigante com todos os chats
file_name = 'SEU_ARQUIVO_COMPLETO.txt' 
mineracao_contextual(file_name, 'DOSSIE_EXPANDIDO.txt')