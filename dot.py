# -*- coding: utf-8 -*-
import random
from cocos.actions import MoveTo, CallFuncS
from cocos.sprite import Sprite

import define


def kill(spr):  #
    spr.unschedule(spr.update)  # 在时间安排表中移除spr的更新
    arena = spr.parent.parent  # 传入arena
    if not spr.is_big:  # sqr为小点
        arena.batch.add(Dot())  # batch中添加Dot
        spr.killer.add_score()  # 增加杀死spr的snake的score
    else:  # sqr为大点
        spr.killer.add_score()  # 增加杀死spr的snake的score
    arena.batch.remove(spr)  # 在batch中移除spr的更新
    if not spr.killer.is_enemy:  # 被snake(玩家)杀死
        arena.parent.update_score()  # 更新得分
    del spr  # 删除spr


class Dot(Sprite):  # 继承Sprite类(CocosNode that displays a rectangular image)，实现Dot类
    def __init__(self, pos=None, color=None):
        if color is None:  # 初始化随机颜色
            color = random.choice(define.ALL_COLOR)

        super(Dot, self).__init__('circle.png', color=color)  # 初始化函数
        self.killed = False  # 状态初始化
        if pos is None:  # 初始化位置
            self.position = (random.randint(40, define.WIDTH - 40),
                             random.randint(40, define.HEIGHT - 40))
            self.is_big = False  # 初始化Dot为小点
            self.scale = 0.8  # 初始化Dot的尺寸
        else:  # 位置信息已存在，改变位置
            self.position = (pos[0] + random.random() * 32 - 16,
                             pos[1] + random.random() * 32 - 16)
            self.is_big = True  # 设置Dot为大点
        self.schedule_interval(self.update, random.random() * 0.2 + 0.1)  # 每个interval根据schedule进行更新

    def update(self, dt):
        arena = self.parent.parent  # 传入arena
        snake = arena.snake  # 传入snake
        self.check_kill(snake)  # 检查是否杀死snake
        for s in arena.enemies:  # 检查是否杀死怪物
            self.check_kill(s)

    def check_kill(self, snake):  # 检查是否被snake杀死
        if (not self.killed and not snake.is_dead) and (
                abs(snake.x - self.x) < 32 and abs(snake.y - self.y) < 32
        ):  # 当自己没有被吃掉且snake活着且距离足够小才满足被吃掉
            self.killed = True  # 改变状态
            self.killer = snake  # 记录击杀者
            self.do(MoveTo(snake.position, 0.1) + CallFuncS(kill))  # 用0.1秒移动自己的位置到snake的位置
