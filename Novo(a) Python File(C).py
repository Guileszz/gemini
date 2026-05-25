import os

# --- CONFIGURAÇÃO DO ORÁCULO (GPS FIXO) ---
# Agora ele força o sistema a olhar apenas para a pasta onde o script está.

CATEGORIAS = {
    "💰 MÁQUINA DE VENDAS (Money & Copy)": [
        "venda", "lucro", "dinheiro", "copy", "copywriting", "ticket", 
        "preço", "oferta", "cupom", "funil", "negócio", "freelance", "upwork"
    ],
    "🛠️ ARSENAL TÉCNICO (Tools & Hacks)": [
        "infra zero", "oracle", "cloudflare", "python", "script", "ferramenta",
        "automação", "ia ", "bot", "hack", "burlar", "onehack", "software"
    ],
    "🧠 ESTRATÉGIA DE COMANDO (Mindset & Planos)": [
        "estratégia", "plano", "visão", "entidade", "império", "barão", 
        "protocolo", "lei ", "axioma", "doppelgänger", "predador", "fase 2"
    ]
}

NOME_RELATORIO = "DOSSIÊ_FINAL_ELITE.txt"

def limpar_texto(texto):
    return texto.replace("**", "").replace("##", "").replace("###", "").strip()

def executar_oraculo():
    # --- CORREÇÃO DE ROTA (O PULO DO GATO) ---
    # Pega o caminho exato da pasta onde este arquivo .py está salvo
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_relatorio = os.path.join(pasta_atual, NOME_RELATORIO)
    
    print(f"--- 👁️ ORÁCULO ATIVO EM: {pasta_atual} ---")
    print(f"--- 💾 SALVANDO EM: {caminho_relatorio} ---")
    
    dados_extraidos = {key: [] for key in CATEGORIAS.keys()}
    dados_extraidos["📁 OUTROS INSIGHTS"] = []
    
    arquivos_lidos = 0
    
    # Lista arquivos da pasta correta
    for arquivo in os.listdir(pasta_atual):
        # Ignora o script e o relatório final
        if arquivo == os.path.basename(__file__) or arquivo == NOME_RELATORIO or not arquivo.endswith(".txt"):
            continue
            
        caminho_arquivo_leitura = os.path.join(pasta_atual, arquivo)
            
        try:
            linhas = []
            try:
                with open(caminho_arquivo_leitura, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
            except:
                with open(caminho_arquivo_leitura, 'r', encoding='latin-1') as f:
                    linhas = f.readlines()

            arquivos_lidos += 1
            print(f"Lendo: {arquivo}...")

            i = 0
            while i < len(linhas):
                linha_atual = linhas[i].lower()
                linha_original = linhas[i]
                capturado = False
                
                for categoria, keywords in CATEGORIAS.items():
                    for word in keywords:
                        if word in linha_atual:
                            bloco = [f"[FONTE: {arquivo}]"]
                            bloco.append(f"👉 {limpar_texto(linha_original)}")
                            
                            if i + 1 < len(linhas) and len(linhas[i+1].strip()) > 3:
                                bloco.append(f"   ↳ {limpar_texto(linhas[i+1])}")
                            if i + 2 < len(linhas) and len(linhas[i+2].strip()) > 3:
                                bloco.append(f"   ↳ {limpar_texto(linhas[i+2])}")
                            
                            bloco.append("-" * 30 + "\n")
                            dados_extraidos[categoria].append("\n".join(bloco))
                            capturado = True
                            break 
                    if capturado: break
                
                i += 1 

        except Exception as e:
            print(f"[ERRO] {arquivo}: {e}")

    # --- SALVAMENTO FORÇADO ---
    try:
        with open(caminho_relatorio, 'w', encoding='utf-8') as f_out:
            f_out.write("=== 🦅 DOSSIÊ DE INTELIGÊNCIA: IMPÉRIO MUTANTE ===\n\n")
            for categoria, conteudos in dados_extraidos.items():
                if conteudos:
                    f_out.write(f"\n{'='*10} {categoria} {'='*10}\n\n")
                    for item in conteudos:
                        f_out.write(item)
        print(f"\n✅ SUCESSO! ARQUIVO SALVO EM: {caminho_relatorio}")
    except Exception as e:
        print(f"\n❌ ERRO AO SALVAR O ARQUIVO FINAL: {e}")

    input("Pressione ENTER para fechar...")

if __name__ == "__main__":
    executar_oraculo()