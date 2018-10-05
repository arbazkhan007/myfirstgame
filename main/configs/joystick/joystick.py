import pygame

from direct.showbase.DirectObject import DirectObject



class joystick(DirectObject):

    def __init__(self,*kwargs):
        
        super(joystick,self).__init__()
        pygame.init()
        
        num_of_joy = pygame.joystick.get_count()
        if num_of_joy > 0:
            pygame.joystick.init()
            self.joylist = {}
            for i in range(num_of_joy):
                self.joylist['player{}'.format(i + 1)] = pygame.joystick.Joystick(i)
            for key in self.joylist:
                self.joylist[key].init()

        else:
            self.joylist = (None,None)

        
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                messenger.send('player{}button{}'.format(event.joy + 1,event.button))
                print(event.joy + 1,event.button)

        
            if event.type == pygame.JOYAXISMOTION:
                messenger.send('player{}axis{}'.format(event.joy + 1, event.axis))
           
            if event.type == pygame.JOYBUTTONUP:
                messenger.send('player{}button{}-up'.format(event.joy + 1,event.button))

            if event.type == pygame.JOYHATMOTION:
                messenger.send('player{}axis{}'.format(event.joy + 1,event.hat))
