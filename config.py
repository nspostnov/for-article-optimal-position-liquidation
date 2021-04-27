'''This file consists of some config info variables
'''
from dotenv import dotenv_values


ENV_VALUES = dotenv_values('.env')

USER = 'npostnov'  # the username of postgresql database
PASSWORD = ENV_VALUES['ARTICLE_DB_PASSWORD']  # the password for this database
HOST = 'localhost'  # host
PORT = 5432  # port
DB_NAME = 'selection'  # the name of database
PATH_INITIAL = '/Users/npostnov/Data'  # the path consisting the raw files of data (orderlog20190603.txt, ...)
PATH_DATES_FILE = '/Users/npostnov/Data/dates.txt'  # the file with dates (20190603\n20190604...\n)
PATH_SECCODES_FILE = '/Users/npostnov/Data/seccodes_top.txt'  # the file with seccodes (SBER\nVTBR...\n)

PATH_TO_SAVE_1 = '/Users/npostnov/projects/article-almgren-chriss-framework'  # the first part of path to save images
PATH_TO_SAVE_2 = 'report/source/images'   # the second part of path to save images 
