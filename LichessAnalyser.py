from datetime import datetime, timedelta
import json
from os import mkdir, remove, listdir
from berserk import utils
from LichessData import LichessData
  
#The LichessAnalyer has methods that allow the Player to analyse his own games as well gain insight into other peoples games
class LichessAnalyser(LichessData):
    def __init__(self):
        LichessData.__init__(self)
        
    def getRecentGames(self,username:str, weeks:int):
        #create place to save games or remove the existing files 
        try:
            mkdir(path="./games/{}".format(username))                
        except FileExistsError:
            pass
        try:
            for file in listdir("./games/{}".format(username)):
                remove(path="./games/{}/{}".format(username,file))
        except FileNotFoundError:            
            pass


        #get all games played by a user in a set timeframe
        end = utils.to_millis(datetime.today())
        start = utils.to_millis(datetime.today()-timedelta(weeks=weeks))
        recentGames =self.client.games.export_by_player(username=username, since=start,until=end,max=25)
        
        #dumps the games in json files at ./games/{username}/
        for game in list(recentGames):
            game_id = game["id"]
            entireGame=self.client.games.export(game_id=game_id)
            
            for key in entireGame:
                if isinstance(entireGame[key],datetime):
                    entireGame[key]=json.dumps(entireGame[key].isoformat())

            with open("./games/{}/{}.json".format(username,game_id),'a') as f:
                json.dump(entireGame,f, indent=4)
                

if __name__ == "__main__":
    Analyser = LichessAnalyser()
    Analyser.getRecentGames("Triumpfole",10)