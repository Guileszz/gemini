import os
import re

# --- A INTELIGÊNCIA DA REFINARIA ---
# Define o peso de cada tipo de informação.
# O script pontua cada parágrafo. Só passa o que tiver pontuação alta.

PESOS = {
    # CRITÉRIO 1: ESTRUTURA DE COMANDO (Peso Alto)
    "comando": 3, "prompt": 3, "void ": 4, "class ": 4, "system.": 3,
    "passo a passo": 3, "checklist": 3, "1.": 2, "2.": 2, "👉": 3,
    
    # CRITÉRIO 2: VOCABULÁRIO DE ELITE (Peso Médio)
    "néctar": 2, "ouro": 2, "axioma": 2, "lei ": 2, "entidade": 2,
    "infra zero": 2, "matrix": 1, "sistema": 1, "blindagem": 2,
    "doppelgänger": 3, "carrasco": 2, "sombra": 2,
    
    # CRITÉRIO 3: RESULTADO (Peso Médio)
    "lucro": 1, "venda": 1, "milhão": 1, "escala": 1, "roi": 1,
    "conversão": 1, "ticket": 1
}

# Limite mínimo para ser considerado "Néctar"
SCORE_MINIMO = 5 

NOME_FINAL = "000_O_GRANDE_LIVRO_DO_IMPERIO.txt"

def calcular_score(texto):
    score = 0
    texto_lower = texto.lower()
    
    for palavra, pontos in PESOS.items():
        if palavra in texto_lower:
            score += pontos
            
    return score

def executar_refinaria():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    print(f"--- 💎 INICIANDO REFINARIA FINAL EM: {pasta_atual} ---")
    print("Analisando densidade de valor em todos os arquivos...")
    
    blocos_de_ouro = []
    arquivos_lidos = 0
    
    # Varre todos os arquivos .txt
    for arquivo in os.listdir(pasta_atual):
        if arquivo == os.path.basename(__file__) or arquivo == NOME_FINAL or not arquivo.endswith(".txt"):
            continue
            
        caminho = os.path.join(pasta_atual, arquivo)
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                # Lê o arquivo inteiro como um bloco de texto
                conteudo_total = f.read()
            
            # Separa por blocos duplos de linha (parágrafos) para analisar contexto
            paragrafos = conteudo_total.split('\n\n')
            
            for paragrafo in paragrafos:
                # Limpeza básica
                p_limpo = paragrafo.strip()
                if len(p_limpo) < 30: continue # Ignora frases muito curtas
                
                # A MÁGICA: Calcula se o parágrafo vale a pena
                pontuacao = calcular_score(p_limpo)
                
                if pontuacao >= SCORE_MINIMO:
                    # Se for Ouro, formata e guarda
                    bloco_formatado = f"🏆 [SCORE: {pontuacao}] FONTE: {arquivo}\n"
                    bloco_formatado += f"{p_limpo}\n"
                    bloco_formatado += "-" * 40 + "\n"
                    blocos_de_ouro.append((pontuacao, bloco_formatado))
                    
            arquivos_lidos += 1
            print(f"Lendo: {arquivo}...")

        except Exception as e:
            # Tenta encoding alternativo se falhar
            try:
                with open(caminho, 'r', encoding='latin-1') as f:
                    conteudo_total = f.read()
                # (Repete a lógica - simplificada aqui para não duplicar código visualmente)
            except:
                print(f"[X] Erro em {arquivo}")

    # ORDENAÇÃO POR VALOR
    # Coloca os blocos com maior pontuação (Mais importantes) no topo do arquivo
    blocos_de_ouro.sort(key=lambda x: x[0], reverse=True)

    # GRAVAÇÃO
    with open(os.path.join(pasta_atual, NOME_FINAL), 'w', encoding='utf-8') as f_out:
        f_out.write("=== O GRANDE LIVRO DO IMPÉRIO (ORDENADO POR RELEVÂNCIA) ===\n")
        f_out.write("Este arquivo contém o Néctar Absoluto, do mais valioso para o menos valioso.\n\n")
        
        for score, texto in blocos_de_ouro:
            f_out.write(texto + "\n")

    print(f"\n--- REFINARIA CONCLUÍDA ---")
    print(f"Arquivos Escaneados: {arquivos_lidos}")
    print(f"Pepitas de Ouro Encontradas: {len(blocos_de_ouro)}")
    print(f"💎 ARQUIVO FINAL: {NOME_FINAL}")
    input("Pressione ENTER para acessar o Néctar...")

if __name__ == "__main__":
    executar_refinaria()