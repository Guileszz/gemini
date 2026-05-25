import re

def extrair_emails_senhas(arquivo_entrada, arquivo_saida):
    # Expressão regular para capturar email seguido de senha
    # Email: padrão básico válido (pode ser ajustado conforme necessidade)
    # Senha: qualquer sequência até espaço, nova linha ou caractere proibido (ajustável)
    padrao = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([^\s/:]+)'

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Encontrar todos os pares email:senha
        resultados = re.findall(padrao, conteudo)

        # Remover duplicados mantendo ordem
        vistos = set()
        pares_unicos = []
        for email, senha in resultados:
            par = f"{email}:{senha}"
            if par not in vistos:
                vistos.add(par)
                pares_unicos.append(par)

        # Salvar resultado no arquivo de saída
        with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
            for par in pares_unicos:
                f_out.write(par + '\n')

        print(f"Extração concluída! {len(pares_unicos)} pares extraídos e salvos em '{arquivo_saida}'.")

    except FileNotFoundError:
        print(f"Erro: arquivo '{arquivo_entrada}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    entrada = input("Digite o nome do arquivo de entrada (ex: dados.txt): ")
    saida = input("Digite o nome do arquivo de saída (ex: saida.txt): ")
    extrair_emails_senhas(entrada, saida)
