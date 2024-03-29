import time
#import timeit
import logging
from app.mongo import MongoDB
from app.skoob import SkoobScraping
from app.log import logar_erro

def lambda_handler(event={}, context={}):
    try:
        start_time = time.time()
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
                skoob.book_id = book["_id"]
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
        
        skoob.robot.driver.close()
    except Exception as e:
        logar_erro(e)
        
    finally:
        logging.info(f"\n\nFinalizando scraping...")
        return {
            'statusCode': 200,
            'body': {},
            'headers': {
                "Content-Type": "application/json"
            }
        }

#execution_time = timeit.timeit(lambda_handler, number=1)
#print(f"Tempo de execução: {execution_time} segundos")

