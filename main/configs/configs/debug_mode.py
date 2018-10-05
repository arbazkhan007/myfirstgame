from environment.environment import environment
from players.players import character
from configs.configs.gameMechanics import gameMechanics
from direct.wxwidgets.ViewPort import Viewport

import sys


def test_run():
    
    arena =  environment()

  
    player =  character(char='models/char/worrior/warrior.egg',name='worrior')
   



    player2 =  character(char='models/char/gmo/GMO.egg',name='gmo')
   
    
  
    

    
    playerlist = [player,player2]
    game = gameMechanics(playerslist=playerlist,environment=arena)

    players = 0
    game.numofjoy += len(game.joy.joylist)

    
    for player in playerlist:
        player.setupController(game.joy.joylist,players,game)
        players += 1
   
    player2.debug_mode()
    player.debug_mode()
