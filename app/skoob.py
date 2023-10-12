

import logging
import time
import re

from .robot import Robot

class SkoobScraping():
    
    def __init__(self) -> None:
        self.url = "https://www.skoob.com.br/livro/lista/"
        self.xpath_element_selection_type_search = "/html/body/div/div[2]/div[3]/div/div/div[1]/form/select"
        self.xpath_element_button_submit_search = "/html/body/div/div[2]/div[3]/div/div/div[1]/form/input[2]"
        self.xpath_element_item_chosen = "/html/body/div/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/a[1]"
        self.xpath_element_reviews_link = "/html/body/div/div[2]/div[3]/div/div/div[1]/div[1]/ul/li[5]/a"
        self.list_of_reviews_id = "perfil-conteudo-intern"
        self.input_search_id = "BuscaTag"
        self.regex_reviews = r"<div\s+id=\"[^\"]*resenha[^\"]*\">"
        self.robot = Robot(url=self.url)
        time.sleep(0.5)
        
    
    def select_search_method(self, method: str):
        self.robot.get_element_by_xpath(self.xpath_element_selection_type_search)
        logging.info(f"\n\nSelecionando opção de pesquisa: {method}")
        self.robot.select_by_option(method)
        
    def search(self, content: str):
        self.robot.get_element_by_id(self.input_search_id)
        logging.info(f"\n\nPreenchendo compo de pesquisa: {content}")
        self.robot.to_fill_input(content)
        self.robot.get_element_by_xpath(self.xpath_element_button_submit_search)
        logging.info(f"\n\nPesquisando conteúdo: {content}")
        self.robot.click()
        
    def select_item(self):
        self.robot.get_element_by_xpath(self.xpath_element_item_chosen)
        logging.info("\n\nSelecionando item")
        self.robot.click()
        logging.info("\n\nItem selecionado")
        
        
    def select_reviews(self):
        
        # Fechando modal chato
        time.sleep(1)
        self.robot.get_element_by_class_name("modal")
        self.robot.remove_element_dom()
        self.robot.get_element_by_class_name("modal-backdrop")
        self.robot.remove_element_dom()
        
        self.robot.get_element_by_xpath(self.xpath_element_reviews_link)
        logging.info("Abrindo resenhas")
        self.robot.click()
        
        logging.info("Capturando resenhas")
        html = self.robot.driver.page_source
        divs = re.findall(self.regex_reviews, html)
        ids_reviews = [re.search(r'<div\s+id="(.+?)"', div).group(1) for div in divs]
        
        for id_review in ids_reviews:
            time.sleep(1)
            id_skoob = id_review.split("resenha")
            id_completo_comentario = "resenha" + 'c' + id_skoob[-1]
            self.robot.save_element_text(id_completo_comentario)
            
        
        
        self.robot.get_element_by_id(self.list_of_reviews_id)
        
        
        
        
        
        
            
    
    
        