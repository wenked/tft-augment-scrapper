from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

driver.get('https://tactics.tools/augments')


def adding_filters(tier='silver'):
    time.sleep(3)
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



def main():
    try:
      adding_filters(tier='prismatic')
    except Exception as e:
      print(f'Error: {e}')
      driver.close()  
      
main()      