from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common import exceptions
import time

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

def get_data():
  counter_linha_nome = 2
  counter_linha = 1
  data = []
  nome =  driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[{counter_linha_nome}]/div/div/div[2]')
  while nome:
      augment = {}
      try:
        nome =  driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[{counter_linha_nome}]/div/div/div[2]')
        augment['nome'] = nome.text
      except exceptions.NoSuchElementException:
        nome = False
        continue     
      pickrate = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[1]/div')
      place = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[2]')
      top4 = pickrate = driver.find_element_by_xpath(f'/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[{counter_linha}]/div[3]')
      augment['pickrate'] = pickrate.text
      augment['place'] = place.text
      augment['top4'] = top4.text
      print(augment)
      data.append(augment)
      counter_linha += 1  
      counter_linha_nome += 1
  else:
    return data
    
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]
    
    ## /html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div[3]
def main():
      adding_filters(tier='gold')
      data = get_data()
      print(data)
    
      
main()      