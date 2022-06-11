import pymysql.cursors
import configparser


def connect_db():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    connection = pymysql.connect(host=config["DEFAULT"]["host"],
                                 user=config["DEFAULT"]["user"],
                                 password=config["DEFAULT"]["password"],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


