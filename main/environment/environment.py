from direct.showbase.DirectObject import DirectObject
from panda3d.bullet import ZUp
from panda3d.bullet import BulletRigidBodyNode,BulletDebugNode,BulletTriangleMeshShape
from panda3d.bullet import BulletPlaneShape,BulletHeightfieldShape,BulletTriangleMesh
from panda3d.core import PNMImage,Filename,GeoMipTerrain
from panda3d.core import GeomNode,Vec3,Geom
from models.staticModels import sceneModel 



class environment(DirectObject):

    def __init__(self,*args,**kwargs):
        super(environment,self).__init__()
        
        self.sky = loader.loadModel('models/environmentModels/sceneModels/sky/skydome2.egg')
       

        self.modelList = []

        self.terrain = GeoMipTerrain('terrain')


    def setupPhysics(self,**kwargs):
        self.barn = sceneModel(modelName='models/environmentModels/sceneModels/New folder.egg',world=kwargs['world'],dynamic=False)
        self.modelList.append(self.barn)
        self.barn.model.setScale(.14)
        self.barn.nodePath.setPos(8,-5,-1.2)
        self.barn.nodePath.setScale(.4)
        self.barn.model.setZ(self.barn.nodePath.getZ())
        self.mainNp = kwargs['world'].attachNewNode(BulletRigidBodyNode('Heightfield'))
        self.debugNP = kwargs['world'].attachNewNode(BulletDebugNode('Debug'))

        self.crate = sceneModel(modelName='models/environmentModels/sceneModels/crate.egg',world=kwargs['world'],dynamic=True)
        self.crate.nodePath.setScale(.06)
        self.modelList.append(self.crate)
        
       
        self.crate.nodePath.setPos(self.barn.nodePath,(-4,-3,-.9))
        self.crate.model.setPos(self.crate.nodePath,(15.8,5.6,-1.9))
        self.crate.model.setScale(1.2)
        self.debugNP.show()
        self.debugNP.node().showNormals(True)
        height = 10.0

        skytexture= loader.loadTexture('models/environmentModels/sceneModels/sky/tex/skydome.png')     
        self.sky.setTexture(skytexture)
        self.sky.reparentTo(kwargs['world'])
        
       
        img = PNMImage(Filename('models/environmentModels/eartharena/tex/terrainHeight.png'))
        shape = BulletHeightfieldShape(img,height, ZUp)
        shape.setUseDiamondSubdivision(True)
       
        self.mainNp.node().addShape(shape)
        
        self.mainNp.setPos(0,0,.01)
        self.mainNp.setScale(.340)
        self.mainNp.setCollideMask(kwargs['mask'])
        
       
       
        
        self.terrain.setHeightfield(Filename('models/environmentModels/eartharena/tex/terrainHeight.png'))
        self.terrain.setBlockSize(64)
        self.terrain.setNear(50)
        self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)

        

        rootNp = self.terrain.getRoot()
        rootNp.reparentTo(render)
        rootNp.setSz(15)
  
        texture = loader.loadTexture('models/environmentModels/eartharena/tex/nova_TX.jpg')
        rootNp.setTexture(texture)
        
        
        offset = img.getXSize() / 2.0 - 0.25
        rootNp.setPos(-offset, -offset, -height / 2.0)
        self.terrain.generate()
      

    

       
            
