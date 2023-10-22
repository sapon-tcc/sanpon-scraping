import traceback
import logging

def logar_erro(excecao):
    """Registra o traceback de uma exceção."""
    traceback_string = traceback.format_exc()  # Obtém o traceback como uma string
    # Você pode fazer algo com a string do traceback, como escrevê-la em um arquivo de log
    # Neste exemplo, apenas imprimimos a string do traceback
    logging.error(f"Erro detectado: {excecao}")
    logging.error(traceback_string)