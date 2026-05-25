import os
import shutil
import zipfile
import string
from ctypes import windll

# DEPENDÊNCIA TÁTICA: pip install rarfile
try:
    import rarfile
    # Caso precise do caminho do unrar no Windows, descomente e ajuste a linha abaixo:
    # rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
    RAR_HABILITADO = True
except ImportError:
    RAR_HABILITADO = False
    print("[-] AVISO: 'rarfile' não detectado. Instalando, rastrearemos RARs também.")

def mapear_drives():
    """Detecta todos os HDDs/SSDs plugados na máquina do Império."""
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letra in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letra + ':\\')
        bitmask >>= 1
    return drives

def minerar_ativos():
    # Ponto de extração
    cofre_desktop = os.path.join(os.path.expanduser("~"), "Desktop", "SVB_APOGEU")
    if not os.path.exists(cofre_desktop):
        os.makedirs(cofre_desktop)
        print(f"[+] COFRE CRIADO: {cofre_desktop}")

    drives = mapear_drives()
    
    print("[!] INICIANDO VARREDURA GLOBAL. LATÊNCIA NEGATIVA EM EXECUÇÃO...")

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            # Ignorar pastas mortas/sistema para manter o Flow e não perder processamento
            if any(skip in root for skip in ['Windows', '$Recycle.Bin', 'ProgramData', cofre_desktop]):
                continue
                
            for file in files:
                caminho_completo = os.path.join(root, file)
                mover = False
                
                try:
                    # 1. Alvo Direto
                    if file.lower().endswith('.svb'):
                        mover = True
                    
                    # 2. Infiltração em ZIP
                    elif file.lower().endswith('.zip'):
                        with zipfile.ZipFile(caminho_completo, 'r') as z:
                            if any(f.lower().endswith('.svb') for f in z.namelist()):
                                mover = True
                                
                    # 3. Infiltração em RAR
                    elif RAR_HABILITADO and file.lower().endswith('.rar'):
                        with rarfile.RarFile(caminho_completo, 'r') as r:
                            if any(f.lower().endswith('.svb') for f in r.namelist()):
                                mover = True
                                
                    # Execução do Carrasco (Mover)
                    if mover:
                        destino = os.path.join(cofre_desktop, file)
                        # Se já existir um arquivo com o mesmo nome, ele sobrescreve para manter só o mais letal
                        shutil.move(caminho_completo, destino)
                        print(f"[+] ATIVO RESGATADO: {file}")
                        
                except Exception:
                    # Silence is gold. Zero logs de erro de permissão para não sujar a tela.
                    pass 

if __name__ == '__main__':
    minerar_ativos()
    print("\n[$$$] OPERAÇÃO CONCLUÍDA. ATIVOS CENTRALIZADOS NO DESKTOP.")