import os

# Nome do arquivo final onde tudo será unificado
arquivo_final = "consolidado_geral.txt"

def fundir_arquivos():
    print("[+] Iniciando a fusão tática dos arquivos...")
    
    total_fundidos = 0
    linhas_vistas = set() # Conjunto para rastrear linhas únicas
    
    # Abre o arquivo mestre para escrita
    with open(arquivo_final, 'w', encoding='utf-8', errors='ignore') as outfile:
        for arquivo in os.listdir("."):
            # Filtra apenas .txt e ignora o próprio arquivo de saída
            if arquivo.endswith(".txt") and arquivo != arquivo_final:
                print(f"[>] Fundindo: {arquivo}")
                try:
                    with open(arquivo, 'r', encoding='utf-8', errors='ignore') as infile:
                        for linha in infile:
                            # Remove a quebra de linha do final para comparar de forma justa
                            linha_limpa = linha.rstrip('\n')
                            
                            # Se a linha não foi vista ainda, grava no arquivo e salva no set
                            if linha_limpa not in linhas_vistas:
                                outfile.write(linha_limpa + '\n')
                                linhas_vistas.add(linha_limpa)
                                
                        total_fundidos += 1
                except Exception as e:
                    print(f"[!] Falha ao processar {arquivo}: {e}")
                    
    print(f"[+] Operação finalizada. {total_fundidos} arquivos unificados sem duplicatas em '{arquivo_final}'.")

if __name__ == "__main__":
    fundir_arquivos()