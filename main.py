import logging

from app.skoob import SkoobScraping


try:
    skoob = SkoobScraping()
    logging.info("\n\nScraping do skoob inicializado com sucesso.")
    skoob.select_search_method("ISBN")
    logging.info("\n\nMétodo de pesquisa selecionado.")
    skoob.search("9788532512062")
    logging.info("\n\nSelecionando livro")
    skoob.select_item()
    logging.info("\n\nIniciando processo de seleção de resenhas")
    skoob.select_reviews()
except Exception as e:
    logging.error(f"\n\nErro no scraping {e}")
    
finally:
    logging.info(f"\n\nFinalizando scraping...")
    skoob.robot.driver.close()
    exit(0)