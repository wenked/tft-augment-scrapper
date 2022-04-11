from pickle import TRUE
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common import exceptions
import pandas as pd
import time
import sqlite3
import logging
import inquirer
import sys
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="w3nked17",
  database='augments'
)

mysql_cursor = mydb.cursor(buffered=TRUE)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
db = sqlite3.connect('augments.db')
db.set_trace_callback(print)
cursor = db.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS augments (id INTEGER PRIMARY KEY, name TEXT,tier TEXT, pickrate TEXT, placement TEXT, top4 TEXT, winrate TEXT, stage14 TEXT, stage33 TEXT, stage46 TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
db.commit()


def insert_mysql(data,update=False,id=None):
      if update:
        mysql_cursor.execute(f'UPDATE augments SET name=%s,tier=%s,pickrate=%s,placement=%s,top4=%s,winrate=%s,stage14=%s,stage33=%s,stage46=%s,updatedAt=CURRENT_TIMESTAMP WHERE id={id}',data)
      else:    
        mysql_cursor.execute('INSERT INTO augments (name, tier, pickrate, placement, top4, winrate, stage14, stage33, stage46) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', data)
      mydb.commit()


def insert_data(data,update=False,id=None):
      if update:
            cursor.execute(f'UPDATE augments SET name=?,tier=?,pickrate=?,placement=?,top4=?,winrate=?,stage14=?,stage33=?,stage46=?,updated_at=CURRENT_TIMESTAMP WHERE id={id}',data)
      else:    
        cursor.execute('INSERT INTO augments (name, tier, pickrate, placement, top4, winrate, stage14, stage33, stage46) VALUES (?,?,?,?,?,?,?,?,?)', data)
      db.commit()


def select_driver(driver='firefox'):
      if driver == 'Firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        return driver
      elif driver == 'Edge':
        driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
        return driver



def adding_filters(driver,tier='silver'):
    time.sleep(5)
    # alerta cookies
    logging.info('Adicionando filtros...')
    time.sleep(5)

    if tier == 'silver':
      # desmarcando gold checkbox
      driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/label/span[1]/input').click()
      
      # marcando silver checkbox
      driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/label[1]/span[1]/input').click()
     
    if tier == 'gold':
      # desmarcando prismatic checkbox
      driver.find_element_by_xpath('//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/label[2]/span[1]/input').click()
      
      # marcando gold checkbox
      driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/label/span[1]/input').click()
     
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




def get_data(tier,driver):
  counter = 0    
  counter_linha_nome = 2
  counter_linha = 1
  logging.info('Fazendo scraping de dados...')
  nome =  driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[{counter_linha_nome}]/div/div/div')
  while nome:
      try:
        nome =  driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[{counter_linha_nome}]/div/div/div').text
      except exceptions.NoSuchElementException:
        nome = False
        continue     
      pickrate = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[1]/div').text
      place = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[2]').text
      top4 = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[3]').text
      win = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[4]').text
      stage14 = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[5]').text
      stage33 = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[6]').text
      stage46 = driver.find_element_by_xpath(f'//*[@id="__next"]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[7]').text 
      data = (nome,tier, pickrate, place, top4, win, stage14, stage33, stage46) 
      data_exists = db.execute("SELECT * FROM augments WHERE name = :nome AND tier = :tier",(nome,tier)).fetchall()
      mysql_cursor.execute(f"SELECT * FROM augments WHERE name = %s AND tier = %s",(nome,tier)).fetchall()
      datasql_exists = mysql_cursor.fetchall()
      print(datasql_exists)
      if(len(datasql_exists) > 0):
          id = data_exists[0][0]
          print(id)
          insert_mysql(data,update=True,id=id)
      else:
        insert_mysql(data)
      
      if(len(data_exists) > 0):
            id = data_exists[0][0]
            print(id)
            insert_data(data,update=True,id=id)
            insert_mysql(data,update=True,id=id)
      else:      
        insert_data(data)
      counter_linha += 1  
      counter_linha_nome += 1
      counter += 1
  else:
    logging.info(f'Fim do scraping de dados. Total de {counter} registros inseridos na database.')

def scrap_data(api=False):
      tiers =['prismatic','gold','silver']
      if(api):
            driver =select_driver('Edge')
      else:
       
        questions = [
                  inquirer.List('driver',
                      message="Selecione o driver que deseja utilizar",
                      choices=['Firefox','Edge'],
                  ),
                  ]
        answers = inquirer.prompt(questions)
        driver = select_driver(answers['driver'])
      driver.get('https://tactics.tools/augments')
      driver.maximize_window()
      driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div[1]/button[2]').click()
      for tier in tiers:
          adding_filters(driver,tier=tier)
          get_data(tier=tier,driver=driver)
      driver.close()  
        
      time.sleep(5)
      print('FIM')
    
def main():
      if(len(sys.argv) > 1):
            if(sys.argv[1] == 'scrap'):
                  scrap_data(api=True)
                  return
                  
      exists = db.execute("SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND  name='augments');").fetchall()[0][0]

      if exists == 1:
        questions = [
                  inquirer.List('awnser',
                      message="Database já existe, deseja atualizar ela ?",
                      choices=['Sim','Não'],
                  ),
                  ]
        answers = inquirer.prompt(questions)
        if answers['awnser'] == 'Sim':
            scrap_data()
            return
        else:
          questions = [
                  inquirer.List('awnser',
                      message="Deseja vizualizar os dados ?",
                      choices=['Sim','Não'],
                  ),
                  ]
          answers = inquirer.prompt(questions)
          if(answers['awnser'] == 'Sim'):
                data = pd.read_sql("SELECT * FROM augments", db)
                data.to_excel('augments.xlsx')
                print(data)
          else:
              return
      else:      
        scrap_data()
        return
     
     
         
main()      