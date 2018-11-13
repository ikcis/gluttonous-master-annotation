import cocos
import define
from arena import Arena
from gameover import Gameover


class HelloWorld(cocos.layer.Layer):  # 继承ColorLayer类
    is_event_handler = True  # 设置状态为处理者，获取鼠标和键盘事件

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.arena = Arena()  # 创建Arena对象
        self.add(self.arena)  # 添加Arena对象
        self.score = cocos.text.Label('30',
                                      font_name='Times New Roman',
                                      font_size=24,
                                      color=define.GOLD)  # 设置得分面板的格式
        self.score.position = 20, 440  # 设置得分面板的位置
        self.add(self.score, 99999)  # 加入得分面板并设置Z轴位置为99999

        self.gameover = Gameover()  # 创建Gameover对象
        self.add(self.gameover, 100000)  # 加入Gameover对象

    def update_score(self):  # 更新得分
        self.score.element.text = str(self.arena.snake.score)

    def end_game(self):  # 游戏结束
        self.gameover.visible = True  # 设置Gameover图层为可见
        self.gameover.score.element.text = str(self.arena.snake.score)  # 传递得分参数

    def on_mouse_press(self, x, y, buttons, modifiers):  # 设置重新开始游戏的鼠标事件
        if self.gameover.visible:  # 当前处于游戏结束状态
            self.gameover.visible = False  # 设置Gameover图层不可见
            self.arena.unschedule(self.arena.update)  # 在时间安排表中关闭arena的更新
            self.remove(self.arena)  # 移除arena对象
            self.arena = Arena()  # 创建Arena对象
            self.add(self.arena)  # 添加Arena对象
            self.update_score()  # 更新得分


cocos.director.director.init(caption="Gluttonous Python")  # 标题
cocos.director.director.run(cocos.scene.Scene(HelloWorld()))  # 运行场景即游戏
