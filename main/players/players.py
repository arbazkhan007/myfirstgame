from direct.actor.Actor import Actor
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.fsm.FSM import FSM
from direct.interval.ActorInterval import ActorInterval
from panda3d.core import Vec3,BitMask32
from panda3d.core import PandaNode,NodePath

from panda3d.bullet import BulletCharacterControllerNode,BulletCapsuleShape
from panda3d.bullet import ZUp

import os




class character(Actor,FSM,GravityWalker):
    RUNSPEED = 2

    def __init__(self,**kwargs):
        animes = {}
        for a,b,c in os.walk('models/char/animes'):
            for d in c:
                animes[d] = 'models/char/animes/%s' %(d)
                  
        super(character,self).__init__(kwargs['char'],anims=animes)
        
        self.name = kwargs['name']
        FSM.__init__(self,self.name)
        self.setH(180)
       
    
        self.setupAnimes()
        self.interval_setup()
        self.setPos(0,0,-.2)
        self.setScale(.2)
        self.lockedOnTarget = True
        self.targets = []
       
        
        self.anim_playList = []
        self.isAction = {'run':False, 'jump':False,'hit_distance':False,'idle':False,'jumpPunch':False,'punch':False,
                         'kick':False,'strifeLeft':False,'strifeRight':False,'runLeft':False,'runRight':False}
        self.animes = {'jump':self.jumpping,'run':self.running,'jumpPunch':self.jumpPunch}
        inputState.watch('run','player1axis1',None)

    def setupPhysics(self,**kwargs):
        
        self.worldNp = kwargs['worldnp']
        self.world = kwargs['world']
        h = .2

        w = .1
        
        shape = BulletCapsuleShape(w, h  , ZUp)
       
        
        self.character = BulletCharacterControllerNode(shape, .5, 'Player_{}'.format(self.name))
  
        self.characterNP = self.worldNp.attachNewNode(self.character)
        
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
       
       
        self.world.attachCharacter(self.character)
        
        self.floater = NodePath(PandaNode('floater'))
        self.floater.reparentTo(self.characterNP)
        self.floater.setZ(self.characterNP,.52)
        self.floater.setY(self.characterNP.getY() + .25)

        
    def setupAnimes(self):
        self.running = self.getAnimControl('run.egg')
        self.jumpping = self.getAnimControl('jump.egg')
        self.jumpPunch = self.getAnimControl('jumppunch.egg')
        self.rightPunch = self.getAnimControl('rightpunch.egg')
        self.leftKick = self.getAnimControl('leftkick.egg')
        self.leftKick.setPlayRate(2)
        self.rightPunch.setPlayRate(3)
        self.actionAnim = [self.rightPunch,self.leftKick]
        self.actionList = []
        
    def setupController(self,joy,player,handler):
        self.game=handler
        if type(joy) != tuple:
            if handler.numofjoy >= 1:
                self.joy = joy['player{}'.format(player + 1)]
                handler.numofjoy -= 1
                taskMgr.add(self.use_joy,'player{}joyUpdate'.format(player + 1))
                self.useKeyboard = False

            else:
                self.joy = 'keyboard{}'.format(player + 1)
                self.useKeyboard = True
                self.use_Keyboard() 
        else:
            self.joy = 'keyboard{}'.format(player + 1)
            self.useKeyboard = True
            self.use_Keyboard()
                                    
           
    def setup_collision(self):
        self.player_results = self.world.contactTest(self.character)                                  
        dt = globalClock.getDt()
        for contact in self.player_results.getContacts():
            print(str(contact.getNode0()) + ' bumps ' + str(contact.getNode1()))
            mpoint = contact.getManifoldPoint()
            #print(mpoint.getDistance())
            #print(mpoint.getLocalPointA())
            
        
    def getModel(self):
        self.reparentTo(self.characterNP)
    
    def use_Keyboard(self):
    
        print(self.joy)
        
    def use_joy(self,task):
        
        self.button1 = self.joy.get_button(0)
        self.button2 = self.joy.get_button(1)
        self.button3 = self.joy.get_button(2)
        self.button4 = self.joy.get_button(3)
        self.button5 = self.joy.get_button(4)
        self.button6 = self.joy.get_button(5)
        self.button7 = self.joy.get_button(6)
        self.button8 = self.joy.get_button(7)
        self.button9 = self.joy.get_button(8)
        self.button10 = self.joy.get_button(9)
        self.button11 = self.joy.get_button(10)
        self.button12 = self.joy.get_button(11)

        self.axis1 = self.joy.get_axis(0)
        self.axis2 = self.joy.get_axis(1)
        self.axis3 = self.joy.get_axis(2)
        self.axis4 = self.joy.get_axis(3)

        self.dpad = self.joy.get_hat(0)
        
        for x in self.actionAnim:
            if x.isPlaying():
                if not x in self.actionList:
                    self.actionList.append(x)
                    print('action')
                break
              
            else:
                if len(self.actionList) > 0:
                    self.actionList.pop(0)
                    
        self.enemy_setup()
        self.joy_controls()
       
        return task.cont

    def toggleLockOn(self):
        if self.lockedOnTarget:
            self.lockedOnTarget = False
        else:
            self.lockedOnTarget = True
    def joy_controls(self):

        
        
        self.speed = Vec3(0,0,0)
        omega = globalClock.getDt()

       

        
        if not self.lockedOnTarget:  
            if  self.axis2 > .4:
                self.characterNP.setH(base.camera.getH() + 180)
                self.speed.setY(self.RUNSPEED)

            elif self.axis2 < -.4:
                self.characterNP.setH(base.camera.getH())
                self.speed.setY(self.RUNSPEED)
              
            elif self.axis1 > .4:
                self.characterNP.setH(base.camera.getH() - 90)
                self.speed.setY(self.RUNSPEED)
        

            elif self.axis1 < -.4:
                self.characterNP.setH(base.camera.getH() + 90)
                self.speed.setY(self.RUNSPEED)
                

            if self.axis1 > .4 and self.axis2 < -.4:
                self.characterNP.setH(base.camera.getH() - 45)

            elif self.axis1 > .4 and self.axis2 > .4:
                self.characterNP.setH(base.camera.getH() - 135)

            elif self.axis1 < -.4 and self.axis2 < -.4:
                self.characterNP.setH(base.camera.getH() + 45)
                
            elif self.axis1 < -.4 and self.axis2 > .4:
                self.characterNP.setH(base.camera.getH() + 135)

            if self.axis3 > .4:
                base.camera.setX(base.camera, +20 * omega)
              
            elif self.axis3 < -.4:
                base.camera.setX(base.camera, -20 * omega)
                

        else:
            if self.axis2 > .4:
                self.speed.setY(-6)

            if self.axis2 < -.4:
                self.speed.setY(6)

            if self.axis1 > .4:
                self.speed.setX(5)

            if self.axis1 < -.4:
                self.speed.setX(-5)

            self.characterNP.lookAt(self.targets[0])




        if (self.axis1 < -.4 and self.axis2 < -.4):
            if self.character.isOnGround():
                if  not self.isAction['runLeft']:
                    self.runLeft()
                    for action in self.isAction:
                        self.isAction[action] = False
                    self.isAction['runLeft'] = True
         

        elif (self.axis1 > .4 and self.axis2 < -.4):
            if self.character.isOnGround():
                if  not self.isAction['runRight']:
                    self.runRight()
                    for action in self.isAction:
                        self.isAction[action] = False
                    self.isAction['runRight'] = True
         
            
        elif self.axis2 > .4 :     
            if self.button2:
                if self.character.isOnGround():
                    if not self.isAction['jump']:
                        self.jump()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['jump'] = True
                    else:
                        if not len(self.actionList):
                            if self.character.isOnGround():
                                if not self.isAction['idle']:
                                    self.idle()
                                    for a in self.isAction:
                                        self.isAction[a] = False
                                    self.isAction['idle'] = True
                 
            elif self.button1:
                if self.character.isOnGround():
                    if not len(self.actionList):
                        if not self.isAction['punch']:
                            self.punch()
                            for action in self.isAction:
                                self.isAction[action] = False
                            self.isAction['punch'] = True
                        
                    elif not self.character.isOnGround():
                        if not self.isAction['jumpPunch']:
                            self.jump_punch()
                            for action in self.isAction:
                                self.isAction[action] = False
                            self.isAction['jumpPunch'] = True
                        
            else:
                if self.character.isOnGround():
                    if self.isAction['run'] != True:
                        self.run()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['run'] = True
            
        elif self.axis2 < -.4:
            if self.button2:
                if self.character.isOnGround():
                    if not self.isAction['jump']:
                        self.jump()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['jump'] = True
                    else:
                        if not len(self.actionList):
                            if self.character.isOnGround():
                                if not self.isAction['idle']:
                                    self.idle()
                                    for a in self.isAction:
                                        self.isAction[a] = False
                                    self.isAction['idle'] = True
                 
            elif self.button1:
                if self.character.isOnGround():
                    if not len(self.actionList):
                        if not self.isAction['punch']:
                            self.punch()
                            for action in self.isAction:
                                self.isAction[action] = False
                            self.isAction['punch'] = True
                        
                    elif not self.character.isOnGround():
                        if not self.isAction['jumpPunch']:
                            self.jump_punch()
                            for action in self.isAction:
                                self.isAction[action] = False
                            self.isAction['jumpPunch'] = True
                        
            else:
                if self.character.isOnGround():
                    if self.isAction['run'] != True:
                        self.run()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['run'] = True
                        
        

        elif  self.axis1 > .4 :
            if self.lockedOnTarget:
                if self.character.isOnGround():
                    if self.isAction['strifeRight'] != True:
                        self.strifeRight()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['strifeRight'] = True

            else:
                if self.character.isOnGround():
                    if self.isAction['run'] != True:
                        self.run()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['run'] = True

        elif self.axis1 < -.4:
            if self.lockedOnTarget:
                if self.character.isOnGround():
                    if self.isAction['strifeLeft'] != True:
                        self.strifeLeft()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['strifeLeft'] = True

            else:
                if self.character.isOnGround():
                    if self.isAction['run'] != True:
                        self.run()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['run'] = True
                        
                            
        elif self.button2:
            if self.character.isOnGround():
                if not self.isAction['jump']:
                    self.jump()
                    for action in self.isAction:
                        self.isAction[action] = False
                    self.isAction['jump'] = True
                    
                else:
                    if not len(self.actionList):
                        if self.character.isOnGround():
                            if not self.isAction['idle']:
                                self.idle()
                                for a in self.isAction:
                                    self.isAction[a] = False
                                self.isAction['idle'] = True
                
        elif self.button1:
            if self.character.isOnGround():
                if not len(self.actionList):
                    if not self.isAction['punch']:
                        self.punch()
                        for action in self.isAction:
                            self.isAction[action] = False
                        self.isAction['punch'] = True
                
            elif not self.character.isOnGround():
                if not self.isAction['jumpPunch']:
                    self.jump_punch()
                    for action in self.isAction:
                        self.isAction[action] = False
                    self.isAction['jumpPunch'] = True
                    
        elif self.button3:
            if self.character.isOnGround():
                if not len(self.actionList):
                    if not self.isAction['kick']:
                        self.kick()
                        for action in self.isAction:
                            self.isAction[action] =False
                        self.isAction['kick'] = True

                    else:
                        if not len(self.actionList):
                            if self.character.isOnGround():
                                if not self.isAction['idle']:
                                    self.idle()
                                    for a in self.isAction:
                                        self.isAction[a] = False
                                    self.isAction['idle'] = True
        else:
            if not len(self.actionList):
                if self.character.isOnGround():
                    if not self.isAction['idle']:
                        self.idle()
                        for a in self.isAction:
                            self.isAction[a] = False
                        self.isAction['idle'] = True
                        
                
                
        if self.button5:
            self.toggleLockOn()
        self.character.setLinearMovement(self.speed,True)
   



    def enemy_setup(self):
        for enemy in self.game.listOfPlayers:
            if enemy.character.name != self.character.name:
                if not enemy in self.targets:
                    self.targets.append(enemy)
            
    def interval_setup(self):
        self.jumpInterval = self.actorInterval('jump.egg',loop=0,startFrame=1,
                                               endFrame=10)
        self.jumpPunchInterval  = self.actorInterval('jumppunch.egg',playRate=2,
                                                     loop=0, startFrame=self.jumpPunch.getNumFrames()/2,
                                                     endFrame=self.jumpPunch.getNumFrames())
        

 
    def lockON(self,player):
        self.characterNP.lookAt(player)

    def punch(self):
        self.request('Punch')

    def kick(self):
        self.request('Kick')

    def jump_punch(self):
        self.request('JumpPunch')
        
    def jump(self):
        self.request('Jump')
        
    def run(self):
        self.request('Run')
        
    def runLeft(self):
        self.request('RunLeft')
        
    def runRight(self):
        self.request('RunRight')
        
    def strifeLeft(self):
        self.request('StrifeLeft')

    def strifeRight(self):
        self.request('StrifeRight')
    
    def idle(self):
        self.request('Idle')
        
    #Finite State Rquests
    def enterJumpPunch(self):
        self.jumpPunchInterval.start()

    def enterPunch(self):
        self.rightPunch.play()
       

    def enterKick(self):
        self.leftKick.play()
    
    def enterJump(self):
        
        self.character.setMaxJumpHeight(5.0)
        self.character.setJumpSpeed(2.0)
        self.jumpInterval.start()
        self.character.doJump()

    def enterIdle(self):
        self.loop('idle.egg')



    def enterRun(self):
        self.loop('run.egg')

    def enterRunLeft(self):
        self.loop('runleft.egg')

    def enterRunRight(self):
        self.loop('runright.egg')
        
    def enterStrifeLeft(self):
        self.loop('leftstrife.egg')
      
    def enterStrifeRight(self):
        self.loop('rightstrife.egg')
       
    def exitJumpPunch(self):
        self.jumpPunchInterval.finish()
        

    def exitRun(self):
        self.stop()

    def exitRunLeft(self):
        self.stop()

    def exitRunRight(self):
        self.stop()
      
    def exitStrifeLeft(self):
        self.stop()

    def exitStrifeRight(self):
        self.stop()
    def exitPunch(self):
        self.stop()

    def exitKick(self):
        self.stop()
        

    def exitJump(self):
        self.stop()
        
    def exitIdle(self):
        self.stop()
        
        
    def debug_mode(self):
        pass
        
    
 
    


