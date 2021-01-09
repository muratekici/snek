from common.game import Game
from client.game_engine import init_game_engine
import sys
from client import network as client_network
from server import network as server_network
from common import constants as c

game = Game()


if __name__ == "__main__":
    c.MY_NAME = sys.argv[1]
    print("MY NAME: " + c.MY_NAME)
    
    if c.MY_NAME == 'server':
        server_network.start_server()
    else:
        client_network.start_client()
        init_game_engine(game=game)
