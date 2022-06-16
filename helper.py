import pymysql.cursors
import configparser
import logging


def connect_db():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    connection = pymysql.connect(host=config["DEFAULT"]["host"],
                                 user=config["DEFAULT"]["user"],
                                 password=config["DEFAULT"]["password"],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def logging_ofac():
    logging.basicConfig(level=logging.INFO, filemode='a')

    logger = logging.getLogger(__name__)

    handler = logging.FileHandler('ofac.log')
    formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger