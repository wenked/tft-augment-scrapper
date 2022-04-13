from numpy import place
import requests
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()



mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_NAME')
)

mysql_cursor = mydb.cursor(buffered=True)
mysql_cursor.execute('CREATE TABLE IF NOT EXISTS augments_match_data (id INTEGER AUTO_INCREMENT PRIMARY KEY, matchid TEXT,elo TEXT,game_version TEXT,placement INT,augment TEXT,round TEXT ,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
mysql_cursor.execute('CREATE TABLE IF NOT EXISTS matches (id INTEGER AUTO_INCREMENT PRIMARY KEY, matchid TEXT,elo TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
print(mysql_cursor.statement)
mydb.commit()

mysql_cursor.execute('SELECT * FROM augmentsdb.matches;')

matchesIds = mysql_cursor.fetchall()

matchDatas = []

if(len(matchesIds) == 0):
    challengers = requests.get('https://br1.api.riotgames.com/tft/league/v1/challenger?api_key=RGAPI-8aaf5c36-0f2d-4eb5-b7de-6a53d7e797e4').json()
    print(challengers['entries'])
    summonerMatches = []



    for challenger in challengers['entries']:
        summoner = requests.get(' https://br1.api.riotgames.com/tft/summoner/v1/summoners/'+challenger['summonerId']+'?api_key=RGAPI-8aaf5c36-0f2d-4eb5-b7de-6a53d7e797e4').json()
        print(summoner)
        matches = requests.get('https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/'+summoner['puuid']+'/ids?count=20&api_key=RGAPI-8aaf5c36-0f2d-4eb5-b7de-6a53d7e797e4').json()
        
        for match in matches:
            print(match,'oi')
            mysql_cursor.execute(f'INSERT INTO matches (matchid,elo) VALUES ("{match}","challenger")')
            summonerMatches.append(match)
            print(mysql_cursor.statement)
            mydb.commit()
else:
        print('entrei aqui')
        for match in matchesIds:
            print(match[1])
            matchData = requests.get('https://americas.api.riotgames.com/tft/match/v1/matches/'+match[1]+'?api_key=RGAPI-8aaf5c36-0f2d-4eb5-b7de-6a53d7e797e4').json()
            
            
          
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
                            
                    data = (match, 'challenger', gameversion, placement, augment)
                    mysql_cursor.execute(f'INSERT INTO augments_match_data (matchid,elo,game_version,placement,augment,round) VALUES ("{match[1]}","challenger","{gameversion}","{placement}","{augment}","{round}")')
                    print(mysql_cursor.statement)
                    mydb.commit()
                    
                    
