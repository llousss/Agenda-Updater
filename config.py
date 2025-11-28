import os

DOCS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "AgendaUpdater")
os.makedirs(DOCS_DIR, exist_ok=True)

ANGRY_PATH = r"C:\Program Files\Angry IP Scanner\ipscan.exe"

SAIDA_CSV = os.path.join(DOCS_DIR, "resultado.csv")

USUARIO = "admin"
SENHA = "admin"

IP_RANGE_START = "192.168.2.1"
IP_RANGE_END = "192.168.2.254"
