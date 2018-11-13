# -*- coding: utf-8 -*-
import math
import random
import cocos
from cocos.sprite import Sprite

import define
from dot import Dot


class Snake(cocos.cocosnode.CocosNode):  # 继承ColorLayer类，实现snake
    def __init__(self, is_enemy=False):  # 初始化并设置状态为玩家
        super(Snake, self).__init__()  # 初始化
        self.is_dead = False  # 初始化状态为存活
        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度
        self.color = random.choice(define.ALL_COLOR)  # 随机颜色
        if is_enemy:  # 随机怪物位置
            self.position = random.randrange(150, 650), random.randrange(100, 300)
            if 300 < self.x < 500:
                self.x += 200
        else:  # 随机玩家位置
            self.position = random.randrange(350, 450), random.randrange(180, 230)
        self.is_enemy = is_enemy  # 传入状态
        self.head = Sprite('circle.png', color=self.color)  # 设置头的颜色
        self.scale = 1.5  # 设置头的尺寸
        eye = Sprite('circle.png')  # 设置眼睛
        eye.y = 5  # 设置眼睛的Y轴
        eye.scale = 0.5  # 设置眼睛的尺寸
        eyeball = Sprite('circle.png', color=define.BLACK)  # 设置眼球的颜色
        eyeball.scale = 0.5  # 设置眼球的尺寸
        eye.add(eyeball)  # 在眼睛中添加眼球
        self.head.add(eye)  # 在头中添加眼睛
        eye = Sprite('circle.png')  # 设置眼睛
        eye.y = -5  # 设置眼睛的Y轴
        eye.scale = 0.5  # 设置眼睛的尺寸
        eyeball = Sprite('circle.png', color=define.BLACK)  # 设置眼球的颜色
        eyeball.scale = 0.5  # 设置眼球的尺寸
        eye.add(eyeball)  # 在眼睛中添加眼球
        self.head.add(eye)  # 设置眼睛

        self.add(self.head)  # 把头添加进身体

        self.speed = 200  # 设置怪物速度
        if not is_enemy:  # 设置玩家速度
            self.speed = 150
        self.path = [self.position] * 100  # 用一个列表记录蛇头经过的位置，身子则根据路径中对应数据更新位置

        self.schedule(self.update)  # 在时间安排表中加入snake的更新
        if self.is_enemy:  # 更新怪物
            self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)

    def add_body(self):  # 添加进身体
        b = Sprite('circle.png', color=self.color)  # 设置颜色
        b.scale = 1.5  # 设置尺寸
        self.body.append(b)  # 添加进身体
        b.position = self.position  # 传入位置
        self.parent.batch.add(b, 9999 - len(self.body))  # 添加进batch为后续更新

    def init_body(self):  # 初始化身体
        self.score = 30  # 初始化得分
        self.length = 4  # 初始化长度
        self.body = []  # 初始化身体的构成
        for i in range(self.length):  # 添加进身体
            self.add_body()

    def update(self, dt):  # 更新
        self.angle = (self.angle + 360) % 360  # 加360取模，保证为正角度

        arena = self.parent  # 传入arena
        if self.is_enemy:  # 若为怪物则检查是否发生碰撞
            self.check_crash(arena.snake)
        for s in arena.enemies:  # 检查是否与怪物发生碰撞
            if s != self and not s.is_dead:
                self.check_crash(s)
        if self.is_dead:  # 发生碰撞则返回
            return

        if abs(self.angle - self.angle_dest) < 2:  # 角度差很小则直接更新为按键方向
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (
                    self.angle - self.angle_dest < -180):  # 改变的方向与原方向夹角小于180或大于-180
                self.angle -= 500 * dt  # 方向改变速率，dt为两次update之间的间隔时间(schedule中设定)
            else:  # 改变的方向与原方向夹角大于180或大于-180
                self.angle += 500 * dt  # 方向改变速率，dt为两次update之间的间隔时间(schedule中设定)
        self.head.rotation = -self.angle  # 头旋转的角度要匹配转动的方向

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed  # 更新X轴位置
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed  # 更新Y轴位置
        self.path.append(self.position)  # 将更新好的位置添加进记录path的列表

        lag = int(round(1100.0 / self.speed))  # 设置更新身体的延迟(四舍五入)
        for i in range(int(self.length)):  # 依次更新记录身体位置的列表
            idx = (i + 1) * lag + 1  # 第i个部位的偏移
            self.body[i].position = self.path[-min(idx, len(self.path))]  # 将蛇身的位置根据蛇头经过的路径依次更新,取小的目的为防止越界
        m_l = max(self.length * lag * 2, 60)  # 对当前长度在数据更新过程中可能的最大长度
        if len(self.path) > m_l:  # 拓展列表空间以保存更多数据
            self.path = self.path[int(-m_l * 2):]  # 扩大1倍

    def update_angle(self, keys):  # 更新运动角度
        x, y = 0, 0
        if 65361 in keys:  # 左
            x -= 1
        if 65362 in keys:  # 上
            y += 1
        if 65363 in keys:  # 右
            x += 1
        if 65364 in keys:  # 下
            y -= 1
        directs = ((225, 180, 135), (270, None, 90), (315, 0, 45))  # 不同的角度
        direct = directs[x + 1][y + 1]  # 角度合成
        if direct is None:  # 方向不变
            self.angle_dest = self.angle
        else:
            self.angle_dest = direct

    def add_score(self, s=1):  # 添加得分
        if self.is_dead:  # 已经死了则返回
            return
        self.score += s  # 加分
        l = (self.score +2) / 8  # 每多8分长度加1
        if l > self.length:
            self.length += 1
            self.add_body()

    def ai(self, dt):  # 怪物的转向
        self.angle_dest = (self.angle_dest + 360) % 360  # 加360取模，保证为正角度
        if (self.x < 100 and 90 < self.angle_dest < 270) or (
                self.x > define.WIDTH - 100 and (
                self.angle_dest < 90 or self.angle_dest > 270)
        ):  # 怪物即将与左右边框发生撞墙则转向
            self.angle_dest = 180 - self.angle_dest
        elif (self.y < 100 and self.angle_dest > 180) or (
                self.y > define.HEIGHT - 100 and self.angle_dest < 180
        ):  # 怪物即将与上下边框发生撞墙则转向
            self.angle_dest = -self.angle_dest
        else:
            arena = self.parent  # 传入arena
            self.collision_detect(arena.snake)  # 怪物面对玩家的躲避检测
            for s in arena.enemies:  # 怪物间的躲避检测
                if s != self:
                    self.collision_detect(s)

    def collision_detect(self, other):  # 躲避检测，对于在头部范围内的其他蛇身，计算蛇身与蛇头连线的角度，和自身的运动方向进行比较，如果角度相差很小，就意味着会撞上，于是调整当前运动方向。
        if self.is_dead or other.is_dead:  # 两条蛇中有一个已经死了则返回
            return
        for b in other.body:  # 两者的距离
            d_y = b.y - self.y
            d_x = b.x - self.x
            if abs(d_x) > 300 or abs(d_y) > 300:  # 距离足够大则安全
                return
            if d_x == 0:  # 两者位于同一X上(此时夹角的tan不存在，所以需要特判)
                if d_y > 0:
                    angle = 90
                else:
                    angle = -90
            else:
                angle = math.atan(d_y / d_x) * 180 / math.pi  # 计算夹角
                if d_x < 0:
                    angle += 180
            angle = (angle + 360) % 360  # 加360取模，保证为正角度
            if abs(angle - self.angle_dest) < 5:  # 蛇身和蛇头的角度和运动方向角度相差很小说明可能发生碰撞则转向
                self.angle_dest += random.randrange(90, 270)

    def check_crash(self, other):  # 玩家与怪物碰撞检测
        if self.is_dead or other.is_dead:  # 两者中有一个已经死了则返回
            return
        if (self.x < 0 or self.x > define.WIDTH) or (
                self.y < 0 or self.y > define.HEIGHT
        ):  # 撞墙则死亡
            self.crash()
            return
        for b in other.body:  # 根据两者的直线距离判断是否发生了碰撞
            dis = (b.x - self.x) ** 2 + (b.y - self.y) ** 2
            if dis < 576:  # 距离小于24则发生碰撞
                self.crash()
                return

    def crash(self):  # 碰撞处理
        if not self.is_dead:
            self.is_dead = True  # 状态设定为死亡
            self.unschedule(self.update)  # 在时间安排表中移除更新
            self.unschedule(self.ai)  # 在时间安排表中移除怪物
            arena = self.parent  # 传入arena
            for b in self.body:  # 分解身体为Dot
                arena.batch.add(Dot(b.position, b.color))
                arena.batch.add(Dot(b.position, b.color))
                arena.batch.remove(b)  # 从batch中移除

            arena.remove(self)  # 从arena中移除
            arena.add_enemy()  # 重新添加新的怪物
            del self.path  # 删除记录的路径
            if self.is_enemy:  # 死的是怪物
                arena.enemies.remove(self)  # 从enemies中移除
                del self.body  # 删除
                del self
            else:
                arena.parent.end_game()  # 死的是玩家则游戏结束
