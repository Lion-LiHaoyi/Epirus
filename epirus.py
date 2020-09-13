import math
import random


class Players:  # 玩家类
    name = ''
    Ep = 0
    power = 0  # 蓄能
    HP = 3
    skill = 0  # 使用技能

    def __init__(self, n):
        self.name = n


print('欢迎来到拍手游戏')
player = [Players('玩家'), Players('电脑')]


class Skills:  # 技能类
    cost = 0  # 花费
    who = 0  # 对象
    priority = 0  # 优先级
    name = ''

    def __init__(self, n, a, b, c=3):
        self.name = n
        self.cost = a
        self.who = b
        self.priority = c

    def doing(self, n):
        to = (self.who + n) & 1
        print('{}受到了{}，技能的优先度为{}'.format(
            player[to].name, self.name, self.priority))


skills = [Skills('ジ', -1, 0, 0),
          Skills('防御', 0, 0),
          Skills('反弹', 0, 0),
          Skills('超反', 1, 0),
          Skills('枪', 1, 1, 2),
          Skills('激光剑', 2, 1),
          Skills('坦克', 2, 1),
          Skills('狙击', 2, 1, 1),
          Skills('摄魂指法', 3, 1)]

table = [[[-1, 0], [0, 0], [0, -1], [0, 0]],  # 基础结算表
         [[-1, 0], [0, 0], [-1, 0],  [0, 0]],
         [[-1, 0], [-1, 0], [0, -1], [0, 0]],
         [[-1, 0], [-1, 0], [-1, 0], [0, 0]]]


def Doing():  # 结算
    for i in range(0, 2):
        # 勾
        if(player[i].skill == 8):
            if(skills[player[(i + 1) & 1].skill].priority < 3 and player[i].HP == 1):
                player[i].HP += 1
                player[(i + 1) & 1].HP -= 1
        # 同时攻击类
        elif(player[i].skill > 3 and player[(i + 1) & 1].skill > 3):
            if(skills[player[i].skill].priority > skills[player[(i + 1) & 1].skill].priority):
                player[(i + 1) & 1].HP += table[player[i].skill - 4][0][0]
        # 一方防御类
        elif(player[i].skill > 3):
            player[(i + 1) & 1].HP += table[player[i].skill - 4][player[(i + 1) & 1].skill][0]
            player[i].HP += table[player[i].skill - 4][player[(i + 1) & 1].skill][1]
        # 狙击
        if(player[i].skill == 7 and player[(i + 1) & 1].skill == 0):
            if(random.choice(range(0, 8)) == 0):
                print('{}被爆头！'.format(player[(i + 1) & 1].name))
                player[(i + 1) & 1].HP -= 1


while player[0].HP > 0 and player[1].HP > 0:
    print('Player HP:{} Ep{}   Computer HP:{} Ep{}\n'.format(
        player[0].HP, player[0].Ep, player[1].HP, player[1].Ep))
    for i in range(0, len(skills)):
        print('{}、{}'.format(i, skills[i].name))
    player[0].skill = int(input('输入你的技能符'))
    # 贷款判定
    if(player[0].Ep >= skills[player[0].skill].cost):
        player[0].Ep -= skills[player[0].skill].cost
        skills[player[0].skill].doing(0)
    else:
        player[0].HP -= (skills[player[0].skill].cost - player[0].Ep) / 2
        player[0].Ep = 0
        player[0].skill = 0
    # 电脑不会贷款
    check = 0
    while not check:
        player[1].skill = random.choice(range(0, len(skills) + 5))
        if(player[1].skill >= len(skills)):
            player[1].skill = 0
        check = player[1].Ep >= skills[player[1].skill].cost
    player[1].Ep -= skills[player[1].skill].cost
    skills[player[1].skill].doing(1)
    Doing()
