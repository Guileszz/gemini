import re

def minerar_imperio(input_file, output_file):
    # Palavras-chave de alto valor (Néctar e Músculo)
    keywords = [
        "NÉCTAR", "COPY DE GUERRA", "EQUITY", "CHECKLIST", "QAP",
        "MINERAR", "SECO", "SEM PALESTRINHA", "PRODUTO", "PREÇO",
        "SCRIPT", "MÓDULO", "TÁTICA"
    ]
    
    # Marcadores de descarte (Gordura)
    trash_words = ["DESCARTAR", "DESCARTE", "LIXO", "PALESTRINHA"]

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separar por blocos de conversa/fonte baseados no padrão do seu arquivo
    blocks = re.split(r'----------------------------------------', content)
    
    pepitas = []

    for block in blocks:
        # Lógica de Filtragem:
        # 1. Se tiver palavra de descarte, ignora.
        # 2. Se tiver palavra-chave de valor, mantém.
        if any(trash in block.upper() for trash in trash_words):
            continue
            
        if any(key in block.upper() for key in keywords):
            pepitas.append(block.strip())

    # Salva o Néctar em um novo arquivo pronto para ordens diretas
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n=== NÉCTAR EXTRAÍDO PARA OPERAÇÃO ===\n\n")
        f.write("\n\n----------------------------------------\n\n".join(pepitas))

    print(f"📡 Mineração concluída. {len(pepitas)} blocos de valor isolados em: {output_file}")

# Execução
minerar_imperio('PEPITAS_DO_IMPERIO_FINAL.txt', 'ORDENS_DIRETAS.txt')