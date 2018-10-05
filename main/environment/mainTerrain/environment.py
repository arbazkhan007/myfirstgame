from direct.showbase.DirectObject import DirectObject
from panda3d.bullet import BulletTriangleMesh,ZUp
from panda3d.bullet import BulletRigidBodyNode,BulletDebugNode
from panda3d.bullet import BulletPlaneShape,BulletTriangleMeshShape
from panda3d.core import PNMImage,Filename
from panda3d.core import GeomNode,Vec3


class environment(DirectObject):

    def __init__(self,*args,**kwargs):
        self.modelpath = kwargs['model']
        self.model = loader.loadModel(self.modelpath)
        self.grassmodel = loader.loadModel('models/environmentModels/New folder/grassModel/grassFieldModel.egg.pz')
      
    
        self.model.setScale(92.5)
        self.model.setZ(-5.3)
        
       
        
       
        
        
       
         
        
       



    def setupPhysics(self,**kwargs):
        self.debugNP = kwargs['world'].attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()
        self.debugNP.node().showNormals(True)

        mesh = BulletTriangleMesh()
        
        geomlist = self.model.findAllMatches('**/+GeomNode')
        geom = geomlist[0].node().getGeom(0)
        mesh.addGeom(geom)

        
       
        shape = BulletPlaneShape(Vec3(0,0,0),0)
        node = BulletRigidBodyNode('arena')
        node.addShape(shape)
        
        
        triangle = BulletTriangleMeshShape(mesh,dynamic=False)
        node1 = BulletRigidBodyNode('wall')
        node1.addShape(triangle)
        self.wallNp = kwargs['world'].attachNewNode(node1)
        self.mainNp = kwargs['world'].attachNewNode(node)

        self.mainNp.setCollideMask(kwargs['mask'])
        
    

        
    
          
    def getModel(self):
        self.model.reparentTo(self.mainNp)


    def getZ(self):
        return self.model.getZ()


    def getPos(self):
        return self.model.getPos()
             
       
            
