from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

list_kad_numbers = []

with open("list_kadr_number.txt", "r") as f:
    for line in f:
        list_kad_numbers.append(line)


#list_kad_numbers = ['34:00:000000:113101', '34:00:000000:113101', '34:00:000000:113100']
#['34:00:000000:113100', '34:00:000000:113101', '34:00:000000:113102']
list_error = []
email = ''


#Функция, добавления кадастрового номера в error_list
def add_error_list(txt):
    with open("error.txt", "a") as f:
        f.write(txt)

#Функция, которая вставляет данные в форму ввода  send_key_input(browser, '')
def send_key_input(obj, xpath_input, key):
    obj.find_element_by_xpath(xpath_input).send_keys(key)

#Функция, которая нажимает кнопку click_btn(browser, '')
def click_btn(obj, xpath_btn):
    obj.find_element_by_xpath(xpath_btn).click()

#Функция вставки данных и отправки заявления
def insertion_data(kad_number, email):
    # 2. Нажатие кнопки предоставление сведений ЕГРН
    try:
        WebDriverWait(browser, 90).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-page-wrapper"]/div[2]/div/div[2]/div[2]/a[3]')))
    finally:
        click_btn(browser, '//*[@id="main-page-wrapper"]/div[2]/div/div[2]/div[2]/a[3]')
    # End 2.

    # 3. Выбор услуги
    try:
        WebDriverWait(browser, 90).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div/label/div/div[1]/div/span[1]/input')))
    finally:
        send_key_input(browser,
                       '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div/label/div/div[1]/div/span[1]/input',
                       'Предоставление сведений об объектах недвижимости и (или) их правообладателях')
        click_btn(browser, '/html/body/div[7]/div/div/div/div/div/div[2]/div/div/div[1]')
    # End 3.

    # 4. Выбор категории заявителя, адреса эл.почты, вид выписки
    try:
        WebDriverWait(browser, 90).until(EC.presence_of_element_located((By.XPATH,
                                                                         '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/label/div/div[1]/div/span[1]/input')))
    finally:
        click_btn(browser,
                  '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/label/div/div[1]/div/span[1]/input')

        click_btn(browser, '/html/body/div[17]/div/div/div/div/div/div[2]/div/div/div')

        send_key_input(browser,
                       '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/label[2]/div/div[1]/input',
                       email)

        send_key_input(browser,
                       '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/label[1]/div/div[1]/div[1]/div[1]/div[2]/div/input',
                       'Выписка из Единого государственного реестра недвижимости о кадастровой стоимости объекта недвижимости')

        click_btn(browser,
                  '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/label[1]/div/div[1]/div[2]/div/div')
    # End 4.

    # 5. Добавление кадастрового номера, нажатие кнопки далее на форме заявления
    send_key_input(browser,
                   '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/label/div/div[1]/div/div[1]/div[2]/div/input',
                   kad_number)

    try:
        WebDriverWait(browser, 90).until(EC.presence_of_element_located((By.XPATH,
                                                                         '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/label/div/div[1]/div[2]/div/div')))
    except:
        list_error.append(kad_number)
        print(list_error)
        browser.get('https://lk.rosreestr.ru/eservices')
    else:
        click_btn(browser,
                  '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/label/div/div[1]/div[2]/div/div')
        time.sleep(3)
        click_btn(browser, '/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div[2]/div[4]/button')
    # End 5.

    # Нажатие клавиши далее для подтвержения отправки
    try:
        WebDriverWait(browser, 90).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/main/div[2]/div/div/div[2]/div[3]/button[2]')))
    except:
        add_error_list(kad_number)
        browser.get('https://lk.rosreestr.ru/eservices')
    else:
        click_btn(browser, '/html/body/div[1]/div/div[1]/main/div[2]/div/div/div[2]/div[3]/button[2]')
    ###############################

#Если запрос успешно отправлен
    try:
        WebDriverWait(browser, 90).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/main/div[2]/div/div/div/div')))
    except:
        add_error_list(kad_number)
        browser.get('https://lk.rosreestr.ru/eservices')
###############################





#1. Запуска браузера Google Chrome и открытие страницы аунтификации
browser = webdriver.Chrome('/home/atadmin/PycharmProjects/rosreestr/step01/chromedriver')
browser.get('https://lk.rosreestr.ru/eservices')
#End 1.

for x in list_kad_numbers:
    insertion_data(x, email)
