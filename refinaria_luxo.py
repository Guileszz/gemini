import ijson
import re

# Regex tática para capturar apenas e-mails válidos
regex_email = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'

def refinaria_mutante(input_json, output_txt):
    print(f"[*] Iniciando Refinaria no arquivo: {input_json}")
    
    with open(input_json, 'rb') as f:
        # Usamos o prefixo 'item' - ajuste se o JSON tiver outra estrutura
        objetos = ijson.items(f, 'item')
        
        with open(output_txt, 'w', encoding='utf-8') as out:
            vistos = set() # Cache para evitar duplicatas na mesma sessão
            contador = 0
            
            for obj in objetos:
                email = obj.get('EMAIL', '').lower().strip()
                
                # Só processa se o e-mail passar na Regex e não for repetido
                if re.match(regex_email, email) and email not in vistos:
                    out.write(f"{email}\n")
                    vistos.add(email)
                    contador += 1
                    
                    # Limpa o cache de vistos a cada 100k para não estourar a RAM
                    if len(vistos) > 100000:
                        vistos.clear()
                
                if contador % 50000 == 0 and contador > 0:
                    print(f"[+] {contador} ativos de luxo refinados...")

    print(f"[!] Extração Finalizada. Total: {contador} leads únicos.")

# Disparo
refinaria_mutante('bvd_contactinfo_email.json', 'leads_validados.txt')