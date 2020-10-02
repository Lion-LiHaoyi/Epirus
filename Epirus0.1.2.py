import math
import random


class Players:  # 玩家类
    name = ''
    Ep = 0
    power = 0  # 蓄能
    HP = 5
    skill = 0  # 使用技能
    no = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 禁用技能

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
        print('{}受到了{}，技能的优先度为{}'.format(
            player[(self.who + n) & 1].name, self.name, self.priority))


skills = [Skills('ジ', -1, 0, 0),
          Skills('防御', 0, 0),
          Skills('反弹', 0, 0),
          Skills('超反', 1, 0),
          Skills('地雷', 3, 0, 0),
          Skills('八卦阵', 0, 0),
          Skills('枪', 1, 1, 2),
          Skills('激光剑', 2, 1),
          Skills('坦克', 2, 1),
          Skills('狙击', 2, 1, 1),
          Skills('真正的落雷', 5, 1, 4),
          Skills('摄魂指法', 3, 1)]

table = [[[-1, 0], [0, 0], [0, -1], [0, 0], [-1, -1]],  # 基础结算表
         [[-1, 0], [0, 0], [-1, 0],  [0, 0], [-1, -1]],
         [[-1, 0], [-1, 0], [0, -1], [0, 0], [-1, -1]],
         [[-1, 0], [-1, 0], [-1, 0], [0, 0], [-1, 0]],
         [[-2, 0], [0, 0], [0, 0], [0, 0], [-2, 0]]]

# 游戏过程
while player[0].HP > 0 and player[1].HP > 0:
    print('Player HP:{} Ep{}   Computer HP:{} Ep{}\n'.format(
        player[0].HP, player[0].Ep, player[1].HP, player[1].Ep))
    for i in range(0, len(skills)):
        print('{}、{}       \t花费为{}'.format(
            i, skills[i].name, skills[i].cost))
    player[0].skill = int(input('输入你的技能符'))
    # 技能判定
    if (player[0].skill > 2 and player[0].no[player[0].skill - 3] > 0):
        player[0].HP -= 1
        player[0].skill = 0
        print('该技能还需{}回合才能使用'.format(player[0].no[player[0].skill - 3]))
    elif(player[0].Ep < skills[player[0].skill].cost):
        player[0].HP -= (skills[player[0].skill].cost - player[0].Ep) / 2
        player[0].Ep = 0
        player[0].skill = 0
        print('你贷款了')
    else:
        player[0].Ep -= skills[player[0].skill].cost
        skills[player[0].skill].doing(0)
    # 电脑技能判定
    check = 0
    while not check:
        player[1].skill = random.randint(0, len(skills) + 10)
        if(player[1].skill >= len(skills)):
            if(player[1].skill > len(skills) + 3):
                player[1].skill = 0
            else:
                player[1].skill = 10
        check = (player[1].Ep >= skills[player[1].skill].cost
                 and player[1].no[player[1].skill - 3] == 0)
        if player[1].skill == 11 and player[1].HP > 1:
            check = 0
    player[1].Ep -= skills[player[1].skill].cost
    skills[player[1].skill].doing(1)
    # 结算
    for i in range(0, 2):
        # 勾
        for j in range(0, 9):
            if(player[i].no[j] > 0):
                player[i].no[j] -= 1
        if(player[i].skill == 11):
            if(player[i].HP <= 1):
                if(player[(i + 1) & 1].skill == 5):
                    if(random.randint(0, 1) == 0):
                        print('判定失败')
                        player[(i + 1) & 1].skill = 0
                    else:
                        print('判定成功')
                        break
                elif(skills[player[(i + 1) & 1].skill].priority < 2):
                    player[i].HP += 1
                    player[(i + 1) & 1].HP -= 1
        # 同时攻击类
        elif(player[i].skill > 5 and player[(i + 1) & 1].skill > 5):
            if(skills[player[i].skill].priority > skills[player[(i + 1) & 1].skill].priority):
                player[(i + 1) & 1].HP += table[player[i].skill - 6][0][0]
                if(player[i].skill == 10):
                    player[i].HP -= 2
                    player[i].no[player[i].skill - 3] = 3
        # 一方防御类
        elif(player[i].skill > 5):
            if(player[(i + 1) & 1].skill == 5):
                if(random.randint(0, 1) == 0):
                    print('判定失败')
                    player[(i + 1) & 1].skill = 0
                else:
                    print('判定成功')
                    break
            player[(i + 1) & 1].HP += table[player[i].skill -
                                            6][player[(i + 1) & 1].skill][0]
            player[i].HP += table[player[i].skill -
                                  6][player[(i + 1) & 1].skill][1]
        # 狙击
        if(player[i].skill == 9 and player[(i + 1) & 1].skill == 0):
            if(random.randint(0, 8) == 0):
                print('{}被爆头！'.format(player[(i + 1) & 1].name))
                player[(i + 1) & 1].HP -= 1
        # 大雷
        if(player[i].skill == 10):
            if(player[(i + 1) & 1].skill > 2):
                player[(i + 1) & 1].no[player[(i + 1) & 1].skill - 3] = 3


# 游戏结束
if(player[0].HP <= 0 and player[1].HP <= 0):
    print('平局')
elif(player[0].HP <= 0):
    print('你输了')
else:
    print('你赢了')
input('按回车退出')
