from panda3d.bullet import BulletRigidBodyNode,BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.core import GeomNode
from panda3d.core import BitMask32


class sceneModel():
    def __init__(self,*args,**kwargs):
        self.model = loader.loadModel(kwargs['modelName'])
        self.worldnp = kwargs['world']
        self.dynamic = kwargs['dynamic'] 
        self.setup_collision(self.model)
        



    def setup_collision(self,modelName):
        mesh = BulletTriangleMesh()
        geoms = GeomNode('{}'.format(modelName))
        a = 0
        for x in self.model.findAllMatches('**/+GeomNode').getPath(0).node().modifyGeoms():
            if a <= len(self.model.findAllMatches('**/+GeomNode')):
                geoms.addGeom(x)
        for geom in geoms.getGeoms():
             mesh.addGeom(geom)
       
        shape = BulletTriangleMeshShape(mesh,dynamic=self.dynamic)
        self.nodePath = self.worldnp.attachNewNode(BulletRigidBodyNode('{}'.format(self.model)))
        self.nodePath.node().addShape(shape)
        self.model.reparentTo(self.nodePath)
        self.model.setPos(self.nodePath.getPos())
