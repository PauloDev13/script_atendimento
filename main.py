from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def aceitar_alerta(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alerta = driver.switch_to.alert
        print("Alerta encontrado:", alerta.text)
        alerta.accept()  # ou alerta.dismiss()
    except TimeoutException:
        print("Nenhum alerta apareceu.")


def main():
    driver = None
    try:
        # Configurações do Chrome para rodar em background (sem abrir janela)
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Inicia o Chrome com webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # Define timeout padrão para waits
        wait = WebDriverWait(driver, 20)

        # Acessa a URL de login
        driver.get("http://atendimento.pgm.intranet.natal.rn.gov.br/login")

        # Preenche o login
        usuario_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/input[1]'))
        )
        usuario_input.send_keys("pgmadmin")

        # Preenche a senha
        senha_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login"]/input[2]'))
        )
        senha_input.send_keys("Pgmnet00")

        # Clica no botão de login
        btn_login = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/button'))
        )
        btn_login.click()

        # Navega diretamente para a URL de configurações
        driver.get("http://atendimento.pgm.intranet.natal.rn.gov.br/novosga.settings")

        # Clica na aba especificada
        aba = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="settings"]/ul/li[2]'))
        )
        aba.click()

        # Botões a serem clicados em ordem
        botoes_xpaths = [
            '//*[@id="tab-triagem"]/div/div[2]/div/table[1]/tbody/tr[1]/td[3]/button',
            '//*[@id="tab-triagem"]/div/div[2]/div/table[1]/tbody/tr[2]/td[3]/button',
            '//*[@id="tab-triagem"]/div/div[2]/div/table[1]/tbody/tr[3]/td[3]/button',
        ]

        # Clicar cada botão
        for xpath in botoes_xpaths:
            botao = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            botao.click()
            # aceitar_alerta(driver)
            # Aceita alerta caso apareça
            try:
                wait.until(EC.alert_is_present())
                driver.switch_to.alert.accept()
            except TimeoutException:
                pass

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Erro ao localizar elemento: {e}")
    except WebDriverException as e:
        print(f"Erro no WebDriver: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        # Finaliza o driver de forma segura
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
