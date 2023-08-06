from direct.showbase.ShowBase import ShowBase
from math import pi, sin, cos
from direct.task import Task
from direct.actor.Actor import Actor, TransparencyAttrib
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, ConfigVariableString, DirectionalLight, AmbientLight, TextNode
from panda3d.core import loadPrcFileData
from direct.gui.DirectGui import *

loadPrcFileData("", "#fullscreen true")


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        # 其他的场景根节点  self.render2d self.aspect2d self.pixel2d （self.hidden弃用）
        self.scene.setScale(0.25)
        self.scene.setPos(-8, 42, 0)

        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.pandaActor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005)
        # self.pandaActor.setTransparency(TransparencyAttrib.MAlpha)
        # self.pandaActor.setColorScale(1, 1, 1, 0.5)
        # self.pandaActor.setAlphaScale(0.5)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
        # self.pandaActor.place()
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3, Point3(180, 0, 0), startHpr=Point3(0, 0.0))
        hprInterval2 = self.pandaActor.hprInterval(3, Point3(0, 0, 0), startHpr=Point3(180, 0, 0))

        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()
        self.dlight = DirectionalLight('my dlight')
        dlnp = self.render.attachNewNode(self.dlight)
        self.pandaActor.setLight(dlnp)
        self.render.setLight(dlnp)

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((0.1, 0.1, 0.1, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)

        directionalLight = DirectionalLight('directionalLight')
        directionalLight.setColor((0.8, 1, 1, 1))
        directionalLight.setShadowCaster(True, 512, 512)
        directionalLightNp = self.render.attachNewNode(directionalLight)
        directionalLightNp.setHpr(180, -20, 0)
        self.render.setLight(directionalLightNp)
        self.render.setShaderAuto()

        ambient = AmbientLight('ambient')
        ambient.setColor((0.5, 1, 0.5, 1))
        ambientNP = self.pandaActor.attachNewNode(ambient)

        self.pandaActor.setLightOff()
        self.pandaActor.setLight(ambientNP)

        self.useDrive()  # 鼠标键盘控制模式，很难用
        self.useTrackball()  # 默认的控制模式
        bk_text = "This is my Demo"
        # self.textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
        #                                fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
        #                                mayChange=1)
        # b = DirectButton(text="OK",
        #                  scale=0.2, command=self.setText)

    def setText(self):
        bk_text = "Button Clicked"
        self.textObject.setText(bk_text)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 190.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
