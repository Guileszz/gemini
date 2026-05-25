import os

def eliminar_duplicatas():
    print("/// INICIANDO PROTOCOLO CARRASCO ///")
    print("-" * 40)

    # 1. Input: Onde está o arquivo sujo?
    arquivo_entrada = input("1. Digite o nome do arquivo com DUPLICATAS (ex: contas.txt): ").strip()
    
    if not os.path.exists(arquivo_entrada):
        print(f"\n[ERRO] Arquivo '{arquivo_entrada}' inexistente. Verifique o nome.")
        return

    # 2. Output: Onde salvar o néctar puro?
    arquivo_saida = input("2. Nome do arquivo ÚNICO (ex: contas_unicas.txt): ").strip()

    print("\n[PROCESSANDO] Auditando linhas...")

    # Estrutura de memória (Set = Tabela Hash = Velocidade Máxima)
    linhas_vistas = set()
    linhas_totais = 0
    linhas_unicas = 0

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8', errors='ignore') as f_in, \
             open(arquivo_saida, 'w', encoding='utf-8') as f_out:
            
            for linha in f_in:
                linha_limpa = linha.strip() # Remove espaços extras nas pontas
                
                # Se a linha não estiver vazia
                if linha_limpa:
                    linhas_totais += 1
                    
                    # O HASH CHECK: Se não vi essa linha antes, escrevo.
                    if linha_limpa not in linhas_vistas:
                        f_out.write(linha_limpa + '\n')
                        linhas_vistas.add(linha_limpa) # Adiciona à memória
                        linhas_unicas += 1

        duplicatas_removidas = linhas_totais - linhas_unicas
        
        print("-" * 40)
        print("/// RELATÓRIO DE AUDITORIA ///")
        print(f"Total analisado: {linhas_totais}")
        print(f"✅ Únicos mantidos: {linhas_unicas}")
        print(f"✂️ Duplicatas cortadas: {duplicatas_removidas}")
        print(f"Arquivo gerado: '{arquivo_saida}'")
        print("-" * 40)

    except Exception as e:
        print(f"\n[FALHA CRÍTICA] Erro durante a purificação: {e}")

if __name__ == "__main__":
    eliminar_duplicatas()