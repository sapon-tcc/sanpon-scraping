import logging
import time
import traceback

from app.mongo import MongoDB
from app.skoob import SkoobScraping

def logar_erro(excecao):
    """Registra o traceback de uma exceção."""
    traceback_string = traceback.format_exc()  # Obtém o traceback como uma string
    # Você pode fazer algo com a string do traceback, como escrevê-la em um arquivo de log
    # Neste exemplo, apenas imprimimos a string do traceback
    logging.error(f"Erro detectado: {excecao}")
    logging.error(traceback_string)

try:
    mongo = MongoDB("books")
    books_to_scraping = mongo.retrieve_books_to_scraping()
    time.sleep(0.1)
    skoob = SkoobScraping()
    logging.info("Scraping do skoob inicializado com sucesso.")
    time.sleep(0.1)
    
    for book in books_to_scraping:
        try:
            if book["volumeInfo"]["industryIdentifiers"]:
                identificador = book["volumeInfo"]["industryIdentifiers"][0]["identifier"]
            else:
                mongo.update_book(book)
                continue
        except IndexError:
            continue
            
        try:
            skoob.update_page()
            skoob.select_search_method("ISBN")
            time.sleep(0.1)
            logging.info("Método de pesquisa selecionado.")
            skoob.search(str(identificador))
            logging.info("Selecionando livro")
            time.sleep(0.1)
            skoob.select_item()
            logging.info("Iniciando processo de seleção de resenhas")
            time.sleep(0.1)
            skoob.select_reviews()
        except Exception as e:
            logar_erro(e)
            
        finally:
            mongo.update_book(book)
    
except Exception as e:
    logar_erro(e)
    
finally:
    logging.info(f"\n\nFinalizando scraping...")
    skoob.robot.driver.close()
    exit(0)