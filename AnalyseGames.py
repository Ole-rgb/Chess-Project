import json
from os import listdir
import chess, chess.pgn, chess.engine
from chess.engine import Cp, Mate, MateGiven
from collections import Counter
from typing import Optional
from io import StringIO
from stockfish import Stockfish

class HelperClass:
    # returns all openings corresponding to the given list of files
    def getOpeningNames(self, username:str,files:list)->dict:
        #uses a map to get the opening names
        return list(map(lambda file : self.getGame(username,file)["opening"]["name"].split(":")[0],files))

    def getGame(self, username:str, file:str):
        return json.load(open("./games/{}/{}".format(username,file)))
    
    
    #returns a list of files where the username has the given color (if the color is not specified the function returns all user games)
    def getFiles(self, username:str,white:Optional[bool]=None):
        files = list()
        for file in listdir("./games/{}".format(username)):
            game = self.getGame(username=username,file=file)
            if white is not None:
                try:
                    if username==game["players"]["white" if white else "black"]["user"]["name"]:
                        files.append(file)
                except KeyError:
                    pass
            else:
                files.append(file)
        return files
        


class ChessAnalyser:
    def __init__(self) -> None:
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("./Stockfish/src/stockfish")
        
    def playTheGame(self,game):
        pgn = StringIO(game["moves"])
        game = chess.pgn.read_game(pgn)
        print(game)

    def getEval(self, time:Optional[int]=0.1):
        info = self.engine.analyse(self.board, chess.engine.Limit(time=time))
        return info["score"]

    def setPoition(self):
        pass
    
    def quitEngine(self):
        self.engine.quit()



if __name__ == "__main__":
    helperClass = HelperClass()
    #gets a saved game
    game = helperClass.getGame("Triumpfole",helperClass.getFiles("Triumpfole",True)[0])
    
    analyser = ChessAnalyser()
    #updates the position on the board to the end position
    analyser.playTheGame(game=game)
    
    #evaluates the end position
    print(analyser.getEval(2))
    
    #quits the engine
    analyser.quitEngine()