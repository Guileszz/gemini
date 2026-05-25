import requests

def testar_proxy_elite(proxy_ip):
    # Endpoint que devolve os headers recebidos
    url = "http://httpbin.org/get"
    proxies = {"http": proxy_ip, "https": proxy_ip}
    
    try:
        response = requests.get(url, proxies=proxies, timeout=5).json()
        headers = response.get('headers', {})
        
        # O CRITÉRIO ELITE:
        # Não pode ter rastro do seu IP real nem marca de Proxy
        if "Via" not in headers and "X-Forwarded-For" not in headers:
            print(f"[+] ATIVO ELITE IDENTIFICADO: {proxy_ip}")
            return True
    except:
        return False

# Exemplo de uso na sua lista de minerada
# proxy = "187.xx.xx.xx:8080"