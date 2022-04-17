from numpy import place
import requests
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import inquirer
import time
import json
load_dotenv()



mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_NAME')
)
API_KEY= os.getenv('API_KEY')
mysql_cursor = mydb.cursor(buffered=True)
mysql_cursor.execute('CREATE TABLE IF NOT EXISTS augments_match_data (id INTEGER AUTO_INCREMENT PRIMARY KEY, matchid TEXT,elo TEXT,game_version TEXT,placement INT,augment TEXT,api_name TEXT,tier TEXT,round TEXT ,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
mysql_cursor.execute('CREATE TABLE IF NOT EXISTS matches (id INTEGER AUTO_INCREMENT PRIMARY KEY, matchid TEXT,elo TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
mysql_cursor.execute('CREATE TABLE IF NOT EXISTS augments_stats (id INTEGER AUTO_INCREMENT PRIMARY KEY, name TEXT,api_name TEXT,tier TEXT,avg_placement FLOAT,avg_placement14 FLOAT,avg_placement33 FLOAT,avg_placement46 FLOAT ,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
print(mysql_cursor.statement)
mydb.commit()

mysql_cursor.execute('SELECT * FROM augmentsdb.matches;')

matchesIds = mysql_cursor.fetchall()

matchDatas = []


    
    

def grab_player_data(requests_count):
    ranks = ['challenger','grandmaster','master']
    
    for rank in ranks:
        print(requests_count)
        if(requests_count == 99):
            print('Request count = 99, sleep')
            time.sleep(62)
            requests_count = 0
        try:
            players = requests.get('https://na1.api.riotgames.com/tft/league/v1/'+rank+'?api_key='+API_KEY).json()
            print(players['entries'])
        except Exception as e:
            print(f'Error: {e}, Error ao processar playerbase,aguardando por 60 segundos...')
            time.sleep(60)
            continue
        requests_count += 1
        for player in players['entries']:
            if(requests_count == 99):
                print('Request count = 99, sleep')
                time.sleep(62)
                requests_count = 0
                
            try:    
                summoner = requests.get(' https://na1.api.riotgames.com/tft/summoner/v1/summoners/'+player['summonerId']+'?api_key='+API_KEY).json()
                requests_count += 1
                print(summoner)
            except Exception as e:
                print(f'Error: {e}, Error ao buscar o summoner,aguardando por 60 segundos...')
                time.sleep(60)
                continue 
               
            if(requests_count == 99):
                print('Request count = 99, sleep')
                time.sleep(62)
                requests_count = 0
            try:    
                matches = requests.get('https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/'+summoner['puuid']+'/ids?count=20&api_key='+API_KEY).json()
                requests_count += 1
            except Exception as e:
                print(f'Error: {e}, Error ao buscar partidas,aguardando por 60 segundos...')
                time.sleep(60)
                continue
            
            for match in matches:
                mysql_cursor.execute('SELECT * FROM augmentsdb.matches where matchid = %s;', (match,))
                match_id_check = mysql_cursor.fetchall()
                if(len(match_id_check) > 0):
                    print('Id de partida já existente >> ', match)
                    continue
                
                mysql_cursor.execute(f'INSERT INTO matches (matchid,elo) VALUES ("{match}","{rank}")')
                print(mysql_cursor.statement)
                mydb.commit()

    return True



def grab_match_data(matchesIds,requests_count):
    json_file = open('augments_stats_formated.json')
    json_data = json.load(json_file)
    print('Buscando dados de partidas')
    for index,match in enumerate(matchesIds):
        print(f"{index}/{len(matchesIds)} partidas...")
        matchId = match[1]
        mysql_cursor.execute('SELECT * FROM augmentsdb.augments_match_data where matchid = %s;', (matchId,))
        match_id_check = mysql_cursor.fetchall()
       
        
        
        if(len(match_id_check) > 0):
            print('Id de partida já existente >> ', match[1])
            continue
        
        if(requests_count == 99):
            print('Request count = 99, sleep')
            time.sleep(62)
            requests_count = 0
        try:    
            matchData = requests.get('https://americas.api.riotgames.com/tft/match/v1/matches/'+match[1]+'?api_key='+API_KEY).json()
            time.sleep(2)
            requests_count += 1
             
            for participant in matchData['info']['participants']:
                    print(participant)
                    for index,augment in enumerate(participant['augments']):
                        gameversion = matchData['info']['game_version']
                        placement = participant['placement']
                        if(index == 0):
                            round = 'stage14'

                        if(index == 1):
                            round = 'stage33'
                            
                        if(index == 2):
                            round = 'stage46'
                                    
                        
                        
                        augment_object = list(filter(lambda x: x['api'] == augment, json_data))
                        if(len(augment_object) > 0): 
                            formated_object = augment_object[0]
                            formated_name = formated_object['name']
                            formated_api_name = formated_object['api']
                            formated_tier = formated_object['tier']                  
                            mysql_cursor.execute(f'INSERT INTO augments_match_data (matchid,elo,game_version,placement,augment,api_name,tier,round) VALUES ("{match[1]}","challenger","{gameversion}","{placement}","{formated_name}","{formated_api_name}","{formated_tier}","{round}")')
                            print(mysql_cursor.statement)
                            mydb.commit()
                        else:
                            mysql_cursor.execute(f'INSERT INTO augments_match_data (matchid,elo,game_version,placement,augment,api_name,tier,round) VALUES ("{match[1]}","challenger","{gameversion}","{placement}","-","{augment}","-","{round}")')
                            print(mysql_cursor.statement)
                            mydb.commit()
        except Exception as e:
            print(e)
            print('Erro ao buscar dados de partida')
            print(match[1])
            time.sleep(2)
            continue        
        json_file.close()
 
 
def generate_augments_stats():
    mysql_cursor.execute('SELECT distinct api_name FROM augmentsdb.augments_match_data;')
    print(mysql_cursor.statement)
    augments_names = mysql_cursor.fetchall() 
    for augment in augments_names:
        agument_name = augment[0]
        mysql_cursor.execute(f"""SELECT 
            (SELECT DISTINCT
                    augment
                FROM
                    augments_match_data
                WHERE
                    api_name = "{agument_name}") AS name,
            (SELECT DISTINCT
                    api_name
                FROM
                    augments_match_data
                WHERE
                    api_name = "{agument_name}") AS api_name,
            (SELECT DISTINCT
                    tier
                FROM
                    augments_match_data
                WHERE
                    api_name = "{agument_name}") AS tier,
            (SELECT 
                    AVG(placement)
                FROM
                    augmentsdb.augments_match_data
                WHERE
                    api_name = "{agument_name}") AS avgPlacement,
            (SELECT 
                    AVG(placement)
                FROM
                    augmentsdb.augments_match_data
                WHERE
                    api_name = "{agument_name}"
                        AND round = "stage14") AS avgPlacement_14,
            (SELECT 
                    AVG(placement)
                FROM
                    augmentsdb.augments_match_data
                WHERE
                    api_name = "{agument_name}"
                        AND round = "stage33") AS avgPlacement_33,
            (SELECT 
                    AVG(placement)
                FROM
                    augmentsdb.augments_match_data
                WHERE
                    api_name = "{agument_name}"
                        AND round = "stage46") AS avgPlacement_46""")
        print(augment[0])
        print(mysql_cursor.statement)
        stats = mysql_cursor.fetchall()[0]
        print(stats)
        mysql_cursor.execute(f"""SELECT * FROM augmentsdb.augments_stats where api_name = "{agument_name}" """)
        stats_exists = mysql_cursor.fetchall()
        stats14 = stats[4]
        stats33 = stats[5]
        stats46 = stats[6]
        
        if(stats[4] == None):
            stats14 = 0
        if(stats[5] == None):
            stats33 = 0
        if(stats[6] == None):
            stats46 = 0
            
        if len(stats_exists) > 0:
            mysql_cursor.execute(f'UPDATE  augments_stats SET name="{stats[0]}",api_name="{stats[1]}",tier="{stats[2]}",avg_placement={stats[3]},avg_placement14={stats14},avg_placement33={stats33},avg_placement46={stats46} where api_name = "{agument_name}"')
            print(mysql_cursor.statement)
            mydb.commit() 
        else:
            mysql_cursor.execute(f'INSERT INTO augments_stats (name,api_name,tier,avg_placement,avg_placement14,avg_placement33,avg_placement46) VALUES ("{stats[0]}","{stats[1]}","{stats[2]}","{stats[3]}","{stats14}","{stats33}","{stats46}")')
            print(mysql_cursor.statement)
            mydb.commit()

                   
                    
def main():
    
    global request_count
    requests_count = 0
    
   
    mysql_cursor.execute('SELECT * FROM augmentsdb.matches;')
    matchesIds = mysql_cursor.fetchall()
    questions = [
                  inquirer.List('awnser',
                      message="Deseja realizar update nos stats?",
                      choices=['Sim','Não'],
                  ),
                  ]
    answers = inquirer.prompt(questions)
    if answers['awnser'] == 'Sim':
        generate_augments_stats()
    
        
    questions = [
                  inquirer.List('awnser',
                      message="Deseja realizar update da playerbase?",
                      choices=['Sim','Não'],
                  ),
                  ]
    answers = inquirer.prompt(questions)
    if answers['awnser'] == 'Sim':
        grab_player_data(requests_count)
        
        
     
    if(len(matchesIds) > 0):
        grab_match_data(matchesIds,requests_count)
        
   

main()