import os

# Nome do arquivo final onde tudo será unificado
arquivo_final = "consolidado_geral.txt"

def fundir_arquivos():
    print("[+] Iniciando a fusão tática dos arquivos...")
    
    total_fundidos = 0
    
    # Abre o arquivo mestre para escrita
    with open(arquivo_final, 'w', encoding='utf-8', errors='ignore') as outfile:
        for arquivo in os.listdir("."):
            # Filtra apenas .txt e ignora o próprio arquivo de saída
            if arquivo.endswith(".txt") and arquivo != arquivo_final:
                print(f"[>] Fundindo: {arquivo}")
                try:
                    with open(arquivo, 'r', encoding='utf-8', errors='ignore') as infile:
                        # Escreve o conteúdo no arquivo mestre
                        outfile.write(infile.read())
                        
                        # Adiciona uma quebra de linha para não grudar os dados
                        outfile.write("\n")
                        total_fundidos += 1
                except Exception as e:
                    print(f"[!] Falha ao processar {arquivo}: {e}")
                    
    print(f"[+] Operação finalizada. {total_fundidos} arquivos unificados em '{arquivo_final}'.")

if __name__ == "__main__":
    fundir_arquivos()