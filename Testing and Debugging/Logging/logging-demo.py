from fastapi import FastAPI
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    format = "[%(asctime)s] (line %(lineno)d) - %(levelname)s - %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S"
)

@app.get('/logs')
def logs_demo():
    
    logger.debug('This is a debug level log')
    logger.info('This is an Info level log')
    logger.warning('This is a warning level log')
    logger.error('This is an error level log')
    logger.critical('This is a critical level log')
    
    return {'message': 'Check your console logs'}

logger = logging.getLogger(__name__)