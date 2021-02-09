import sys
from common import constants as c
import common.settings as settings

if __name__ == "__main__":
    settings.init(sys.argv[1])
    if settings.MY_NAME == 'server':
        from server import network as server_network
        server_network.start_server()
    else:
        from client import listener as client_network
        from common.game import game
        from client.game_engine import init_game_engine
        if not client_network.start_client():
            sys.exit()
        init_game_engine(game=game)