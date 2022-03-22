from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common import exceptions
import time
import sqlite3

db = sqlite3.connect('augments.db')
db.set_trace_callback(print)
cursor = db.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS augments (id INTEGER PRIMARY KEY, name TEXT,tier TEXT, pickrate TEXT, placement TEXT, top4 TEXT, winrate TEXT, stage14 TEXT, stage33 TEXT, stage46 TEXT)')
db.commit()

def insert_data(data):
      cursor.execute('INSERT INTO augments (name, tier, pickrate, placement, top4, winrate, stage14, stage33, stage46) VALUES (?,?,?,?,?,?,?,?,?)', data)
      db.commit()

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

driver.get('https://tactics.tools/augments')


def adding_filters(tier='silver'):
    time.sleep(5)
    # alerta cookies
    print('estou aqui')
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div[1]/button[2]').click()
    print('ué')
    if tier == 'silver':
      # desmarcando gold checkbox
      driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/label/span[1]/input').click()
      # desmarcando prismatic checkbox
      driver.find_element_by_xpath('//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/label[2]/span[1]/input').click()
    if tier == 'gold':
      # desmarcando prismatic checkbox
      driver.find_element_by_xpath('//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/label[2]/span[1]/input').click()
      # desmarcando silver checkbox
      driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/label[1]/span[1]/input').click()
    if tier == 'prismatic':
      # desmarcando gold checkbox
       driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/label/span[1]/input').click()
      # desmarcando silver checkbox
       driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/label[1]/span[1]/input').click() 
        
    # selecionando top 4
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[3]').click()

    # selecionando master+
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div/div[2]/div[2]/div/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/ul/li[2]').click()


## nome2 --   /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]

## nome --    /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]
## pickrate --/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div          
## place --   /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[2]
## top4 --    /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[3]

def get_data(tier):
  counter_linha_nome = 2
  counter_linha = 1

  nome =  driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[{counter_linha_nome}]/div/div/div[2]')
  while nome:
      augment = {}
      try:
        nome =  driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[{counter_linha_nome}]/div/div/div[2]').text
      except exceptions.NoSuchElementException:
        nome = False
        continue     
      pickrate = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[1]/div').text
      place = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[2]').text
      top4 = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[3]').text
      win = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[4]').text
      stage14 = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[5]').text
      stage33 = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[6]').text
      stage46 = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[7]').text 
      data = (nome,tier, pickrate, place, top4, win, stage14, stage33, stage46)
      insert_data(data)
      counter_linha += 1  
      counter_linha_nome += 1
  else:
    print('Dados inseridos na tabela')
    
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]
    
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[3]
def main():
      adding_filters(tier='gold')
      get_data(tier='gold')
      print('FIM')
     
     
         
main()      