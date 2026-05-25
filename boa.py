import os
import hashlib

# --- CONFIGURAÇÃO DO UNIFICADOR ---
# O script vai caçar TODOS os arquivos de texto nas subpastas,
# eliminar repetições e criar o Documento Final.

NOME_DO_IMPERIO = "01_CODEX_SUPREMO_FINAL.txt"

def calcular_hash(texto):
    # Cria uma impressão digital única para o texto (para detectar cópias)
    return hashlib.md5(texto.strip().lower().encode('utf-8')).hexdigest()

def executar_unificacao():
    raiz = os.path.dirname(os.path.abspath(__file__))
    print(f"--- 🌐 INICIANDO PROTOCOLO UNIFICADOR EM: {raiz} ---")
    
    conteudo_final = []
    hashes_vistos = set() # O Banco de Dados de Repetições
    arquivos_processados = 0
    duplicatas_eliminadas = 0
    
    # Cabeçalho do Mestre
    conteudo_final.append("=== CODEX SUPREMO: A SOMA DE TODO O CONHECIMENTO ===\n")
    conteudo_final.append("Este arquivo unifica todas as pastas, sem redundância.\n")
    conteudo_final.append("====================================================\n\n")

    # O CRAWLER (A Aranha que anda pelas pastas)
    for pasta_atual, subpastas, arquivos in os.walk(raiz):
        
        # Ignora a pasta .git ou pastas ocultas se tiver
        if ".git" in pasta_atual: continue
        
        for arquivo in arquivos:
            # Ignora o próprio script e o arquivo final para não entrar em loop
            if arquivo == os.path.basename(__file__) or arquivo == NOME_DO_IMPERIO or not arquivo.endswith(".txt"):
                continue
            
            caminho_completo = os.path.join(pasta_atual, arquivo)
            nome_pasta_origem = os.path.basename(pasta_atual)
            
            try:
                # Leitura
                texto_arquivo = ""
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as f:
                        texto_arquivo = f.read()
                except:
                    with open(caminho_completo, 'r', encoding='latin-1') as f:
                        texto_arquivo = f.read()
                
                # Separa por blocos (Parágrafos ou Seções)
                # Assumindo que seus arquivos usam linhas vazias ou traços para separar ideias
                blocos = texto_arquivo.split('\n\n')
                
                novos_blocos_deste_arquivo = []
                
                for bloco in blocos:
                    bloco_limpo = bloco.strip()
                    if len(bloco_limpo) < 20: continue # Ignora frases soltas muito curtas
                    
                    # Verifica se já vimos esse texto antes
                    assinatura = calcular_hash(bloco_limpo)
                    
                    if assinatura not in hashes_vistos:
                        hashes_vistos.add(assinatura)
                        # Adiciona identificação de onde veio (só na primeira vez)
                        novos_blocos_deste_arquivo.append(bloco_limpo)
                    else:
                        duplicatas_eliminadas += 1
                
                # Se sobrou algo novo nesse arquivo, adiciona ao Mestre
                if novos_blocos_deste_arquivo:
                    conteudo_final.append(f"\n⚡ FONTE: [{nome_pasta_origem}] / {arquivo}")
                    conteudo_final.append("-" * 40)
                    conteudo_final.append("\n\n".join(novos_blocos_deste_arquivo))
                    conteudo_final.append("\n" + "="*40 + "\n")
                    
                    arquivos_processados += 1
                    print(f"[+] Processado: {arquivo} (Pasta: {nome_pasta_origem})")
                else:
                    print(f"[.] {arquivo} ignorado (100% duplicado)")
                    
            except Exception as e:
                print(f"[X] Erro ao ler {arquivo}: {e}")

    # Gravação Final
    caminho_final = os.path.join(raiz, NOME_DO_IMPERIO)
    with open(caminho_final, 'w', encoding='utf-8') as f_out:
        f_out.writelines(conteudo_final)

    print(f"\n--- MISSÃO DE UNIFICAÇÃO CUMPRIDA ---")
    print(f"Pastas Varridas: Várias")
    print(f"Arquivos Processados: {arquivos_processados}")
    print(f"Ecos Eliminados (Duplicatas): {duplicatas_eliminadas}")
    print(f"👑 ARQUIVO SUPREMO: {NOME_DO_IMPERIO}")
    input("Pressione ENTER para acessar o Codex Supremo...")

if __name__ == "__main__":
    executar_unificacao()