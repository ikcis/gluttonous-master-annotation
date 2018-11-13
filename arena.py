import cocos
from cocos.director import director

import define
from snake import Snake
from dot import Dot


class Arena(cocos.layer.ColorLayer):  # 继承ColorLayer类，实现游戏图层，绘制游戏中的界面
    is_event_handler = True  # 设置状态为处理者，接收鼠标和键盘事件

    def __init__(self):
        super(Arena, self).__init__(255, 255, 255, 250, define.WIDTH,
                                    define.HEIGHT)  # 初始化函数，传入的参数为r,g,b,a,width,height,游戏中的界面颜色和窗口的位置
        self.center = (
        director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)  # 根据窗口被创建时的尺寸确定窗口中游戏图形位置及大小
        self.batch = cocos.batch.BatchNode()  # cocos的BatchNode，用于批量绘制会动的游戏元素
        self.add(self.batch)  # 添加batch

        self.snake = Snake()  # 创建snake对象，玩家自己的对象
        self.add(self.snake, 10000)  # 添加snake对象并设置Z轴位置于10000，设置snake的位置
        self.snake.init_body()  # 初始化蛇身

        self.enemies = []  # 保存敌人的list，其他的玩家的蛇（即电脑控制的）
        for i in range(5):  # 添加敌人，一个游戏中的敌对玩家有5个
            self.add_enemy()

        self.keys_pressed = set()  # 创建键盘控制对象

        for i in range(30):  # 添加Dot，每个游戏中的豆子固定为30个，被吃掉一个就会生成一个新的
            self.batch.add(Dot())  # 添加精灵

        self.schedule(self.update)  # 在时间安排表中加入arena的更新

    def add_enemy(self):  # 添加敌人
        enemy = Snake(True)  # 设置初始状态为"是敌人"
        self.add(enemy, 10000)  # 添加敌人并设置Z轴位置于10000
        enemy.init_body()  # 初始化敌人
        self.enemies.append(enemy)  # 添加到保存敌人的list

    def update(self, dt):  # 根据snake的移动更新arena的位置
        self.x = self.center[0] - self.snake.x
        self.y = self.center[1] - self.snake.y

    def on_key_press(self, key, modifiers):  # 键盘按下
        self.keys_pressed.add(key)
        self.snake.update_angle(self.keys_pressed)  # 更新运动轨迹

    def on_key_release(self, key, modifiers):  # 键盘放开
        self.keys_pressed.remove(key)
        self.snake.update_angle(self.keys_pressed)  # 更新运动轨迹
