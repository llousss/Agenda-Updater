import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import USUARIO, SENHA

# Configuração padrão do Chrome
def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    return webdriver.Chrome(options=chrome_options), WebDriverWait(webdriver.Chrome(options=chrome_options), 30)

def abrir_pagina(ip):
    """Abre a página de contatos do IP e retorna driver e wait"""
    driver = webdriver.Chrome(options=Options())
    wait = WebDriverWait(driver, 30)
    url = f"https://{USUARIO}:{SENHA}@{ip}/_index.html#/contacts"
    driver.get(url)
    # Espera a tabela aparecer
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr")))
    return driver, wait

def selecionar_todos_contatos(driver, wait, timeout_sec=30):
    """Seleciona todos os checkboxes de contatos, aguardando a página carregar completamente"""
    end_time = time.time() + timeout_sec
    while time.time() < end_time:
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        if checkboxes and all(cb.is_displayed() for cb in checkboxes):
            # Seleciona todos os checkboxes
            for cb in checkboxes:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", cb)
                    if not cb.is_selected():
                        cb.click()
                except Exception as e:
                    print(f"Erro ao clicar checkbox: {e}")
            # Confere se todos foram selecionados
            checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            if all(cb.is_selected() for cb in checkboxes):
                return True
        time.sleep(1)
    return False  # Timeout

def deletar_contatos(driver, wait):
    """Clica no botão de deletar e aceita popup se existir"""
    driver.find_element(By.ID, "delete_button").click()
    try:
        alert = wait.until(EC.alert_is_present())
        print("Texto do popup:", alert.text)
        alert.accept()
    except:
        print("Nenhum popup apareceu")
    print("✔ Todos os contatos foram excluídos")

def importar_agenda(driver, wait, xml_path):
    """Importa a agenda XML"""
    aba_importar = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Importar']")))
    aba_importar.click()
    input_file = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    input_file.send_keys(os.path.abspath(xml_path))
    btn_atualizar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Atualizar'] | //input[@value='Atualizar']"))
    )
    btn_atualizar.click()
    print("✔ Nova agenda enviada com sucesso")
    time.sleep(5)

def atualizar_agenda(ips, xml_path):
    """Função principal que processa todos os IPs"""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")

    for ip in ips:
        print(f"\n🔹 Processando IP {ip}...")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 30)
        url = f"https://{USUARIO}:{SENHA}@{ip}/_index.html#/contacts"
        driver.get(url)

        # Seleciona contatos
        if not selecionar_todos_contatos(driver, wait):
            print(f"❌ Timeout: checkboxes não carregaram corretamente para {ip}")
            driver.quit()
            continue

        # Deleta contatos
        deletar_contatos(driver, wait)

        # Importa agenda
        importar_agenda(driver, wait, xml_path)

        driver.quit()

    print("\n🚀 Processo concluído para todos os IPs!")
