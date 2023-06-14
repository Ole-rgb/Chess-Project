from decouple import config
import berserk

class LichessData:
    def __init__(self):
        LICHESS_TOKEN=config("AUTH_TOKEN")
        session = berserk.TokenSession(LICHESS_TOKEN)
        self.client = berserk.Client(session=session)
        