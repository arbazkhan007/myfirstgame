from configs.joystick.joystick import joystick
from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionTraverser,CollisionHandlerQueue
from panda3d.core import BitMask32,Vec3
from panda3d.bullet import BulletWorld,ZUp
from math import pi,sin,cos

import logging




class gameMechanics(DirectObject):

    def __init__(self,**kwargs):
        super(gameMechanics,self).__init__()

        self.joy = joystick()
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0,0,-9.81))
        self.arena = kwargs['environment']
        self.worldNp = render.attachNewNode('world')
        self.worldNp.setScale(3)
        self.arena.setupPhysics(world=self.worldNp,mask=BitMask32.allOn())
        self.world.setDebugNode(self.arena.debugNP.node())
        self.world.setDebugNode(self.arena.debugNP.node())
        
        self.listOfPlayers = kwargs['playerslist']
        self.setupCollisions(playerslist=self.listOfPlayers)
        self.world.attachRigidBody(self.arena.mainNp.node())
        for model in self.arena.modelList:
            self.world.attachRigidBody(model.nodePath.node())
        
        
    
        
        self.numofjoy = 0
        taskMgr.add(self.mech_update,'mechupdate')
        
        self.listOfPlayers[1].characterNP.setY(self.listOfPlayers[0], -5)
       # base.disableMouse()
    def setupCollisions(self,**kwargs):
        
        for player in self.listOfPlayers:
            player.setupPhysics(worldnp=self.worldNp,world=self.world)
            player.getModel()

       
       
       
        


    def mech_update(self,task):
        for player in self.listOfPlayers:
            player.setup_collision
        dt = globalClock.getDt()
        self.world.doPhysics(dt,80,1/180)
        
        self.cameraTask(task)
        self.joy.get_input()
       
       
        return task.cont

        
    def cameraTask(self,task):
     
        pass
    
         
    


 

        
