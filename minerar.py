import os

def minerar_dados(diretorio_alvo, termo_busca, arquivo_saida):
    print(f"[*] INICIANDO BUSCA: '{termo_busca}' em '{diretorio_alvo}'")
    
    encontrados = 0
    # Abre o arquivo de saída uma única vez para escrita
    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        # Varre diretório e subdiretórios (Recursividade Total)
        for raiz, _, arquivos in os.walk(diretorio_alvo):
            for nome_arquivo in arquivos:
                if nome_arquivo.endswith('.txt'):
                    caminho_completo = os.path.join(raiz, nome_arquivo)
                    
                    # Proteção para não ler o próprio arquivo de saída
                    if nome_arquivo == arquivo_saida:
                        continue

                    try:
                        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as infile:
                            for linha in infile:
                                if termo_busca.lower() in linha.lower():
                                    outfile.write(linha)
                                    encontrados += 1
                    except Exception as e:
                        print(f"[!] Erro ao ler {nome_arquivo}: {e}")

    print("-" * 30)
    print(f"[+] OPERAÇÃO FINALIZADA.")
    print(f"[+] Linhas extraídas: {encontrados}")
    print(f"[+] Destino: {arquivo_saida}")

# --- CONFIGURAÇÃO DE EXECUÇÃO ---
# Se o script estiver na pasta dos arquivos, use '.'
# Caso contrário, coloque o caminho completo: 'C:/Sua/Pasta'
PASTA = './' 
ALVO = 'habbo.com.br' 
SAIDA = 'extracao_habbo_resultados.txt'

minerar_dados(PASTA, ALVO, SAIDA)
input("\n[Pressione ENTER para fechar]")