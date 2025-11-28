import subprocess
import time
import os
import csv
from config import ANGRY_PATH, SAIDA_CSV, IP_RANGE_START, IP_RANGE_END

def escanear_ips():
    """Executa o Angry IP Scanner e retorna uma lista de IPs com portas 80.443"""
    if os.path.exists(SAIDA_CSV):
        os.remove(SAIDA_CSV)

    proc = subprocess.Popen([
        ANGRY_PATH,
        "-f:range", IP_RANGE_START, IP_RANGE_END,
        "-o", SAIDA_CSV,
        "-s", "-q"
    ])
    print("🔍 Escaneando IPs na rede... aguarde o término do Angry IP Scanner.")
    proc.wait()
    print("✔ Escaneamento concluído.")

    # Aguarda CSV ser gerado
    timeout = 60
    while timeout > 0 and not os.path.exists(SAIDA_CSV):
        time.sleep(1)
        timeout -= 1

    if not os.path.exists(SAIDA_CSV):
        raise FileNotFoundError("❌ Erro: o arquivo CSV não foi gerado.")

    # Lê IPs válidos
    valid_ips = []
    with open(SAIDA_CSV, 'r', newline='', encoding='cp1252') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            portas = row.get("Portas", "").strip()
            if portas == "80.443":
                valid_ips.append(row["IP"])


    return valid_ips
