# -*- coding: utf-8 -*-
import cocos
from cocos.director import director
import define


class Gameover(cocos.layer.ColorLayer):  # 继承ColorLayer类，实现Gameover图层
    def __init__(self):
        super(Gameover, self).__init__(200, 235, 235, 200, 4000, 300)  # 初始化函数，传入的参数为r,g,b,a(alpha-透明度),width,height
        self.position = (director.get_window_size()[0] / 2 - 200,
                         director.get_window_size()[1] / 2 - 150)  # 根据窗口被创建时的尺寸确定图形位置，get_window_size取得窗口的尺寸
        self.visible = False  # 初始化为不可见(游戏进行时) 游戏结束时被gluttonous.py设为可见从而表示游戏结束

        self.score = cocos.text.Label('',
                                      font_name='SimHei',
                                      font_size=63,
                                      color=define.MAROON)  # 设置"得分"的格式
        self.score.position = 250, 200  # 设置"得分"的位置
        self.add(self.score)  # 图层中加入"得分"

        text = cocos.text.Label('SCORE: ',
                                font_name='SimHei',
                                font_size=24,
                                color=define.MAROON)  # 设置"SCORE:"的格式
        text.position = 50, 200  # 设置"SCORE:"的位置
        self.add(text)  # 图层中加入"SCORE:"

        text = cocos.text.Label('CLICK TO REPLAY...',
                                font_name='SimHei',
                                font_size=24,
                                color=define.MAROON)  # 设置"CLICK TO REPLAY..."的格式
        text.position = 50, 100  # 设置"CLICK TO REPLAY..."的位置
        self.add(text)  # 图层中加入"CLICK TO REPLAY..."
