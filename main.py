from parser import WebParser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

link = 'https://career.habr.com/vacancies?page=1&s[]=44&s[]=76&s[]=43&type=all'

parser = WebParser(link)

parser.parse()

print(parser.get_data())
