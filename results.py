import pandas as pd
import time
import sqlite3
import logging
import inquirer



logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


db = sqlite3.connect('augments.db')
cursor = db.cursor()


def main():
    search_again = True
    
    while search_again:
        my_input = input('Digite o nome do augment: ')
        augment_data = pd.read_sql(f'SELECT name,tier,placement,top4,stage14 FROM augments WHERE name like "%{my_input}%" order by placement asc', db)
        logging.info('Busca realizada com sucesso!')
        print(augment_data)
        questions = [
                  inquirer.List('awnser',
                      message="Deseja fazer outra pesquisa?",
                      choices=['Sim','Não'],
                  ),
                  ]
        answers = inquirer.prompt(questions)
        if(answers['awnser'] == 'Sim'):
            pass
        else:
            return


main()