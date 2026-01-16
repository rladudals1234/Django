from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # 화면이 나올때까지 대기
from selenium.webdriver.support import expected_conditions as EC    # 화면상태체크
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
import requests
from bs4 import BeautifulSoup
import time
import os
import csv
import random
# 이메일 발송 라이브러리
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
from datetime import datetime
# 마우스제어
import pyautogui

# 상단 Chrome이 자동화된 테스트 소프트웨어에 의해 제어되고 있습니다 제거
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")

url = "https://www.naver.com"
browser = webdriver.Chrome(options=options)
browser.get(url)
browser.maximize_window() # 최대창으로 확대

pyautogui.sleep(3)
pyautogui.scroll(-700)
pyautogui.sleep(1)
pyautogui.scroll(700)
pyautogui.sleep(1)
pyautogui.moveTo(870, 250)
pyautogui.click()
pyautogui.doubleClick()

input("대기")