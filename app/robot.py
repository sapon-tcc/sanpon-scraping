import os
import time
import logging

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import SessionNotCreatedException

from .mongo import MongoDB

# Configure o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

FORMATO = "%Y-%m-%d %H:%M:%S"
SELENIUM_SERVER_URL = os.getenv("SELENIUM_SERVER_URL")

class Robot():
    
    def __init__(self, url: str, ) -> None:
        self.url = url
        
        try:
            options = webdriver.FirefoxOptions()
            options.headless = False
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
            self.driver.get(self.url)
            time.sleep(0.5)
        except Exception as e:
            logging.info(f'\nFalha ao inicializar drive local\nTentando remoto. \n{e}')
            logging.info(f'\nIniciando driver remoto\n{SELENIUM_SERVER_URL}')
            try:
                self.driver = webdriver.Remote(
                    command_executor=f'http://{SELENIUM_SERVER_URL}/wd/hub',
                    options=options,
                    desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True}
                )
                self.driver.get(self.url)
                time.sleep(0.5)
                logging.info(f'\nDriver remoto Inicializado com sucesso.\nAcessando site: {self.url}')
            except Exception as e:
                logging.error(f"\nErro ao inicializar driver remoto: {e}\n ")
                time.sleep(0.5)
                raise ValueError(e)
            
    def get_element_by_class_name(self, value: str):
        self.element = self.driver.find_element(by=By.CLASS_NAME, value=value)
        time.sleep(0.5)
        return self.element
    
    def get_element_by_id(self, value: str):
        self.element = self.driver.find_element(by=By.ID, value=value)
        time.sleep(0.5)
        return self.element
    
    def get_element_by_xpath(self, value: str):
        self.element = self.driver.find_element(by=By.XPATH, value=value)
        time.sleep(0.5)
        return self.element
        
    def select_by_option(self, option: str):
        select = Select(self.element)
        time.sleep(0.5)
        logging.info(f"\nOpções de pesquisa --> {list(map(lambda op: op.text, select.options))} ")
        select.select_by_visible_text(option)
    
    def to_fill_input(self, content: str):
        time.sleep(0.5)
        self.element.send_keys(content)        
        
    def click(self):
        time.sleep(0.5)
        self.element.click()
        
    def remove_element_dom(self):
        self.driver.execute_script("arguments[0].remove();", self.element)
    
    def log_element_text(self, id):
        # Espere que a div seja carregada dinamicamente
        self.get_element_by_id(id)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, id)))
        logging.info(f"\n\n ELEMENT TEXT -->{self.element.text}")
        print(f"\n\n ELEMENT TEXT -->{self.element.text}")
        
    def save_element_text(self, id):
        
        self.get_element_by_id(id)
        
        # O conteúdo nesse site é carregado dinâmicamente, então, precisa esperar carregar ou interagir com a página para carregar o texto.
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.text_to_be_present_in_element((By.ID, id), ' '))
            logging.info(f"Texto Extraído --> {self.element.text}")
        except Exception as e:
            logging.error(f"Falha ao obter resenha, tentando clicar para carregar conteúdo dinâmico... {e}")
            try:
                self.element.click()
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.text_to_be_present_in_element((By.ID, id), ' '))
                logging.info(f"Texto Carregado após clique --> {self.element.text}")
            except:
                try:
                    wait.until(EC.text_to_be_present_in_element((By.ID, id), ' '))
                    logging.info(f"Texto Carregado após clique --> {self.element.text}")
                except:
                    logging.error(f"Falha ao obter resenha, tentando próximo... {e}")
                    return
        
        if not MongoDB("opinioes").colecao.find_one({"skoobId": id}):
            logging.info(f"Salvando Texto Extraído --> {self.element.text}")
            
            MongoDB("opinioes").colecao.insert_one({
                "skoobId": id,
                "text": self.element.text,
                "book_id": self.book_id
                "dtCatch": datetime.now().strftime(FORMATO)
            })
        else:
            logging.info(f"Resenha já existe na Base de Dados -->{id}")

    def f5(self):
        self.driver.get(self.url)
        time.sleep(0.5)