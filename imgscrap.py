from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import wget

driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())

driver.get('https://lolchess.gg/guide/augments')
driver.maximize_window()
imgs = driver.find_elements_by_class_name('guide-augments__image')

print(imgs[0].get_attribute('src'))
path = os.getcwd()
path = os.path.join(path, 'imgs')
os.mkdir(path)
errors = []
for img in imgs:
    try:
        img_link = img.get_attribute('src')
        print(img_link)
        filename = img_link.split('/')[-1]
        print(filename)
        save_as = os.path.join(path,filename)
        wget.download(img_link, save_as)
    except Exception as e:
        print('Error:', e)
        errors.append(img_link)
        continue
print(errors)
print('finalizado')