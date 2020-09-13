import math
import random


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
        p = ' '
        if(to == 0):
            p = 'player'
        else:
            p = 'computer'
        print('{}受到了{}，技能的优先度为{}'.format(p, self.name, self.priority))


skills = [Skills('ジ', -1, 0),
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


class Players:  # 玩家类
    Ep = 0
    power = 0  # 蓄能
    HP = 3
    skill = 0  # 使用技能


print('欢迎来到拍手游戏')
player, computer = Players(), Players()


def Doing():  # 结算
    # 勾
    if(player.skill == 8):
        if(computer.skill == 0 and player.HP==1):
            player.HP += 1
            computer.HP -= 1
    elif(computer.skill == 8 and computer.HP==1):
        if(player.skill == 0):
            computer.HP += 1
            player.HP -= 1
    # 同时攻击类
    elif(player.skill > 3 and computer.skill > 3):
        if(skills[player.skill].priority > skills[computer.skill].priority):
            computer.HP += table[player.skill - 4][0][0]
        elif (skills[player.skill].priority < skills[computer.skill].priority):
            player.HP += table[computer.skill - 4][0][0]
    # 一方防御类
    elif(player.skill > 3):
        computer.HP += table[player.skill - 4][computer.skill][0]
        player.HP += table[player.skill - 4][computer.skill][1]
    elif(computer.skill > 3):
        computer.HP += table[computer.skill - 4][player.skill][1]
        player.HP += table[computer.skill - 4][player.skill][0]
    # 狙击
    if(player.skill == 7 and computer.skill == 0):
        if(random.choice(range(0, 8)) == 0):
            print('computer被爆头！')
            computer.HP -= 1
    if(computer.skill == 7 and player.skill == 0):
        if(random.choice(range(0, 8)) == 0):
            print('player被爆头！')
            player.HP -= 1


while player.HP > 0 and computer.HP > 0:
    print('Player HP:{} Ep{}   Computer HP:{} Ep{}\n'.format(
        player.HP, player.Ep, computer.HP, computer.Ep))
    for i in range(0, len(skills)):
        print('{}、{}'.format(i, skills[i].name))
    player.skill = int(input('输入你的技能符'))
    # 贷款判定
    if(player.Ep >= skills[player.skill].cost):
        player.Ep -= skills[player.skill].cost
        skills[player.skill].doing(0)
    else:
        player.HP -= (skills[player.skill].cost - player.Ep) / 2
        player.Ep = 0
        player.skill = 0
    # 电脑不会贷款
    check = 0
    while not check:
        computer.skill = random.choice(range(0, len(skills) + 5))
        if(computer.skill >= len(skills)):
            computer.skill = 0
        check = computer.Ep >= skills[computer.skill].cost
    computer.Ep -= skills[computer.skill].cost
    skills[computer.skill].doing(1)
    Doing()
