from LichessData import LichessData
  
class LiveOpponentAnalyser:
    def __init__(self):
        self.state = "idle"
        self.DEBUG = True
        self.AnalyseOpponent = True
        LichessData.__init__(self)
    
    def run(self):
        while True:
            if self.state.__eq__("idle"):
                for event in self.client.board.stream_incoming_events():
                    if event["type"].__eq__("gameStart"):
                        self.change_state("gameStart")
            elif self.state.__eq__("gameStart"):
                self.getLiveGameInformation()
            


    def getLiveGameInformation(self):
        #streams the moves form the first ongoing match (TODO board api can only be used in challenges)
        # ongoing = self.client.games.get_ongoing(1)
        # for move in (self.client.board.stream_game_state(ongoing[0]["gameId"])):
        #     print(move)
        # self.change_state("idle")
        for move in self.client.games.stream_game_moves(self.client.games.get_ongoing()[0]["gameId"]):
            if "lm" in move:
                print(move["lm"])
            else:
                print(move["fen"])
        self.change_state("idle")

                
    def change_state(self, to_state):
        self.print_debug("{} -> {}".format(self.state, to_state))
        self.state = to_state

    def print_debug(self, msg:str):
        if self.DEBUG:
            print("****  {}  ****".format(msg))
        


if __name__ == "__main__":
    inst = LiveOpponentAnalyser()
    inst.run()
